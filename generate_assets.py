#!/usr/bin/env python3
"""Generate soccer field background and pixel-art player sprites."""

from PIL import Image, ImageDraw
import json, math, os

BASE = 'futbolagents-ui/public/assets'
FW, FH = 32, 48  # sprite frame size

# ── colours ──────────────────────────────────────────────────────────────
SKIN       = (220, 175, 130)
SOCKS_W    = (245, 245, 245)
CLEAT      = (40, 30, 20)
HAIR_DARK  = (35, 22, 10)
HAIR_BLOND = (200, 168, 72)
HAIR_BROWN = (110, 60, 30)
HAIR_GREY  = (160, 145, 135)

def lerp(a, b, t):
    return tuple(max(0, min(255, int(a[i] + (b[i]-a[i])*t))) for i in range(3))

# ── sprite drawing ────────────────────────────────────────────────────────
def draw_front(d, jersey, shorts, hair, skin, female, phase):
    cx = FW // 2
    leg = int(math.sin(phase) * 3)
    arm = -int(math.sin(phase) * 2)

    # head
    d.ellipse([cx-5, 2, cx+4, 12], fill=skin)
    d.ellipse([cx-5, 2, cx+4, 6],  fill=hair)
    if female:
        d.rectangle([cx-6, 5, cx-4, 12], fill=hair)
        d.rectangle([cx+4, 5, cx+6, 12], fill=hair)
    d.point([cx-2, 7], fill=(40,25,15))
    d.point([cx+2, 7], fill=(40,25,15))
    d.line([cx-2, 10, cx+1, 10], fill=lerp(skin,(120,60,50),0.5))

    # neck
    d.rectangle([cx-1, 12, cx+1, 14], fill=skin)

    # jersey + collar
    d.rectangle([cx-6, 14, cx+5, 25], fill=jersey)
    d.rectangle([cx-2, 14, cx+1, 16], fill=lerp(jersey,(0,0,0),0.25))

    # arms + hands
    d.rectangle([cx-9+arm,  15, cx-5+arm,  23], fill=jersey)
    d.rectangle([cx+5-arm,  15, cx+9-arm,  23], fill=jersey)
    d.ellipse  ([cx-10+arm, 22, cx-5+arm,  26], fill=skin)
    d.ellipse  ([cx+5-arm,  22, cx+10-arm, 26], fill=skin)

    # shorts
    d.rectangle([cx-6, 25, cx+5, 32], fill=shorts)

    # socks
    lx, rx = cx-4, cx+3
    d.rectangle([lx-1, 32, lx+2, 41], fill=SOCKS_W)
    d.rectangle([rx-1, 32, rx+2, 41], fill=SOCKS_W)

    # cleats with leg swing
    fl, fr = lx-1+leg, rx-1-leg
    d.rectangle([fl, 41, fl+4, 46], fill=CLEAT)
    d.rectangle([fr, 41, fr+4, 46], fill=CLEAT)


def draw_back(d, jersey, shorts, hair, skin, female, phase):
    cx = FW // 2
    leg = int(math.sin(phase) * 3)
    arm = -int(math.sin(phase) * 2)

    # head (hair only)
    d.ellipse([cx-5, 2, cx+4, 12], fill=hair)
    if female:
        d.rectangle([cx-6, 5, cx-4, 14], fill=hair)
        d.rectangle([cx+4, 5, cx+6, 14], fill=hair)
    d.rectangle([cx-1, 12, cx+1, 14], fill=skin)

    # jersey + number hint
    d.rectangle([cx-6, 14, cx+5, 25], fill=jersey)
    d.rectangle([cx-3, 17, cx+2, 22], fill=lerp(jersey,(255,255,255),0.65))
    d.rectangle([cx-9+arm, 15, cx-5+arm, 23], fill=jersey)
    d.rectangle([cx+5-arm, 15, cx+9-arm, 23], fill=jersey)
    d.ellipse  ([cx-10+arm, 22, cx-5+arm, 26], fill=skin)
    d.ellipse  ([cx+5-arm,  22, cx+10-arm,26], fill=skin)

    d.rectangle([cx-6, 25, cx+5, 32], fill=shorts)

    lx, rx = cx-4, cx+3
    d.rectangle([lx-1, 32, lx+2, 41], fill=SOCKS_W)
    d.rectangle([rx-1, 32, rx+2, 41], fill=SOCKS_W)
    fl, fr = lx-1+leg, rx-1-leg
    d.rectangle([fl, 41, fl+4, 46], fill=CLEAT)
    d.rectangle([fr, 41, fr+4, 46], fill=CLEAT)


def draw_side(d, jersey, shorts, hair, skin, female, phase, facing_right):
    cx   = FW // 2
    dx   = 2 if facing_right else -2
    x    = cx + dx
    leg  = int(math.sin(phase) * 4)

    # head
    if facing_right:
        d.ellipse([x-4, 2, x+5, 12], fill=skin)
        d.ellipse([x-4, 2, x+1,  6], fill=hair)
        d.point([x+4, 7], fill=(40,25,15))
        if female: d.rectangle([x-5, 4, x-3, 12], fill=hair)
    else:
        d.ellipse([x-5, 2, x+4, 12], fill=skin)
        d.ellipse([x-1, 2, x+4,  6], fill=hair)
        d.point([x-4, 7], fill=(40,25,15))
        if female: d.rectangle([x+3, 4, x+5, 12], fill=hair)

    d.rectangle([x-1, 12, x+1, 14], fill=skin)

    # jersey
    d.rectangle([x-4, 14, x+3, 25], fill=jersey)
    off = 3 if facing_right else -3
    d.rectangle([x+off-1, 15, x+off+1, 23], fill=jersey)
    d.ellipse  ([x+off-2, 22, x+off+2, 26], fill=skin)

    d.rectangle([x-4, 25, x+3, 32], fill=shorts)

    # legs (back leg slightly muted)
    bl = lerp(SOCKS_W,(180,180,180),0.35)
    d.rectangle([x-1, 32, x+2, 41], fill=bl)
    bf = x-1 + (-leg//2 if facing_right else leg//2)
    d.rectangle([bf, 41, bf+4, 46], fill=lerp(CLEAT,(0,0,0),0.3))

    d.rectangle([x-1, 32, x+2, 41], fill=SOCKS_W)
    fo = leg if facing_right else -leg
    ff = x-1+fo
    d.rectangle([ff, 41, ff+4, 46], fill=CLEAT)


def make_spritesheet(pid, colors):
    DIRS = ['back','front','left','right']
    FRAMES = 10   # 1 idle + 9 walk
    sheet  = Image.new('RGBA', (FW*FRAMES, FH*len(DIRS)), (0,0,0,0))
    atlas  = {}
    jersey = colors['jersey']
    shorts = colors['shorts']
    hair   = colors['hair']
    female = colors.get('female', False)
    skin   = colors.get('skin', SKIN)

    for ri, direction in enumerate(DIRS):
        for fi in range(FRAMES):
            phase = 0.0 if fi == 0 else (fi/9.0)*2*math.pi
            frame = Image.new('RGBA', (FW, FH), (0,0,0,0))
            d = ImageDraw.Draw(frame)

            if   direction == 'front': draw_front(d, jersey, shorts, hair, skin, female, phase)
            elif direction == 'back':  draw_back (d, jersey, shorts, hair, skin, female, phase)
            elif direction == 'left':  draw_side (d, jersey, shorts, hair, skin, female, phase, False)
            elif direction == 'right': draw_side (d, jersey, shorts, hair, skin, female, phase, True)

            x, y = fi*FW, ri*FH
            sheet.paste(frame, (x, y))

            key = f'{pid}-{direction}' if fi==0 else f'{pid}-{direction}-walk-{(fi-1):04d}'
            atlas[key] = {
                'frame':           {'x':x, 'y':y, 'w':FW, 'h':FH},
                'rotated':         False,
                'trimmed':         False,
                'spriteSourceSize':{'x':0, 'y':0, 'w':FW, 'h':FH},
                'sourceSize':      {'w':FW, 'h':FH}
            }

    return sheet, atlas


def save_character(pid, colors):
    char_dir = f'{BASE}/characters/{pid}'
    os.makedirs(char_dir, exist_ok=True)
    sheet, atlas_frames = make_spritesheet(pid, colors)
    sheet.save(f'{char_dir}/atlas.png', 'PNG')
    with open(f'{char_dir}/atlas.json', 'w') as f:
        json.dump({
            'frames': atlas_frames,
            'meta':   {'image':'atlas.png','scale':'1','size':{'w':FW*10,'h':FH*4}}
        }, f, indent=2)
    print(f'  ✓ {pid}')


# ── soccer field image ────────────────────────────────────────────────────
def generate_field():
    W, H   = 1280, 1280
    img    = Image.new('RGB', (W,H), (38, 98, 42))   # OOB dark green
    d      = ImageDraw.Draw(img)

    FL,FT  = 80, 110
    FR,FB  = 1200, 1170
    CX     = (FL+FR)//2   # 640
    CY     = (FT+FB)//2   # 640

    G1 = (62, 168, 78)    # lighter stripe
    G2 = (54, 150, 68)    # darker stripe
    WHITE  = (255,255,255)
    LW     = 3

    # alternating horizontal grass stripes
    STRIPES = 8
    bh = (FB-FT)//STRIPES
    for i in range(STRIPES):
        ys = FT + i*bh
        ye = ys + bh if i < STRIPES-1 else FB
        d.rectangle([FL, ys, FR, ye], fill=(G1 if i%2==0 else G2))

    PA_W, PA_H = 185, 440   # penalty area
    GA_W, GA_H = 78, 230    # goal area
    PS_D       = 160        # penalty spot dist from end line
    R_CC       = 105        # center circle radius
    R_COR      = 32         # corner arc radius

    # left penalty area
    d.rectangle([FL, CY-PA_H//2, FL+PA_W, CY+PA_H//2], outline=WHITE, width=LW)
    # left goal area
    d.rectangle([FL, CY-GA_H//2, FL+GA_W, CY+GA_H//2], outline=WHITE, width=LW)
    # left penalty spot
    ps_lx = FL + PS_D
    d.ellipse([ps_lx-4, CY-4, ps_lx+4, CY+4], fill=WHITE)

    # right penalty area
    d.rectangle([FR-PA_W, CY-PA_H//2, FR, CY+PA_H//2], outline=WHITE, width=LW)
    # right goal area
    d.rectangle([FR-GA_W, CY-GA_H//2, FR, CY+GA_H//2], outline=WHITE, width=LW)
    # right penalty spot
    ps_rx = FR - PS_D
    d.ellipse([ps_rx-4, CY-4, ps_rx+4, CY+4], fill=WHITE)

    # halfway line (vertical)
    d.line([CX, FT, CX, FB], fill=WHITE, width=LW)

    # centre circle + spot
    d.ellipse([CX-R_CC, CY-R_CC, CX+R_CC, CY+R_CC], outline=WHITE, width=LW)
    d.ellipse([CX-5,    CY-5,    CX+5,    CY+5   ], fill=WHITE)

    # field boundary (on top of grass, over stripes)
    d.rectangle([FL, FT, FR, FB], outline=WHITE, width=LW)

    # corner arcs (inside field)
    d.arc([FL-R_COR, FT-R_COR, FL+R_COR, FT+R_COR],   0,  90, fill=WHITE, width=LW)
    d.arc([FR-R_COR, FT-R_COR, FR+R_COR, FT+R_COR],  90, 180, fill=WHITE, width=LW)
    d.arc([FL-R_COR, FB-R_COR, FL+R_COR, FB+R_COR], 270, 360, fill=WHITE, width=LW)
    d.arc([FR-R_COR, FB-R_COR, FR+R_COR, FB+R_COR], 180, 270, fill=WHITE, width=LW)

    # goals (thick coloured posts on end lines)
    GH = 185
    goal_color = (230, 230, 230)
    d.rectangle([FL-10, CY-GH//2, FL,    CY+GH//2], fill=goal_color)
    d.rectangle([FR,    CY-GH//2, FR+10, CY+GH//2], fill=goal_color)

    out = f'{BASE}/soccer-field.jpg'
    img.save(out, 'JPEG', quality=95)
    print(f'  ✓ soccer-field.jpg  ({W}×{H})')


# ── player catalogue ──────────────────────────────────────────────────────
PLAYERS = {
    # id             jersey               shorts              hair          female
    'maradona':    {'jersey':(108,166,205),'shorts':(40,40,120),  'hair':HAIR_DARK },
    'cruyff':      {'jersey':(255,130,  0),'shorts':(255,255,255),'hair':HAIR_DARK },
    'pele':        {'jersey':(246,213, 23),'shorts':( 24,107, 48),'hair':HAIR_DARK },
    'ronaldo':     {'jersey':(246,213, 23),'shorts':( 24,107, 48),'hair':HAIR_DARK,'skin':(190,140,100)},
    'suarez':      {'jersey':( 91,190,226),'shorts':( 20, 20, 20),'hair':HAIR_DARK },
    'forlan':      {'jersey':( 91,190,226),'shorts':( 30, 30, 30),'hair':HAIR_BLOND},
    'beckenbauer': {'jersey':(240,240,240),'shorts':( 30, 30, 30),'hair':HAIR_BLOND},
    'di_stefano':  {'jersey':(255,255,255),'shorts':( 20, 20, 20),'hair':HAIR_GREY },
    'puskas':      {'jersey':(200, 30, 30),'shorts':(255,255,255),'hair':HAIR_DARK },
    'garrincha':   {'jersey':(246,213, 23),'shorts':( 24,107, 48),'hair':HAIR_DARK,'skin':(185,135, 95)},
    'miguel':      {'jersey':(200, 50, 50),'shorts':( 30, 30, 30),'hair':HAIR_DARK },
    'paul':        {'jersey':( 30, 80,200),'shorts':(255,255,255),'hair':HAIR_BROWN},
    'sophia':      {'jersey':(220, 60,160),'shorts':(255,255,255),'hair':HAIR_BROWN,'female':True},
}

if __name__ == '__main__':
    print('\n=== Generating soccer field ===')
    generate_field()

    print('\n=== Generating player sprites ===')
    for pid, colors in PLAYERS.items():
        save_character(pid, colors)

    print('\nAll assets generated!')
