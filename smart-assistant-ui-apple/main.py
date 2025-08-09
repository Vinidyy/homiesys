import pygame as pg, json, sys
from pathlib import Path
from data_sources import get_data, fake_step
from ui_apple import toggle_fullscreen, Face, SidePanel, draw_status_bar, draw_vignette

CONFIG_PATH = Path(__file__).with_name("config.json")

def load_config():
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {
            "screen_width": 800, "screen_height": 480, "fps": 60,
            "colors": {"bg":[12,14,18],"fg":[235,235,245],"muted":[128,132,142],"accent":[10,132,255],"warn":[255,69,58]},
            "ui": {"show_clock": True, "vignette_alpha": 70, "glass_alpha": 38, "glass_border_alpha": 60, "glow_strength": 70},
            "thresholds":{"co2_warn_ppm":1000,"temp_hot_c":28.0,"temp_cold_c":18.0}
        }

def main():
    cfg = load_config()
    pg.init()
    flags = pg.SCALED
    screen = pg.display.set_mode((cfg["screen_width"], cfg["screen_height"]), flags)
    pg.display.set_caption("Smart Assistant — Apple Look v3")
    clock = pg.time.Clock()

    face = Face()
    panel = SidePanel()
    fullscreen = False

    while True:
        dt = clock.tick(cfg["fps"]) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); sys.exit(0)
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_q):
                    pg.quit(); sys.exit(0)
                elif event.key == pg.K_b:
                    face.force_blink()
                elif event.key == pg.K_f:
                    fullscreen = toggle_fullscreen(fullscreen)

        # data + sim step
        data = get_data()
        fake_step()

        # updates
        face.update(dt)
        warning = (data["co2"] >= cfg["thresholds"]["co2_warn_ppm"]) or (data["temp"] >= cfg["thresholds"]["temp_hot_c"])

        # draw

        screen.fill((60, 60, 60))  # helles Grau zum Test
        # screen.fill(cfg["colors"]["bg"])
        face.draw(screen, cfg, warning=warning)
        panel.draw(screen, cfg, data)
        draw_status_bar(screen, cfg, data)
        # draw_vignette(screen, cfg["ui"].get("vignette_alpha", 70))

        pg.display.flip()

if __name__ == "__main__":
    main()
