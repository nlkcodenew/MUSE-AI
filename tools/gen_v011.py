#!/usr/bin/env python3
"""Sinh artwork cho MUSE-AI v0.1.1: icon pin/mang + watermark tung he.
Tat ca la hinh ve goc bang PIL (khong dung artwork game co ban quyen).
Watermark: bieu tuong truu tuong dai dien cho tung he, mo 18%, dat sau ten he.
Icon: ve sieu phan giai 3x roi thu nho cho net."""
from PIL import Image, ImageDraw, ImageFilter
import math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "art", "icons")
SYS = os.path.join(ROOT, "art", "sys")
os.makedirs(ICONS, exist_ok=True)
os.makedirs(SYS, exist_ok=True)

PAPER = (245, 240, 230)
AMBER = (255, 180, 84)
TEAL = (92, 200, 180)
SS = 3  # supersampling


def canvas(w, h):
    return Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))


def finish(im, w, h):
    return im.resize((w, h), Image.LANCZOS)


def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([c * SS for c in box], radius=r * SS,
                        fill=fill, outline=outline, width=width * SS)


def circle(d, cx, cy, r, fill=None, outline=None, width=1):
    d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS],
              fill=fill, outline=outline, width=width * SS)


def line(d, pts, fill, width=1):
    d.line([(x * SS, y * SS) for x, y in pts], fill=fill, width=width * SS,
           joint="curve")


def poly(d, pts, fill=None, outline=None):
    d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill, outline=outline)


def with_alpha(rgb, a):
    return (rgb[0], rgb[1], rgb[2], a)


# ---------------- icon pin / mang ----------------
def battery(name, frac, charging=False):
    W, H = 96, 48
    im, d = canvas(W, H), None
    im = canvas(W, H)
    d = ImageDraw.Draw(im)
    # khung + cuc
    rr(d, (4, 8, 80, 40), 8, outline=with_alpha(PAPER, 255), width=4)
    rr(d, (82, 18, 92, 30), 3, fill=with_alpha(PAPER, 255))
    if charging:
        # tia set ho phach giua khung
        poly(d, [(48, 12), (34, 28), (44, 28), (38, 40), (56, 24), (45, 24)],
             fill=with_alpha(AMBER, 255))
    elif frac > 0:
        iw = int(68 * frac)
        rr(d, (10, 14, 10 + iw, 34), 4, fill=with_alpha(AMBER, 255))
    finish(im, W, H).save(os.path.join(ICONS, name))


def wifi():
    W, H = 64, 64
    im = canvas(W, H)
    d = ImageDraw.Draw(im)
    cx, cy = 32, 52
    for r, w in ((12, 5), (22, 5), (32, 5)):
        d.arc([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS],
              start=225, end=315, fill=with_alpha(PAPER, 255), width=w * SS)
    circle(d, cx, cy, 4, fill=with_alpha(PAPER, 255))
    finish(im, W, H).save(os.path.join(ICONS, "network.png"))


def plane():
    W, H = 64, 64
    im = canvas(W, H)
    d = ImageDraw.Draw(im)
    poly(d, [(10, 38), (54, 10), (44, 44), (34, 36)],
         fill=with_alpha(PAPER, 255))
    poly(d, [(10, 38), (34, 36), (30, 52)], fill=with_alpha(AMBER, 255))
    finish(im, W, H).save(os.path.join(ICONS, "planemode.png"))


battery("batt-full.png", 1.0)
battery("batt-75.png", 0.75)
battery("batt-50.png", 0.50)
battery("batt-25.png", 0.25)
battery("batt-empty.png", 0.0)
battery("batt-charge.png", 0.0, charging=True)
wifi()
plane()

# ---------------- watermark tung he ----------------
A = 46  # alpha watermark (~18%)


def wm_base():
    im = Image.new("RGBA", (1280 * SS, 720 * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def wm_save(im, name):
    im = im.filter(ImageFilter.GaussianBlur(1.5 * SS))
    finish(im, 1280, 720).save(os.path.join(SYS, name + ".png"))


def pad(d, cx, cy, w, h, r=18):
    """Tay cam tong quat: than + D-pad + 2 nut."""
    rr(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), r,
       outline=with_alpha(PAPER, A), width=5)
    # D-pad trai
    x, y = cx - w / 2 + 70, cy
    poly(d, [(x - 26, y - 10), (x + 26, y - 10), (x + 26, y + 10),
             (x - 26, y + 10)], fill=with_alpha(PAPER, A))
    poly(d, [(x - 10, y - 26), (x + 10, y - 26), (x + 10, y + 26),
             (x - 10, y + 26)], fill=with_alpha(PAPER, A))
    # 2 nut phai
    circle(d, cx + w / 2 - 78, cy - 8, 16, fill=with_alpha(AMBER, A))
    circle(d, cx + w / 2 - 40, cy + 14, 16, fill=with_alpha(TEAL, A))


def handheld(d, cx, cy, w, h, screen=True):
    rr(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 26,
       outline=with_alpha(PAPER, A), width=5)
    if screen:
        rr(d, (cx - w / 2 + 52, cy - h / 2 + 40, cx + w / 2 - 52,
               cy + h / 2 - 110), 8, outline=with_alpha(TEAL, A), width=4)


def draw_fbneo(d):
    # can joystick arcade: can + bi + de
    line(d, [(640, 470), (640, 240)], with_alpha(PAPER, A), 14)
    circle(d, 640, 200, 52, fill=with_alpha(AMBER, A))
    poly(d, [(500, 470), (780, 470), (820, 560), (460, 560)],
         outline=with_alpha(PAPER, A))
    circle(d, 560, 505, 18, fill=with_alpha(TEAL, A))
    circle(d, 640, 505, 18, fill=with_alpha(AMBER, A))
    circle(d, 720, 505, 18, fill=with_alpha(PAPER, A))


def draw_nes(d):
    rr(d, (420, 300, 860, 430), 10, outline=with_alpha(PAPER, A), width=6)
    x, y = 500, 365
    poly(d, [(x - 34, y - 12), (x + 34, y - 12), (x + 34, y + 12),
             (x - 34, y + 12)], fill=with_alpha(PAPER, A))
    poly(d, [(x - 12, y - 34), (x + 12, y - 34), (x + 12, y + 34),
             (x - 12, y + 34)], fill=with_alpha(PAPER, A))
    circle(d, 740, 355, 20, fill=with_alpha(AMBER, A))
    circle(d, 800, 380, 20, fill=with_alpha(TEAL, A))


def draw_snes(d):
    rr(d, (400, 300, 880, 440), 40, outline=with_alpha(PAPER, A), width=6)
    x, y = 500, 370
    poly(d, [(x - 32, y - 11), (x + 32, y - 11), (x + 32, y + 11),
             (x - 32, y + 11)], fill=with_alpha(PAPER, A))
    poly(d, [(x - 11, y - 32), (x + 11, y - 32), (x + 11, y + 32),
             (x - 11, y + 32)], fill=with_alpha(PAPER, A))
    # 4 nut kim cuong (mau SNES goc, lam mo)
    for (bx, by, c) in ((760, 330, (120, 200, 120)), (800, 370, (230, 220, 120)),
                        (720, 370, (230, 120, 120)), (760, 410, (120, 150, 230))):
        circle(d, bx, by, 18, fill=with_alpha(c, A))


def draw_psx(d):
    # tam giac / tron / gach cheo / vuong
    line(d, [(560, 300), (640, 440), (720, 300)],
         with_alpha((120, 220, 140), A), 8)
    circle(d, 560, 500, 55, outline=with_alpha((230, 120, 120), A), width=8)
    line(d, [(700, 460), (800, 560)], with_alpha((120, 160, 230), A), 8)
    line(d, [(800, 460), (700, 560)], with_alpha((120, 160, 230), A), 8)
    rr(d, (430, 440, 530, 540), 6, outline=with_alpha((230, 140, 200), A), width=8)


def draw_n64(d):
    # tay cam 3 chac don gian: 2 goc + can giua
    poly(d, [(430, 300), (850, 300), (800, 520), (700, 430), (640, 520),
             (580, 430), (480, 520)], outline=with_alpha(PAPER, A))
    circle(d, 640, 380, 22, fill=with_alpha(AMBER, A))
    circle(d, 500, 360, 14, fill=with_alpha(TEAL, A))
    circle(d, 780, 360, 14, fill=with_alpha(PAPER, A))


def draw_ports(d):
    pad(d, 640, 380, 480, 170)


def draw_megadrive(d):
    rr(d, (420, 310, 860, 450), 50, outline=with_alpha(PAPER, A), width=6)
    x, y = 510, 380
    circle(d, x, y, 30, outline=with_alpha(PAPER, A), width=6)
    line(d, [(x - 30, y), (x + 30, y)], with_alpha(PAPER, A), 5)
    line(d, [(x, y - 30), (x, y + 30)], with_alpha(PAPER, A), 5)
    for i, c in enumerate((AMBER, TEAL, PAPER)):
        circle(d, 700 + i * 48, 380, 17, fill=with_alpha(c, A))


def draw_c64(d):
    # ban phim wedge + luoi phim
    poly(d, [(400, 420), (880, 420), (840, 520), (440, 520)],
         outline=with_alpha(PAPER, A))
    for r in range(3):
        for c in range(10):
            rr(d, (460 + c * 38, 440 + r * 22, 488 + c * 38, 456 + r * 22), 3,
               outline=with_alpha(TEAL, A), width=2)


def draw_atari2600(d):
    line(d, [(640, 500), (640, 240)], with_alpha(PAPER, A), 12)
    circle(d, 640, 210, 40, fill=with_alpha(PAPER, A))
    circle(d, 640, 470, 26, fill=with_alpha(AMBER, A))
    rr(d, (540, 500, 740, 560), 10, outline=with_alpha(PAPER, A), width=5)


def draw_dreamcast(d):
    pad(d, 640, 400, 460, 160)
    rr(d, (580, 300, 700, 360), 8, outline=with_alpha(TEAL, A), width=4)


def draw_nds(d):
    rr(d, (470, 200, 810, 350), 16, outline=with_alpha(PAPER, A), width=5)
    rr(d, (470, 370, 810, 520), 16, outline=with_alpha(PAPER, A), width=5)
    rr(d, (500, 225, 780, 325), 6, outline=with_alpha(TEAL, A), width=3)


def draw_pcengine(d):
    # the HuCARD + tay cam tron
    rr(d, (480, 280, 800, 400), 8, outline=with_alpha(PAPER, A), width=5)
    circle(d, 640, 480, 70, outline=with_alpha(PAPER, A), width=5)
    x, y = 610, 480
    poly(d, [(x - 26, y - 9), (x + 26, y - 9), (x + 26, y + 9),
             (x - 26, y + 9)], fill=with_alpha(TEAL, A))
    poly(d, [(x - 9, y - 26), (x + 9, y - 26), (x + 9, y + 26),
             (x - 9, y + 26)], fill=with_alpha(TEAL, A))
    circle(d, 700, 480, 14, fill=with_alpha(AMBER, A))


DRAW = {
    "fbneo": draw_fbneo, "nes": draw_nes, "snes": draw_snes,
    "psx": draw_psx, "n64": draw_n64, "ports": draw_ports,
    "megadrive": draw_megadrive, "c64": draw_c64,
    "atari2600": draw_atari2600, "dreamcast": draw_dreamcast,
    "nds": draw_nds, "pcengine": draw_pcengine,
    "gba": lambda d: handheld(d, 640, 380, 560, 220),
    "gbc": lambda d: handheld(d, 640, 380, 380, 420),
    "gb": lambda d: handheld(d, 640, 380, 360, 400, screen=False),
    "psp": lambda d: handheld(d, 640, 380, 600, 200),
}

for name, fn in DRAW.items():
    im, d = wm_base()
    fn(d)
    wm_save(im, name)
    print("watermark:", name)
print("icons + watermarks xong")
