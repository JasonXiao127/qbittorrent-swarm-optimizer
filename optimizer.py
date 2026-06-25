import logging
import os
import sys
from qbittorrentapi import Client, APIConnectionError, LoginFailed

QBIT_HOST = "http://localhost:8080"
QBIT_USER = "admin"
QBIT_PASSWORD = "your_password_here"

MAX_SEEDERS_IN_SWARM = 50
MIN_SEEDING_TIME_SEC = 86400
DRY_RUN = True

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def connect_client():
    try:
        client = Client(host=QBIT_HOST, username=QBIT_USER, password=QBIT_PASSWORD)
        client.auth_log_in()
        return client
    except LoginFailed:
        logging.error("Failed to authenticate with qBittorrent. Check username and password.")
        sys.exit(1)
    except APIConnectionError as e:
        logging.error(f"Failed to connect to qBittorrent WebUI: {e}")
        sys.exit(1)


def main():
    client = connect_client()
    logging.info("Successfully connected to qBittorrent.")

    # Fetch torrents that are currently seeding or active
    # Using 'seeding' status ensures we only target torrents actively seeding or paused-seeding.
    torrents = client.torrents_info(status_filter="seeding")

    torrents_to_pause = []

    for torrent in torrents:
        name = torrent.name
        info_hash = torrent.hash
        
        # 'num_complete' refers to the total number of seeders in the swarm.
        swarm_seeders = torrent.num_complete
        seeding_time = torrent.seeding_time

        # Skip torrents that haven't met the minimum seeding time yet
        if seeding_time < MIN_SEEDING_TIME_SEC:
            logging.debug(f"Skipping '{name}': seeding time ({seeding_time}s) is less than minimum ({MIN_SEEDING_TIME_SEC}s).")
            continue

        # Check if the swarm has enough seeders to pause your upload
        if swarm_seeders > MAX_SEEDERS_IN_SWARM:
            logging.info(
                f"Target identified to pause: '{name}' "
                f"(Seeders in swarm: {swarm_seeders} > Limit: {MAX_SEEDERS_IN_SWARM}, "
                f"Seeding time: {seeding_time // 3600} hours)"
            )
            torrents_to_pause.append(info_hash)

    if not torrents_to_pause:
        logging.info("No active seeding torrents met the criteria for pausing.")
        return

    if DRY_RUN:
        logging.info(f"[DRY RUN] Would have paused {len(torrents_to_pause)} torrent(s).")
    else:
        try:
            # Pause the selected torrents
            client.torrents_pause(torrent_hashes=torrents_to_pause)
            logging.info(f"Successfully paused {len(torrents_to_pause)} torrent(s).")
        except Exception as e:
            logging.error(f"An error occurred while pausing torrents: {e}")


if __name__ == "__main__":
    main()




