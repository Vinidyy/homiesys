import random, time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# Simulated state
state = {"co2": 720, "temp": 23.0, "bus_in": 5, "meeting": "Standup 10:00"}

@app.get("/api/data")
def get_data():
    # simple random walk for demo
    d = random.randint(-10, 12)
    if random.random() < 0.012:
        d += random.randint(60, 170)
    state["co2"] = max(380, min(2000, state["co2"] + d))
    state["temp"] = max(16.0, min(33.0, state["temp"] + random.uniform(-0.06, 0.06)))
    if random.random() < 0.06:
        state["bus_in"] -= 1
        if state["bus_in"] < 0:
            state["bus_in"] = random.choice([3,5,7,9,12])
    return {
        "co2": int(state["co2"]),
        "temp": float(state["temp"]),
        "bus_in": int(state["bus_in"]),
        "meeting": state["meeting"],
        "time": time.strftime("%H:%M")
    }

# Serve static UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
