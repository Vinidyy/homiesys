# font_cache.py — cache fonts + simple high-quality text rendering
import pygame as pg

_cache = {}

def _sysfont(size: int):
    # Inter preferred; fallbacks keep it clean
    return pg.font.SysFont("Inter,DM Sans,Segoe UI,Arial,DejaVuSans", size)

def font(size: int):
    if size not in _cache:
        _cache[size] = _sysfont(size)
    return _cache[size]

def aa_text(text: str, color, size: int) -> pg.Surface:
    """Render text at 2x then smoothscale down for crisper edges."""
    f2 = font(size * 2)
    s2 = f2.render(text, True, color)
    return pg.transform.smoothscale(s2, (s2.get_width() // 2, s2.get_height() // 2))
