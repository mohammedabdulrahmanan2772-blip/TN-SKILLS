import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("image", exist_ok=True)

def create_legal_logo(filename, is_dark_mode=False):
    width, height = 500, 160
    # Image with transparent background
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    fg_color = (255, 255, 255, 255) if is_dark_mode else (26, 32, 44, 255)
    accent_color = (59, 130, 246, 255) if is_dark_mode else (37, 99, 235, 255)
    sub_color = (156, 163, 175, 255) if is_dark_mode else (100, 116, 139, 255)
    
    # Draw Balance Scales of Justice Symbol on the left
    # Scale center pillar
    pillar_x = 75
    pillar_top = 25
    pillar_bottom = 135
    
    # Central triangle stand & column
    draw.polygon([(pillar_x - 30, pillar_bottom), (pillar_x + 30, pillar_bottom), (pillar_x, pillar_bottom - 20)], fill=accent_color)
    draw.line([(pillar_x, pillar_top + 10), (pillar_x, pillar_bottom - 15)], fill=fg_color, width=5)
    draw.ellipse([(pillar_x - 12, pillar_top - 2), (pillar_x + 12, pillar_top + 22)], fill=accent_color)
    
    # Beam
    beam_left = pillar_x - 45
    beam_right = pillar_x + 45
    beam_y = pillar_top + 18
    draw.line([(beam_left, beam_y), (beam_right, beam_y)], fill=fg_color, width=4)
    
    # Left Pan Strings & Pan
    draw.line([(beam_left, beam_y), (beam_left - 18, beam_y + 42)], fill=fg_color, width=2)
    draw.line([(beam_left, beam_y), (beam_left + 18, beam_y + 42)], fill=fg_color, width=2)
    draw.arc([(beam_left - 24, beam_y + 35), (beam_left + 24, beam_y + 55)], start=0, end=180, fill=accent_color, width=4)
    draw.line([(beam_left - 24, beam_y + 45), (beam_left + 24, beam_y + 45)], fill=accent_color, width=3)
    
    # Right Pan Strings & Pan
    draw.line([(beam_right, beam_y), (beam_right - 18, beam_y + 42)], fill=fg_color, width=2)
    draw.line([(beam_right, beam_y), (beam_right + 18, beam_y + 42)], fill=fg_color, width=2)
    draw.arc([(beam_right - 24, beam_y + 35), (beam_right + 24, beam_y + 55)], start=0, end=180, fill=accent_color, width=4)
    draw.line([(beam_right - 24, beam_y + 45), (beam_right + 24, beam_y + 45)], fill=accent_color, width=3)
    
    # Typography
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 52)
        font_subtitle = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        
    draw.text((150, 32), "LegalEase", fill=fg_color, font=font_title)
    draw.text((152, 95), "AI LEGAL DOCUMENT GENERATOR", fill=sub_color, font=font_subtitle)
    
    img.save(filename)
    print(f"Generated {filename}")

if __name__ == "__main__":
    create_legal_logo("image/Logo.png", is_dark_mode=False)
    create_legal_logo("image/inverseLogo.png", is_dark_mode=True)
