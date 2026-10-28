#!/usr/bin/env python3
"""Make ORIGINAL pixel-art PNG/JPG resources for the Shattered PD Rune Knight.
None of the Rune Knight character/splash/icon pixels are copied from upstream art.
Requires Pillow: pip install pillow
"""
from pathlib import Path
import sys, random, math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/runeknight-original-assets')
OUT.mkdir(parents=True, exist_ok=True)
for d in ['sprites','interfaces','splashes']:
    (OUT/d).mkdir(parents=True, exist_ok=True)

INK=(17,24,40,255); SHADOW=(8,17,32,255); SILVER=(196,221,239,255); BLUE=(34,142,209,255); GLOW=(50,238,247,255)

def pixel_character(tier, frame):
    im=Image.new('RGBA',(12,15)); d=ImageDraw.Draw(im)
    # Every tile is hand-constructed. Armor tier affects cloak, helmet, plates and rune glow.
    dark=(23+min(16,tier*2),33+min(20,tier*2),57+min(20,tier*2),255)
    steel=(79+tier*11,104+tier*10,134+tier*9,255)
    fabric=(11,34+min(14,tier*2),71+min(27,tier*3),255)
    cyan=(22,142+min(tier*12,105),185+min(tier*10,70),255)
    phase=0
    if frame in (2,4,6): phase=-1
    if frame in (3,5,7): phase=1
    # back-cape unique shape: sky blue edged mantle, no warrior/rogue silhouette
    d.polygon([(3,6),(9,6),(10,13),(7,12),(3,14),(2,12)],fill=(7,45,81,255),outline=INK)
    d.line([(3,7),(3,12)],fill=cyan)
    if tier>2: d.line([(9,7),(9,12)],fill=cyan)
    # feet are varied in the running animation
    d.rectangle((3+phase,11,5+phase,14),fill=SHADOW)
    d.rectangle((7-phase,11,9-phase,14),fill=SHADOW)
    d.rectangle((3+phase,13,5+phase,14),fill=steel)
    d.rectangle((7-phase,13,9-phase,14),fill=steel)
    # body armor: rune-centred tabard instead of existing hero silhouette
    d.rectangle((3,6,9,11),fill=dark,outline=steel)
    d.polygon([(4,7),(6,6),(8,7),(7,10),(5,10)],fill=fabric)
    d.point((6,8),fill=GLOW)
    d.line([(6,7),(5,8),(6,10),(7,8)],fill=cyan)
    d.rectangle((3,10,9,10),fill=steel)
    # arms and asymmetrical rune pauldron
    d.rectangle((1,6,3,9),fill=dark,outline=INK)
    d.rectangle((9,6,11,9),fill=dark,outline=INK)
    d.rectangle((1,6,3,7),fill=steel)
    d.rectangle((9,6,11,7),fill=cyan if tier>2 else steel)
    d.point((10,7),fill=GLOW)
    # silver hair / carved crown and eyes
    d.rectangle((3,2,8,6),fill=(236,195,169,255),outline=INK)
    d.rectangle((3,1,9,3),fill=steel)
    d.rectangle((4,0,5,2),fill=SILVER)
    d.rectangle((7,1,9,2),fill=SILVER)
    d.point((4,4),fill=(15,109,184,255));d.point((7,4),fill=GLOW)
    d.line([(3,3),(3,6)],fill=dark)
    if tier>1: d.line([(4,1),(8,1)],fill=cyan)
    if tier>4:
        d.point((6,0),fill=GLOW); d.point((1,5),fill=cyan)
    if frame in (0,1):
        if frame==1:d.point((6,8),fill=(245,252,255,255))
    elif frame in (2,3,4,5,6,7):
        d.point((1,11 if frame%2 else 10),fill=cyan)
    elif frame in (8,9,10,11,12):
        # unique falling / collapse sequence
        im=im.rotate((frame-8)*16, resample=Image.Resampling.NEAREST,expand=False)
        faded=Image.new('RGBA',(12,15), (10,20,36, int((frame-8)*40)))
        im=Image.alpha_composite(im,faded)
        return im
    elif frame in (13,14,15):
        # rune blade on attack frames. Impact slash is drawn per frame.
        d.line([(9,7),(11,2 if frame==13 else 3)],fill=(12,39,74,255),width=2)
        d.line([(9,6),(11,2 if frame==13 else 3)],fill=GLOW)
        d.point((11,1 if frame==13 else 4),fill=(218,252,255,255))
        if frame==15: d.arc((0,-1,11,10),170,325,fill=GLOW,width=1)
    elif frame in (16,17):
        d.ellipse((2,6,10,13),outline=GLOW,width=1)
        d.point((6,11),fill=(255,255,255,255))
    elif frame ==18:
        d.line([(0,12),(11,12)], fill=GLOW)
    elif frame in (19,20):
        d.rectangle((4,9,8,11),fill=(225,241,251,255),outline=BLUE)
        d.point((6,10),fill=BLUE)
    return im

# Match the upstream 256x128 hero atlas, preserving 21x7 original frames.
atlas=Image.new('RGBA',(256,128))
for tier in range(7):
    for frame in range(21):
        atlas.alpha_composite(pixel_character(tier,frame),(frame*12,tier*15))
atlas.save(OUT/'sprites/runeknight.png')

# Custom icons in a standalone atlas, all individually drawn (not taken from game art).
def icon_back():
    x=Image.new('RGBA',(16,16));d=ImageDraw.Draw(x)
    d.rounded_rectangle((1,1,14,14),radius=3,fill=(13,29,58,255),outline=(45,117,167,255))
    return x

def runic_icon(kind):
    im=icon_back(); d=ImageDraw.Draw(im)
    if kind==0: # rune edge
        d.line([(4,13),(11,3)],fill=(200,240,255,255),width=3)
        d.line([(4,13),(11,3)],fill=GLOW,width=1)
        d.line([(3,10),(7,12)],fill=BLUE,width=2)
        d.point((12,2),fill=(255,255,255,255))
    if kind==1: # ward
        d.polygon([(8,2),(13,5),(12,11),(8,14),(4,11),(3,5)],fill=(24,69,116,255),outline=GLOW)
        d.line([(8,4),(8,11),(5,8),(11,8)],fill=(224,254,254,255))
    if kind==2: # mastery
        d.ellipse((3,3,12,12),outline=GLOW,width=2)
        d.line([(8,2),(8,13),(2,8),(13,8)],fill=BLUE)
        d.rectangle((6,6,9,9),fill=(236,254,255,255))
    if kind==3: # recovery
        d.arc((2,2,13,13),30,300,fill=GLOW,width=2)
        d.polygon([(12,2),(13,7),(9,6)],fill=(222,250,255,255))
        d.point((8,8),fill=BLUE)
    return im
icons=Image.new('RGBA',(16*4,16))
for i in range(4): icons.alpha_composite(runic_icon(i),(16*i,0))
icons.save(OUT/'interfaces/runeknight_talents.png')

# One-off energy crest for the special focus (at item tile 16x16).
focus=Image.new('RGBA',(16,16));d=ImageDraw.Draw(focus)
d.ellipse((2,2,13,13),outline=(11,71,125,255),width=2)
d.ellipse((4,4,11,11),outline=GLOW)
d.polygon([(8,1),(12,8),(8,14),(4,8)],fill=(32,118,182,255),outline=SILVER)
d.line([(8,3),(8,12)],fill=GLOW)
d.point((8,7),fill=(255,255,255,255))
focus.save(OUT/'sprites/runic_focus.png')

# Independent concept art for selected character, without use of existing splash.
S=Image.new('RGB',(800,450),(7,14,28));d=ImageDraw.Draw(S)
rng=random.Random(2411)
for x in range(0,800,24):
    for y in range(0,450,24):
        d.rectangle((x,y,x+22,y+22),fill=(12+rng.randint(0,8),19+rng.randint(0,8),34+rng.randint(0,9)))
        d.line((x,y,x+21,y),fill=(26,42,62),width=2)
# room pillars
for x in [45,235,680,756]:
    d.rectangle((x,36,x+38,405),fill=(21,35,54),outline=(49,73,94),width=4)
    for y in range(52,400,35): d.line((x,y,x+38,y),fill=(11,22,39),width=3)
# round floor rune and magical sigils
cx,cy=498,350
for rr in [45,70,105]:d.ellipse((cx-rr,cy-rr//3,cx+rr,cy+rr//3),outline=(17,112+rr//2,165+rr//4),width=3)
for k in range(12):
    a=k*math.tau/12
    xx=int(cx+100*math.cos(a)); yy=int(cy+32*math.sin(a))
    d.line((xx-4,yy,xx+4,yy),fill=(27,206,231),width=2)
# Render from our own sprite atlas with nearest-neighbor scaling (same original source, no old art).
char=pixel_character(6,0).resize((216,270),resample=Image.Resampling.NEAREST)
S.paste(char,(388,102),char)
# another fresh art overlay blade, spells
for i in range(15):
    a=i*math.tau/15
    x=int(495+150*math.cos(a));y=int(234+115*math.sin(a))
    if 60<x<740 and 50<y<380:
        d.line((x-2,y,x+2,y),fill=(40,151,221),width=2)
for rr in [132,137]:d.arc((350-rr//2,110,700,410),190,325,fill=(32,191,244),width=3)
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',46)
except OSError:font=ImageFont.load_default()
d.text((62,355),'RUNE KNIGHT',font=font,fill=(123,225,245),stroke_width=2,stroke_fill=(0,22,47))
S.save(OUT/'splashes/runeknight.jpg',quality=94,subsampling=0)

# subclass icons generated separately, even when game logic takes another iteration.
sub=Image.new('RGBA',(32,16))
for i in range(2):
    z=icon_back();draw=ImageDraw.Draw(z)
    if i==0:
        draw.polygon([(8,1),(13,6),(12,12),(8,14),(4,12),(3,6)],fill=BLUE,outline=SILVER)
        draw.line([(8,3),(8,12)],fill=GLOW)
    else:
        draw.line([(3,12),(12,3)],fill=GLOW,width=3)
        draw.line([(4,3),(12,12)],fill=BLUE,width=3)
    sub.alpha_composite(z,(16*i,0))
sub.save(OUT/'interfaces/runeknight_subclasses.png')

# Preview intentionally uses only new pixels, for inspection of real game assets.
preview=Image.new('RGB',(1080,525),(12,20,33));draw=ImageDraw.Draw(preview)
try: title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',25)
except OSError:title=ImageFont.load_default()
for text,y in [('RUNE KNIGHT - ORIGINAL IN-GAME SPRITES',18),('7 armor tiers | 21 frames per tier (idle, run, death, attack, cast, fly, read)',65),('Original talent icons / Rune Focus',320)]:
    draw.text((32,y),text,fill=(182,228,248),font=title)
preview.paste(atlas.crop((0,0,252,105)).resize((1008,420),resample=Image.Resampling.NEAREST).crop((0,0,1008,220)),(30,102),atlas.crop((0,0,252,105)).resize((1008,420),resample=Image.Resampling.NEAREST).crop((0,0,1008,220)))
preview.paste(icons.resize((384,96),resample=Image.Resampling.NEAREST),(32,363),icons.resize((384,96),resample=Image.Resampling.NEAREST))
preview.paste(focus.resize((96,96),resample=Image.Resampling.NEAREST),(474,365),focus.resize((96,96),resample=Image.Resampling.NEAREST))
preview.save(OUT/'runeknight-assets-preview.png')
print('Original sprite atlas:',atlas.size)
print('Files:')
for f in OUT.rglob('*'):
    if f.is_file():print(f.relative_to(OUT), f.stat().st_size)

# Complete dedicated talent atlas: 17 new T1/T2/T3 talents + 10 distinct
# Rune Knight re-interpretation icons for its tier-four techniques.
alltalents=Image.new('RGBA',(16*27,16))
for ix in range(27):
    p=runic_icon(ix%4).copy()
    ink=ImageDraw.Draw(p)
    # Each design gets its own sigil/corner marks, not shared pixel art with other jobs.
    tone=[(251,190,91,255),(58,234,243,255),(173,125,253,255),(247,246,255,255)][ix%4]
    for k in range(1+(ix//4)%3):
        x=(2+ix*3+k*4)%14+1; y=(2+ix*5+k*3)%14+1
        ink.point((x,y),fill=tone)
    if ix>=4:
        ink.line([(2+ix%5,2),(13,13-ix%6)],fill=tone)
        if ix%3==0:ink.ellipse((4,5,10,11),outline=GLOW)
        if ix%3==1:ink.polygon([(8,3),(12,8),(8,13),(4,8)],outline=tone)
        if ix%3==2:ink.line([(2,8),(13,8)],fill=tone)
    alltalents.alpha_composite(p,(16*ix,0))
alltalents.save(OUT/'interfaces/runeknight_talents.png')

abilities=Image.new('RGBA',(16*3,16))
for i in range(3):
    im=icon_back();dr=ImageDraw.Draw(im)
    if i==0:
        dr.polygon([(7,1),(13,8),(8,14),(3,8)],fill=(20,95,175,255),outline=GLOW)
        dr.line([(8,3),(8,11)],fill=SILVER)
    elif i==1:
        for r in [2,5,8]:dr.arc((8-r,8-r,8+r,8+r),10,165,fill=GLOW)
        dr.line([(2,11),(13,5)],fill=SILVER,width=2)
    else:
        dr.ellipse((2,2,13,13),outline=GLOW)
        dr.polygon([(8,2),(13,8),(8,13),(3,8)],outline=SILVER)
    abilities.alpha_composite(im,(16*i,0))
abilities.save(OUT/'interfaces/runeknight_abilities.png')

armor_icon=Image.new('RGBA',(16,16));dr=ImageDraw.Draw(armor_icon)
dr.polygon([(3,2),(6,1),(10,1),(13,2),(14,7),(12,8),(12,14),(4,14),(4,8),(2,7)],fill=(19,46,89,255),outline=SILVER)
dr.polygon([(5,4),(11,4),(10,11),(8,13),(6,11)],fill=(25,92,168,255),outline=GLOW)
dr.line([(8,4),(8,11),(6,8),(10,8)],fill=SILVER)
armor_icon.save(OUT/'sprites/runeknight_armor.png')
print('Updated original custom talent sheet:', alltalents.size, 'armor icon & ability icons made')