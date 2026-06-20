# qBittorrent Swarm Optimizer

An extremely simple Python script that automatically pauses your seeding torrents if the swarm already has plenty of seeders. This frees up your slots and bandwidth so peers with slower, limited connections can get the data from high-bandwidth seeders instead.

## Features
* **Protects New Torrents:** Will not pause torrents until they hit a minimum seeding time.
* **Saves Bandwidth:** Pauses torrents when the total number of seeders in the swarm exceeds your limit.
* **Dry Run Mode:** Includes a safety switch (`DRY_RUN`) so you can test what it would pause before making changes.

## Requirements
* Python 3.x
* `qbittorrent-api` library

To install the requirement, run:
```bash
pip install qbittorrent-api
