# data_sources.py — simulated data now, swap to HA REST/MQTT later
import time
import random

_state = {
    "co2": 700,
    "temp": 23.0,
    "bus_in": 6,
    "meeting": "Meeting 10:00"
}

def fake_step():
    # CO2 random walk with occasional spikes
    d = random.randint(-12, 14)
    if random.random() < 0.015:
        d += random.randint(60, 160)
    _state["co2"] = max(380, min(2000, _state["co2"] + d))

    # temp slow drift
    _state["temp"] = max(16.0, min(33.0, _state["temp"] + random.uniform(-0.06, 0.06)))

    # bus countdown randomly ticks
    if random.random() < 0.05:
        _state["bus_in"] -= 1
        if _state["bus_in"] < 0:
            _state["bus_in"] = random.choice([3, 5, 7, 10, 12])

def get_data():
    now = time.strftime("%H:%M")
    return {
        "co2": int(_state["co2"]),
        "temp": float(_state["temp"]),
        "bus_in": int(_state["bus_in"]),
        "meeting": _state["meeting"],
        "time": now
    }

# --- Home Assistant stubs (later) ---
# REST example:
# import requests
# def get_data():
#     headers = {"Authorization": "Bearer YOUR_LONG_LIVED_TOKEN"}
#     base = "http://homeassistant.local:8123/api/states"
#     co2 = float(requests.get(f"{base}/sensor.living_co2", headers=headers).json()["state"])
#     temp = float(requests.get(f"{base}/sensor.living_temp", headers=headers).json()["state"])
#     ... build dict as above ...
#     return {...}
