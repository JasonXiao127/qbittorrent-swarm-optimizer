# qbittorrent swarm optimizer

A lightweight Python script that automatically pauses seeding torrents when they no longer need your upload bandwidth. If a torrent has met your minimum seeding time and the swarm already has plenty of health (seeders), this script pauses it so you can prioritize rarer files.

---

## Features
* **Bandwidth Optimization:** Automatically targets and pauses over-seeded torrents.
* **Safety Buffer:** Respects a minimum seeding duration before taking any action.
* **Dry Run Safe:** Preview what the script *would* do without changing anything in your client.

---

## Prerequisites

You need Python 3 installed along with the official qBittorrent API wrapper:

```bash
pip install qbittorrent-api
```

---

## Configuration

Open the script and adjust the constants at the top of the file to fit your needs:

* **`QBIT_HOST` / `USER` / `PASSWORD`:** Your qBittorrent WebUI connection details.
* **`MAX_SEEDERS_IN_SWARM`:** The threshold of peer seeders. If the swarm has more than this number, your torrent becomes a candidate to pause.
* **`MIN_SEEDING_TIME_SEC`:** The minimum duration (in seconds) a torrent must seed before the script can touch it.
* **`DRY_RUN`:** Set to `True` (default) to test and view logs safely. Set to `False` to let the script actually pause torrents.

---

## Usage

Run the script manually, or pair it with a cron job (Linux) / Task Scheduler (Windows) to automate it:

```bash
python optimizer.py
```
