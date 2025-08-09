# Assistant Web UI (Apple-look, no-Node setup)

A modern, cozy, clean web UI you can **run live right now** — no Node required.
A single FastAPI server serves both the **API** and the **static UI** (HTML/CSS/JS).

## Features
- Face on the left (SVG, subtle blink, micro eye movement)
- Frosted glass info panel on the right (CO₂, °C, bus, calendar)
- Apple-like colors & typography (Inter/SF system fallbacks)
- Live data endpoint at `/api/data` (simulated; swap to Home Assistant later)

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:8000
```

## Home Assistant later
- Edit `app.py` in `get_data()` to query HA REST or WebSocket.
- Or point the frontend to your own HA proxy.

## Deploy on Raspberry Pi (Chromium Kiosk)
1) Install Chromium and set auto-login to a lightweight session.
2) Create a systemd service for `app.py` (gunicorn/uvicorn) on boot.
3) Auto-start Chromium in kiosk mode:
   ```bash
   chromium --kiosk --app=http://localhost:8000 --enable-features=OverlayScrollbar --force-dark-mode --use-gl=egl
   ```
