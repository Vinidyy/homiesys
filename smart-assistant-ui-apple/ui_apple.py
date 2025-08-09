# ui_apple.py — Apple look: face left, frosted glass panel right
import pygame as pg, math, time, random
from font_cache import aa_text

def ease_in_out(t): return t*t*(3-2*t)
def lerp(a, b, s):  return a + (b - a) * s

def draw_vignette(screen, alpha: int = 70):
    if alpha <= 0: return
    w, h = screen.get_size()
    v = pg.Surface((w, h), pg.SRCALPHA)
    pg.draw.rect(v, (0, 0, 0, alpha), v.get_rect(), border_radius=40)
    screen.blit(v, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

def glow_circle(surface, center, radius, color, strength=70):
    if strength <= 0: return
    g = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
    for r in range(radius, 0, -2):
        a = int(strength * (r / radius) ** 2)
        pg.draw.circle(g, (*color, a), (radius, radius), r, 2)
    surface.blit(g, (center[0]-radius, center[1]-radius), special_flags=pg.BLEND_PREMULTIPLIED)

def draw_glass_panel(surface, rect: pg.Rect, alpha=38, border_alpha=60):
    # Frosted look via semi-transparent white + subtle stroke
    glass = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.rect(glass, (255, 255, 255, alpha), glass.get_rect(), border_radius=24)
    pg.draw.rect(glass, (255, 255, 255, border_alpha), glass.get_rect(), width=1, border_radius=24)
    surface.blit(glass, rect.topleft)

class Face:
    def __init__(self):
        self.next_saccade = time.time() + random.uniform(2.5, 5.5)
        self.eye_offset = [0.0, 0.0]
        self.eye_target = [0.0, 0.0]
        self.blink_t = 0.0   # 0..1 while blinking
        self.blink_dur = 0.16
        self.breath_t = 0.0

    def update(self, dt):
        self.breath_t += dt
        # saccades
        if time.time() > self.next_saccade:
            self.eye_target = [random.uniform(-3, 3), random.uniform(-1.5, 2.5)]
            self.next_saccade = time.time() + random.uniform(3.0, 6.0)
        self.eye_offset[0] = lerp(self.eye_offset[0], self.eye_target[0], 0.08)
        self.eye_offset[1] = lerp(self.eye_offset[1], self.eye_target[1], 0.08)

        # random blink
        if self.blink_t <= 0 and random.random() < 0.0028:
            self.blink_t = self.blink_dur
        if self.blink_t > 0:
            self.blink_t = max(0.0, self.blink_t - dt)

    def force_blink(self): self.blink_t = self.blink_dur

    def draw(self, screen, cfg, warning=False):
        w, h = screen.get_size()
        face_w = int(w * 0.64)
        cx, cy = face_w // 2, int(h * 0.54)

        eye_dist = int(min(face_w, h) * 0.22)
        eye_r   = int(min(face_w, h) * 0.09)
        ring_r  = int(min(face_w, h) * 0.42)

        # breathing sway
        cy += int(math.sin(self.breath_t * 0.8) * 2)

        color  = cfg["colors"]["accent"] if not warning else cfg["colors"]["warn"]
        glow_circle(screen, (cx, cy-12), ring_r+8, color, strength=cfg["ui"].get("glow_strength", 70))
        pg.draw.circle(screen, color, (cx, cy-12), ring_r, width=2)

        # blink amount eased
        lid_h = 0
        if self.blink_t > 0:
            t = 1.0 - (self.blink_t / self.blink_dur)
            lid_h = int(eye_r * 1.4 * ease_in_out(t))

        eye_color = cfg["colors"]["fg"]
        for dx in (-eye_dist, eye_dist):
            x = cx + dx + int(self.eye_offset[0])
            y = cy - 12 + int(self.eye_offset[1])
            pg.draw.circle(screen, eye_color, (x, y), eye_r)
            if lid_h > 0:
                rect = pg.Rect(x - eye_r, y - eye_r, 2 * eye_r, lid_h)
                pg.draw.rect(screen, cfg["colors"]["bg"], rect)

        # subtle, friendly mouth
        mouth_w = int(eye_dist * 1.15)
        mouth_y = cy + int(eye_r * 1.4)
        rect = pg.Rect(cx - mouth_w // 2, mouth_y, mouth_w, int(eye_r * 1.2))
        start, end = math.pi * 0.15, math.pi - math.pi * 0.15
        pg.draw.arc(screen, (190, 220, 255), rect, start, end, 4)

class SidePanel:
    def __init__(self): pass

    def _rblit(self, screen, x, w, surf, y):
        screen.blit(surf, (x + w - surf.get_width(), y))

    def draw(self, screen, cfg, data):
        w, h = screen.get_size()
        pad = 22
        panel_x = int(w * 0.68)
        panel_w = w - panel_x - pad
        panel_rect = pg.Rect(panel_x, pad*2, panel_w, h - pad*3)
        draw_glass_panel(screen, panel_rect, cfg["ui"].get("glass_alpha", 38), cfg["ui"].get("glass_border_alpha", 60))

        x = panel_rect.x + 18
        col_w = panel_rect.width - 36
        y = panel_rect.y + 20
        gap = 62
        fg = cfg["colors"]["fg"]
        muted = cfg["colors"]["muted"]
        warn = cfg["colors"]["warn"]

        # headings
        self._rblit(screen, x, col_w, aa_text("CO₂", muted, 22), y - 26)
        co2 = int(data.get("co2", 0))
        co2_col = fg if co2 < cfg["thresholds"]["co2_warn_ppm"] else warn
        self._rblit(screen, x, col_w, aa_text(f"{co2} ppm", co2_col, 48), y); y += gap

        self._rblit(screen, x, col_w, aa_text("Temperature", muted, 22), y - 26)
        temp = data.get("temp", 0.0)
        self._rblit(screen, x, col_w, aa_text(f"{temp:.0f}°C", fg, 40), y); y += gap

        self._rblit(screen, x, col_w, aa_text("Next bus", muted, 22), y - 26)
        self._rblit(screen, x, col_w, aa_text(f"{data.get('bus_in', 0)} min", fg, 34), y); y += gap

        self._rblit(screen, x, col_w, aa_text("Calendar", muted, 22), y - 26)
        self._rblit(screen, x, col_w, aa_text(str(data.get("meeting", "")), fg, 28), y)

def draw_status_bar(screen, cfg, data):
    if not cfg["ui"].get("show_clock", True): return
    pad = 16
    time_surf = aa_text(data.get("time", "--:--"), cfg["colors"]["fg"], 22)
    screen.blit(time_surf, (pad, pad))

def toggle_fullscreen(fs: bool) -> bool:
    if not fs:
        pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.SCALED)
        return True
    pg.display.set_mode((800, 480), pg.SCALED)
    return False
