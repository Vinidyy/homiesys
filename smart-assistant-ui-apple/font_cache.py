# font_cache.py — cache fonts + crisp AA text
import pygame as pg

_cache = {}

def _sysfont(size: int):
    # Prefer SF Pro if installed; fallbacks keep it clean and neutral
    return pg.font.SysFont("SF Pro Display,SF Pro Text,Helvetica Neue,Segoe UI,Roboto,Arial,DejaVuSans", size)

def font(size: int):
    f = _cache.get(size)
    if f is None:
        f = _sysfont(size)
        _cache[size] = f
    return f

def aa_text(text: str, color, size: int) -> pg.Surface:
    """Render at 2x and smoothscale down for sharper edges."""
    f2 = font(size * 2)
    s2 = f2.render(text, True, color)
    return pg.transform.smoothscale(s2, (s2.get_width() // 2, s2.get_height() // 2))
