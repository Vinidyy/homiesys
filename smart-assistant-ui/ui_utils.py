import pygame as pg
import math

def toggle_fullscreen(fs):
    if not fs:
        pg.display.set_mode((0,0), pg.FULLSCREEN | pg.SCALED)
        return True
    else:
        pg.display.set_mode((800,480), pg.SCALED)
        return False

def draw_face(screen, cfg, blink=False, warning=False):
    w, h = screen.get_size()
    cx, cy = w//2, int(h*0.36)
    eye_dist = int(w*0.16)
    eye_r = int(min(w,h)*0.055)
    lid_h = int(eye_r*1.4) if blink else 0

    # face glow ring (subtle)
    ring_r = int(min(w,h)*0.28)
    color = cfg["colors"]["accent"] if not warning else cfg["colors"]["warn"]
    pg.draw.circle(screen, (*color, ), (cx, cy), ring_r, width=2)

    # eyes
    eye_color = cfg["colors"]["fg"]
    for dx in (-eye_dist, eye_dist):
        x = cx + dx
        y = cy
        pg.draw.circle(screen, eye_color, (x, y), eye_r)
        if lid_h > 0:
            # eyelid as rectangle
            rect = pg.Rect(x-eye_r, y-eye_r, 2*eye_r, lid_h)
            pg.draw.rect(screen, cfg["colors"]["bg"], rect)

    # mouth (subtle arc)
    mouth_w = int(eye_dist*1.1)
    mouth_y = cy + int(eye_r*2.2)
    thickness = 3
    rect = pg.Rect(cx - mouth_w//2, mouth_y, mouth_w, int(eye_r*1.0))
    start, end = math.pi*0.15, math.pi - math.pi*0.15
    pg.draw.arc(screen, eye_color, rect, start, end, thickness)

def draw_status_bar(screen, cfg, data):
    w, h = screen.get_size()
    pad = 14
    font = pg.font.SysFont("Inter,Arial,DejaVuSans", 22)
    small = pg.font.SysFont("Inter,Arial,DejaVuSans", 18)

    # left: time
    time_surf = font.render(data.get("time","--:--"), True, cfg["colors"]["fg"])
    screen.blit(time_surf, (pad, pad))

    # right: logo text
    label = small.render("home assistant", True, cfg["colors"]["fg"])
    rw = label.get_width()
    screen.blit(label, (w - pad - rw, pad))

    # bottom separator
    pg.draw.line(screen, (30,30,30), (pad, pad+30), (w-pad, pad+30), 1)

def card(surface, rect, title, value, unit, color_fg, color_value):
    pg.draw.rect(surface, (28,28,28), rect, border_radius=12)
    pg.draw.rect(surface, (40,40,40), rect, width=1, border_radius=12)
    pad = 12
    title_font = pg.font.SysFont("Inter,Arial,DejaVuSans", 18)
    value_font = pg.font.SysFont("Inter,Arial,DejaVuSans", 36)
    t = title_font.render(title, True, color_fg)
    surface.blit(t, (rect.x+pad, rect.y+pad))
    val_text = f"{value}{unit}"
    v = value_font.render(val_text, True, color_value)
    surface.blit(v, (rect.x+pad, rect.y+pad+22))

def draw_cards(screen, cfg, data):
    w, h = screen.get_size()
    pad = 16
    top = int(h*0.55)
    card_w = int((w - pad*3)/2)
    card_h = int(h*0.22)
    r1 = pg.Rect(pad, top, card_w, card_h)
    r2 = pg.Rect(pad*2 + card_w, top, card_w, card_h)

    # decide colors based on thresholds
    co2 = int(data.get("co2", 0))
    temp = float(data.get("temp", 0.0))
    bus = data.get("bus_in", 0)

    co2_color = cfg["colors"]["accent"] if co2 < cfg["thresholds"]["co2_warn_ppm"] else cfg["colors"]["warn"]
    temp_color = cfg["colors"]["accent"] if temp < cfg["thresholds"]["temp_hot_c"] else cfg["colors"]["warn"]
    fg = cfg["colors"]["fg"]

    card(screen, r1, "CO₂", co2, " ppm", fg, co2_color)
    if isinstance(temp, float):
        temp_val = f"{temp:.1f}"
    else:
        temp_val = str(temp)
    card(screen, r2, "Temperatur", temp_val, " °C", fg, temp_color)

    # bus info label on bottom center
    bus_font = pg.font.SysFont("Inter,Arial,DejaVuSans", 22)
    msg = f"🚌 Nächste Bahn in {bus} min" if isinstance(bus, int) else "🚌 Daten…"
    bus_surf = bus_font.render(msg, True, fg)
    screen.blit(bus_surf, ((w - bus_surf.get_width())//2, top + card_h + 10))
