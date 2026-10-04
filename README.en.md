# 📡 Real-Time Network Traffic Dashboard

An app that captures network packets with **Scapy** and displays them in an
interactive dashboard built with **Streamlit** and **Plotly**, refreshing
automatically every 2 seconds.

> Based on the freeCodeCamp tutorial:
> [Build a Real-Time Network Traffic Dashboard with Python and Streamlit](https://www.freecodecamp.org/news/build-a-real-time-network-traffic-dashboard-with-python-and-streamlit/).
> I split the code into modules and modified it (see "Changes from the tutorial").

## What it shows

- Total packets captured and elapsed time
- Protocol distribution (TCP, UDP, ICMP, ARP, IPv6)
- Top 10 source IPs
- Traffic over time (bytes per second)
- Table with the latest captured packets

## Project structure

| File | Role |
|---|---|
| `app.py` | Streamlit interface and auto-refresh |
| `processor.py` | `PacketProcessor` class: processes and stores packets (thread-safe) |
| `sniffer.py` | Packet capture running in a separate thread |
| `visualizations.py` | Plotly charts |

## Requirements

- Python 3.9+
- **Windows:** [Npcap](https://npcap.com) installed
- **Linux/Mac:** root privileges to capture packets

## Installation and usage

```bash
git clone <repo-url>
cd <folder>
python -m venv venv
venv\Scripts\activate        # on Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

⚠️ Packet capture requires **administrator privileges**: open the terminal as
administrator (Windows) or use `sudo` with your virtual environment's Streamlit
(Linux/Mac). If permissions are missing, the app shows the error on screen.

## Changes from the tutorial

- Code split into modules instead of a single file
- A single shared sniffer (`st.cache_resource`) instead of one per session
- Refresh with `st.fragment(run_every=2)` instead of `sleep` + `rerun`
- Sniffer errors are shown in the interface
- Extra charts (top IPs and traffic over time)

## Disclaimer

Use this only to analyze **your own network** or networks you are authorized
to monitor. Capturing other people's traffic without permission may be illegal.
