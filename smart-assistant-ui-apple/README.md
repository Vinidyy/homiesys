# Smart Assistant UI — Apple Look (v3)

A modern, cozy, and clean Pygame UI for a Raspberry Pi display. Inspired by Apple's
design language: soft dark background, subtle glow, glass panel, crisp typography,
and gentle motion (blinks, micro-saccades).

## Features
- Face on the left (animated blink + micro eye movements)
- Right-side "glass" info panel (CO₂, temperature, bus, calendar)
- Subtle vignette + glow, Apple-like accent colors
- High-quality text rendering (2x supersampling)
- Configurable via `config.json`
- Ready to swap simulated data with Home Assistant (REST/MQTT stubs)

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Keys
- **B** — Blink
- **F** — Fullscreen toggle
- **Q / ESC** — Quit

## Home Assistant (later)
Replace `get_data()` in `data_sources.py` with real REST or MQTT calls and map your
entity IDs (see stubs inside the file).
