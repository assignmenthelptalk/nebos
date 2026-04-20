"""Generate 1200×420 WebP header images for NEBOSH Phase 2B pages."""
from PIL import Image, ImageDraw, ImageFilter
import os

INPUT = r"c:\Users\jobmu\agentic-workflow\semantic-seo-workflow\client_data\New-sites\nebosh-assignment-help\input-images"
OUTPUT = r"c:\Users\jobmu\my-second-projects\nebosh-assignment-help\public"

BRAND_BLUE  = (27, 58, 107)       # #1B3A6B
BRAND_GOLD  = (201, 168, 76)      # #C9A84C
WHITE       = (255, 255, 255)
W, H        = 1200, 420

pages = [
    {
        "slug":  "nebosh-fire-certificate-assignment-help",
        "photo": "Screenshot_24.png",          # classroom / training
        "line1": "NEBOSH Fire Certificate",
        "line2": "Assignment Help",
        "line3": "FC1 OBE · FC2 Fire Risk Assessment",
    },
    {
        "slug":  "nebosh-environmental-certificate-assignment-help",
        "photo": "Screenshot_25.png",          # group study
        "line1": "NEBOSH Environmental",
        "line2": "Certificate Assignment Help",
        "line3": "EC1 OBE · Practical Assessment · ISO 14001",
    },
    {
        "slug":  "nebosh-construction-certificate-assignment-help",
        "photo": "Screenshot_26.png",          # hi-vis site workers
        "line1": "NEBOSH Construction",
        "line2": "Certificate Assignment Help",
        "line3": "NC1 OBE · NC2 Site Risk Assessment · CDM 2015",
    },
    {
        "slug":  "nebosh-obe-sample-questions-worked-answers",
        "photo": "Screenshot_30.png",          # student studying
        "line1": "NEBOSH OBE",
        "line2": "Sample Questions",
        "line3": "Worked Answers at Pass & Distinction Level",
    },
    {
        "slug":  "nebosh-examiner-reports-analysis",
        "photo": "Screenshot_27.png",          # students at computers
        "line1": "NEBOSH Examiner",
        "line2": "Reports Analysis",
        "line3": "Recurring Patterns · Marking Intelligence",
    },
]

def make_header(cfg):
    canvas = Image.new("RGB", (W, H), BRAND_BLUE)
    draw   = ImageDraw.Draw(canvas)

    # ── right-side photo (takes up right ~45% of canvas) ──────────
    photo_path = os.path.join(INPUT, cfg["photo"])
    photo = Image.open(photo_path).convert("RGB")

    panel_x = int(W * 0.54)
    panel_w = W - panel_x
    panel_h = H

    # Scale photo to fill the panel (cover crop)
    photo_ratio = photo.width / photo.height
    panel_ratio = panel_w / panel_h
    if photo_ratio > panel_ratio:
        new_h = panel_h
        new_w = int(photo_ratio * new_h)
    else:
        new_w = panel_w
        new_h = int(new_w / photo_ratio)
    photo = photo.resize((new_w, new_h), Image.LANCZOS)
    # Centre-crop
    left = (new_w - panel_w) // 2
    top  = (new_h - panel_h) // 2
    photo = photo.crop((left, top, left + panel_w, top + panel_h))

    # Darken the photo slightly for contrast
    darkener = Image.new("RGB", photo.size, (0, 0, 0))
    photo = Image.blend(photo, darkener, 0.25)

    canvas.paste(photo, (panel_x, 0))

    # ── gradient fade from blue into photo ────────────────────────
    fade_w = 120
    for i in range(fade_w):
        alpha = int(255 * (1 - i / fade_w))
        draw.line([(panel_x + i, 0), (panel_x + i, H)],
                  fill=(*BRAND_BLUE, alpha))

    # ── gold accent bar top ───────────────────────────────────────
    draw.rectangle([0, 0, panel_x + fade_w, 6], fill=BRAND_GOLD)

    # ── gold accent bar bottom ────────────────────────────────────
    draw.rectangle([0, H - 6, W, H], fill=BRAND_GOLD)

    # ── text area ─────────────────────────────────────────────────
    # We'll use default PIL font (no external fonts needed)
    # For better sizing we use truetype if available, else fall back
    try:
        from PIL import ImageFont
        # Try a system font
        for candidate in [
            "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]:
            try:
                font_large  = ImageFont.truetype(candidate, 52)
                font_medium = ImageFont.truetype(candidate, 44)
                font_small  = ImageFont.truetype(candidate.replace("bd","").replace("Bold","").replace("bold","").replace("b.ttf",".ttf"), 20)
                break
            except Exception:
                font_large = font_medium = font_small = ImageFont.load_default()
    except Exception:
        font_large = font_medium = font_small = ImageFont.load_default()

    text_x    = 52
    text_area = panel_x - 20  # max text width

    # Line 1 – brand line (gold, large)
    draw.text((text_x, 100), cfg["line1"], font=font_large, fill=BRAND_GOLD)
    # Line 2 – page title (white, large)
    draw.text((text_x, 162), cfg["line2"], font=font_medium, fill=WHITE)
    # Thin gold rule
    draw.rectangle([text_x, 226, text_x + 300, 230], fill=BRAND_GOLD)
    # Line 3 – sub-label (light blue-white, small)
    draw.text((text_x, 248), cfg["line3"], font=font_small, fill=(180, 200, 230))
    # Domain watermark bottom-left
    draw.text((text_x, H - 38), "nebosh-assignment-help.co.uk",
              font=font_small, fill=(120, 150, 190))

    out_path = os.path.join(OUTPUT, f"header_{cfg['slug']}.webp")
    canvas.save(out_path, "WEBP", quality=88)
    print(f"  OK  {out_path}")

for p in pages:
    make_header(p)

print("All headers generated.")
