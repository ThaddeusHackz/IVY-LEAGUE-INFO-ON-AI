#!/usr/bin/env python3
"""
Generate professional Ivy League university shield logos and AI company logos
using PIL for use in the 30 PDF documents.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

LOGO_DIR = "/home/user/IVY-LEAGUE-INFO-ON-AI/logos"
os.makedirs(LOGO_DIR, exist_ok=True)

def draw_shield(draw, cx, cy, w, h, fill_color, outline_color, outline_width=3):
    """Draw a classic heraldic shield shape."""
    points = []
    # Top left
    points.append((cx - w//2, cy - h//3))
    # Top right
    points.append((cx + w//2, cy - h//3))
    # Right side curves down
    for i in range(20):
        angle = math.pi/2 * i / 19
        x = cx + w//2 * math.cos(angle)
        y = cy - h//3 + (h*2//3) * (1 - math.cos(angle)) * 0.5 + (h//2) * (i/19)
        points.append((int(x), int(y)))
    # Bottom point
    points.append((cx, cy + h//2))
    # Left side curves up
    for i in range(19, -1, -1):
        angle = math.pi/2 * i / 19
        x = cx - w//2 * math.cos(angle)
        y = cy - h//3 + (h*2//3) * (1 - math.cos(angle)) * 0.5 + (h//2) * (i/19)
        points.append((int(x), int(y)))
    draw.polygon(points, fill=fill_color, outline=outline_color, width=outline_width)
    return points

def draw_book(draw, cx, cy, w, h, color="white"):
    """Draw an open book symbol."""
    # Left page
    draw.polygon([(cx-w//4, cy-h//4), (cx, cy-h//6), (cx, cy+h//4), (cx-w//4, cy+h//4)], fill=color)
    # Right page
    draw.polygon([(cx+w//4, cy-h//4), (cx, cy-h//6), (cx, cy+h//4), (cx+w//4, cy+h//4)], fill=color)
    # Spine
    draw.line([(cx, cy-h//6), (cx, cy+h//4)], fill="black", width=2)

def draw_star(draw, cx, cy, r, color="white", points=5):
    """Draw a star shape."""
    star_points = []
    for i in range(points * 2):
        angle = math.pi * i / points - math.pi / 2
        radius = r if i % 2 == 0 else r * 0.4
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        star_points.append((int(x), int(y)))
    draw.polygon(star_points, fill=color)

def draw_torch(draw, cx, cy, color="gold"):
    """Draw a torch symbol."""
    # Handle
    draw.rectangle([cx-3, cy-5, cx+3, cy+30], fill="#8B4513")
    # Flame
    draw.ellipse([cx-10, cy-25, cx+10, cy-5], fill=color)
    draw.ellipse([cx-6, cy-30, cx+6, cy-15], fill="#FFD700")

def add_text(img, text, y, size=28, color="white", bold=True):
    """Add text to image center."""
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (img.width - tw) // 2
    draw.text((x, y), text, fill=color, font=font)
    return draw

def create_logo(name, primary_color, secondary_color, symbol_func=None, motto="", bg_color=None):
    """Create a university logo."""
    size = 400
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw shield
    cx, cy = size//2, size//2 - 20
    draw_shield(draw, cx, cy, 260, 280, primary_color, secondary_color, 4)

    # Draw inner shield
    draw_shield(draw, cx, cy, 230, 250, bg_color or primary_color, secondary_color, 2)

    # Draw symbol
    if symbol_func:
        symbol_func(draw, cx, cy - 30)

    # University name
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font = ImageFont.load_default()
        font_sm = font

    bbox = draw.textbbox((0, 0), name.upper(), font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw)//2, size - 80), name.upper(), fill=secondary_color, font=font)

    if motto:
        bbox2 = draw.textbbox((0, 0), motto, font=font_sm)
        tw2 = bbox2[2] - bbox2[0]
        draw.text(((size - tw2)//2, size - 55), motto, fill=secondary_color, font=font_sm)

    return img

def create_openai_logo():
    """Create OpenAI-style logo."""
    size = 400
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size//2, size//2 - 20
    # Hexagonal frame
    hex_points = []
    for i in range(6):
        angle = math.pi/3 * i - math.pi/6
        x = cx + 120 * math.cos(angle)
        y = cy + 120 * math.sin(angle)
        hex_points.append((int(x), int(y)))
    draw.polygon(hex_points, fill="#412991", outline="#7B68EE", width=3)

    # Inner hexagon
    inner_hex = []
    for i in range(6):
        angle = math.pi/3 * i - math.pi/6
        x = cx + 100 * math.cos(angle)
        y = cy + 100 * math.sin(angle)
        inner_hex.append((int(x), int(y)))
    draw.polygon(inner_hex, fill="#1a1a2e", outline="#7B68EE", width=2)

    # Stylized neural network / circuit pattern
    # Central node
    draw.ellipse([cx-15, cy-15, cx+15, cy+15], fill="#10a37f")
    # Surrounding nodes
    for i in range(6):
        angle = math.pi/3 * i
        nx = cx + 55 * math.cos(angle)
        ny = cy + 55 * math.sin(angle)
        draw.ellipse([nx-10, ny-10, nx+10, ny+10], fill="#7B68EE")
        draw.line([(cx, cy), (int(nx), int(ny))], fill="#10a37f", width=2)

    # OPENAI text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_sub = font

    bbox = draw.textbbox((0, 0), "OpenAI", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw)//2, size - 75), "OpenAI", fill="#10a37f", font=font)

    bbox2 = draw.textbbox((0, 0), "Artificial Intelligence", font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((size - tw2)//2, size - 50), "Artificial Intelligence", fill="#7B68EE", font=font_sub)

    return img

def create_anthropic_logo():
    """Create Anthropic/Claude-style logo."""
    size = 400
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size//2, size//2 - 20

    # Circle frame
    draw.ellipse([cx-130, cy-130, cx+130, cy+130], fill="#d4a574", outline="#c4956a", width=3)
    draw.ellipse([cx-110, cy-110, cx+110, cy+110], fill="#2d1810", outline="#d4a574", width=2)

    # Starburst / asterisk pattern (Anthropic style)
    for i in range(8):
        angle = math.pi/4 * i
        x1 = cx + 25 * math.cos(angle)
        y1 = cy + 25 * math.sin(angle)
        x2 = cx + 65 * math.cos(angle)
        y2 = cy + 65 * math.sin(angle)
        draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill="#d4a574", width=4)

    # Central dot
    draw.ellipse([cx-18, cy-18, cx+18, cy+18], fill="#d4a574")

    # Text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_sub = font

    bbox = draw.textbbox((0, 0), "ANTHROPIC", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((size - tw)//2, size - 75), "ANTHROPIC", fill="#d4a574", font=font)

    bbox2 = draw.textbbox((0, 0), "AI Safety Research", font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((size - tw2)//2, size - 50), "AI Safety Research", fill="#c4956a", font=font_sub)

    return img


# Ivy League universities
universities = [
    ("Harvard", "#A51C30", "#C9A87C", "#7B2D26"),
    ("Yale", "#00356B", "#FFFFFF", "#00274C"),
    ("Princeton", "#E77500", "#000000", "#100D09"),
    ("Columbia", "#B9D9EB", "#FFFFFF", "#003DA5"),
    ("UPenn", "#011F5B", "#FFFFFF", "#990000"),
    ("Brown", "#4E3629", "#FFFFFF", "#ED1C24"),
    ("Dartmouth", "#00693E", "#FFFFFF", "#003D1E"),
    ("Cornell", "#B31B1B", "#FFFFFF", "#222222"),
]

def draw_book_symbol(draw, cx, cy, color="white"):
    draw.polygon([(cx-30, cy-20), (cx, cy-10), (cx, cy+25), (cx-30, cy+25)], fill=color, outline="black", width=1)
    draw.polygon([(cx+30, cy-20), (cx, cy-10), (cx, cy+25), (cx+30, cy+25)], fill=color, outline="black", width=1)
    draw.line([(cx, cy-10), (cx, cy+25)], fill="black", width=2)

def draw_open_book(draw, cx, cy):
    draw_book_symbol(draw, cx, cy)

def draw_star_symbol(draw, cx, cy):
    draw_star(draw, cx, cy, 25, "gold", 5)

def draw_torch_symbol(draw, cx, cy):
    draw_torch(draw, cx, cy, "#FFD700")

def draw_tree_symbol(draw, cx, cy):
    # Trunk
    draw.rectangle([cx-5, cy+5, cx+5, cy+30], fill="#8B4513")
    # Canopy
    draw.ellipse([cx-25, cy-30, cx+25, cy+15], fill="#228B22")
    draw.ellipse([cx-18, cy-40, cx+18, cy+5], fill="#2E8B57")

def draw_lion_symbol(draw, cx, cy):
    draw.ellipse([cx-20, cy-20, cx+20, cy+20], fill="gold")
    draw.ellipse([cx-8, cy-10, cx-3, cy-5], fill="black")
    draw.ellipse([cx+3, cy-10, cx+8, cy-5], fill="black")
    draw.arc([cx-10, cy-5, cx+10, cy+10], 0, 180, fill="black", width=2)

def draw_anchor_symbol(draw, cx, cy):
    draw.line([(cx, cy-25), (cx, cy+20)], fill="white", width=4)
    draw.ellipse([cx-8, cy-30, cx+8, cy-18], fill="white", outline="black", width=1)
    draw.arc([cx-20, cy+5, cx+20, cy+30], 200, 340, fill="white", width=4)
    draw.line([(cx-25, cy-15), (cx+25, cy-15)], fill="white", width=3)

def draw_bear_symbol(draw, cx, cy):
    draw.ellipse([cx-22, cy-22, cx+22, cy+22], fill="#B31B1B")
    draw.ellipse([cx-10, cy-8, cx-4, cy-2], fill="white")
    draw.ellipse([cx+4, cy-8, cx+10, cy-2], fill="white")
    draw.ellipse([cx-6, cy+5, cx+6, cy+15], fill="white")

symbols = [draw_book_symbol, draw_star_symbol, draw_torch_symbol,
           draw_anchor_symbol, draw_book_symbol, draw_tree_symbol,
           draw_lion_symbol, draw_bear_symbol]

# Generate Ivy League logos
for i, (name, primary, secondary, bg) in enumerate(universities):
    img = create_logo(name, primary, secondary, symbols[i], bg_color=bg)
    img.save(os.path.join(LOGO_DIR, f"{name.lower().replace(' ', '_')}_logo.png"))
    print(f"Created {name} logo")

# Generate OpenAI logo
openai_img = create_openai_logo()
openai_img.save(os.path.join(LOGO_DIR, "openai_logo.png"))
print("Created OpenAI logo")

# Generate Anthropic logo
anthropic_img = create_anthropic_logo()
anthropic_img.save(os.path.join(LOGO_DIR, "anthropic_logo.png"))
print("Created Anthropic logo")

print("All logos generated successfully!")
