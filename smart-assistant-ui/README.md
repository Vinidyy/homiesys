# Smart Assistant UI (Starter Template)

This is a minimal Pygame-based UI for your Raspberry Pi assistant display. It simulates
CO₂, temperature, and transit times, shows a friendly face, and has placeholders to
integrate with Home Assistant later (via REST or MQTT).

## Features
- 800×480 window (adjust in `config.json`)
- Animated face (idle, blink, warning)
- Simulated sensors (CO₂, temperature) and next bus time
- Keyboard controls for quick testing
- Ready to swap sim data with Home Assistant

## Quick Start (PC/Mac/Linux)
1. Python 3.10+ recommended.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python main.py
   ```

## Controls
- **B**: Force blink
- **W**: Toggle warning (e.g., high CO₂)
- **F**: Toggle fullscreen
- **ESC / Q**: Quit

## Home Assistant Integration (later)
- Replace `get_data()` in `data_sources.py` with real calls.
- Two common options:
  - **REST API** (simple): Use a Long-Lived Access Token and query sensors.
  - **MQTT** (realtime): Subscribe to topics from HA.

See comments in `data_sources.py` for code stubs.
