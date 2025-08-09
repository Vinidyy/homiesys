# data_sources.py — simulated data; plug Home Assistant later
import time, random

_state = {
    "co2": 720,
    "temp": 23.0,
    "bus_in": 5,
    "meeting": "Standup 10:00"
}

def fake_step():
    # CO2: random walk with occasional spikes
    d = random.randint(-10, 12)
    if random.random() < 0.012:
        d += random.randint(60, 170)
    _state["co2"] = max(380, min(2000, _state["co2"] + d))

    # Temperature slow drift
    _state["temp"] = max(16.0, min(33.0, _state["temp"] + random.uniform(-0.06, 0.06)))

    # Bus countdown
    if random.random() < 0.06:
        _state["bus_in"] -= 1
        if _state["bus_in"] < 0:
            _state["bus_in"] = random.choice([3, 5, 7, 9, 12])

def get_data():
    now = time.strftime("%H:%M")
    return {
        "co2": int(_state["co2"]),
        "temp": float(_state["temp"]),
        "bus_in": int(_state["bus_in"]),
        "meeting": _state["meeting"],
        "time": now
    }

# ----- Home Assistant REST example (later) -----
# import requests
# BASE = "http://homeassistant.local:8123/api/states"
# TOKEN = "YOUR_LONG_LIVED_TOKEN"
# HEADERS = {"Authorization": f"Bearer {TOKEN}"}
# def get_data():
#     co2 = float(requests.get(f"{BASE}/sensor.living_co2", headers=HEADERS).json()["state"])
#     temp = float(requests.get(f"{BASE}/sensor.living_temp", headers=HEADERS).json()["state"])
#     bus_in = int(requests.get("http://your_bus_api/...", timeout=5).json()["minutes"])
#     meeting = "Next: " + requests.get(f"{BASE}/calendar.home", headers=HEADERS).json()["attributes"]["message"]
#     return {"co2":co2, "temp":temp, "bus_in":bus_in, "meeting":meeting, "time": time.strftime("%H:%M")}
