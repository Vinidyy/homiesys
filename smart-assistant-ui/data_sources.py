# Data simulation + future Home Assistant integration
# Swap the content of get_data() with real calls later.
import time, random

_state = {
    "co2": 700,
    "temp": 23.0,
    "bus_in": 7  # minutes
}

def fake_step():
    """Small random walk for simulated values."""
    # CO2 fluctuates; spike sometimes
    delta = random.randint(-10, 12)
    if random.random() < 0.01:
        delta += random.randint(50, 180)
    _state["co2"] = max(380, min(2000, _state["co2"] + delta))

    # Temperature slow drift
    _state["temp"] = max(16.0, min(33.0, _state["temp"] + random.uniform(-0.05, 0.05)))

    # Bus countdown
    _state["bus_in"] -= 1 if random.random() < 0.05 else 0
    if _state["bus_in"] < 0:
        _state["bus_in"] = random.choice([3,5,7,10,12])

def get_data():
    """Return current data dict.
    Replace this with Home Assistant fetch:
      - REST: requests.get('http://HA:8123/api/states/sensor.co2', headers={'Authorization': 'Bearer TOKEN'})
      - MQTT: subscribe in a separate thread and update shared state.
    """
    # Example shape:
    # return {
    #     "co2": float(current_co2_ppm),
    #     "temp": float(current_temperature_c),
    #     "bus_in": int(next_bus_minutes),
    #     "time": "HH:MM"
    # }
    now = time.strftime("%H:%M")
    return {
        "co2": _state["co2"],
        "temp": _state["temp"],
        "bus_in": _state["bus_in"],
        "time": now
    }
