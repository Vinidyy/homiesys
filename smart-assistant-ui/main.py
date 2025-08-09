import pygame as pg
import sys, math, time, random
from pathlib import Path
from data_sources import get_data, fake_step
from ui_utils import draw_face, draw_status_bar, draw_cards, toggle_fullscreen
import json

CONFIG_PATH = Path(__file__).with_name("config.json")

def load_config():
    try:
        return json.loads(Path(CONFIG_PATH).read_text(encoding="utf-8"))
    except Exception:
        # sensible defaults
        return {
            "screen_width": 800,
            "screen_height": 480,
            "fps": 60,
            "colors": {"bg":[18,18,18],"fg":[224,224,224],"accent":[38,166,154],"warn":[244,67,54]},
            "thresholds":{"co2_warn_ppm":1000,"temp_hot_c":28.0,"temp_cold_c":18.0},
            "ui":{"show_clock":True,"show_bus":True}
        }

def main():
    cfg = load_config()
    pg.init()
    flags = pg.SCALED
    screen = pg.display.set_mode((cfg["screen_width"], cfg["screen_height"]), flags)
    pg.display.set_caption("Smart Assistant UI")
    clock = pg.time.Clock()

    # UI state
    blink = False
    blink_timer = 0.0
    warning_override = False
    fullscreen = False

    while True:
        dt = clock.tick(cfg["fps"]) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); sys.exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_q):
                    pg.quit(); sys.exit(0)
                elif event.key == pg.K_b:
                    blink = True; blink_timer = 0.18
                elif event.key == pg.K_w:
                    warning_override = not warning_override
                elif event.key == pg.K_f:
                    fullscreen = toggle_fullscreen(fullscreen)
        
        # Simulate new data
        data = get_data()
        fake_step()  # advance simulation
        
        # Blink logic
        if not blink and random.random() < 0.0025:  # occasional spontaneous blink
            blink = True
            blink_timer = 0.14
        if blink:
            blink_timer -= dt
            if blink_timer <= 0:
                blink = False
        
        # Warnings (co2/temp)
        warn = warning_override or (data["co2"] >= cfg["thresholds"]["co2_warn_ppm"]) or (data["temp"] >= cfg["thresholds"]["temp_hot_c"])
        
        # Draw
        screen.fill(cfg["colors"]["bg"])
        draw_face(screen, cfg, blink=blink, warning=warn)
        draw_status_bar(screen, cfg, data)
        draw_cards(screen, cfg, data)
        
        pg.display.flip()

if __name__ == "__main__":
    main()
