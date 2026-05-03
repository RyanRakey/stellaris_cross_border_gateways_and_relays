"""
Thumbnail Generator for Stellaris Steam Workshop Mod

Usage:
    python generate_thumbnail.py <input_image> <output_image>

Generates a 512x512 Steam Workshop thumbnail with the mod title overlay.
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os

# Configuration
THUMBNAIL_SIZE = (512, 512)
MOD_TITLE_LINE1 = 'Cross-Border'
MOD_TITLE_LINE2 = 'Gateways and Relays'
FONT_SIZE = 48
TEXT_COLOR = 'white'
SHADOW_COLOR = 'black'
SHADOW_OFFSET = 2
PADDING_TOP = 20
LINE_SPACING = 10


def generate_thumbnail(input_path, output_path):
    # Open and resize image
    img = Image.open(input_path)
    img = img.resize(THUMBNAIL_SIZE, Image.LANCZOS)
    draw = ImageDraw.Draw(img)

    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype('arial.ttf', FONT_SIZE)
    except:
        try:
            font = ImageFont.truetype('DejaVuSans-Bold.ttf', FONT_SIZE)
        except:
            font = ImageFont.load_default()

    # Calculate positions (centered horizontally)
    img_width, img_height = img.size

    # Get text bounding boxes for centering
    bbox1 = draw.textbbox((0, 0), MOD_TITLE_LINE1, font=font)
    bbox2 = draw.textbbox((0, 0), MOD_TITLE_LINE2, font=font)
    text_width1 = bbox1[2] - bbox1[0]
    text_width2 = bbox2[2] - bbox2[0]
    text_height1 = bbox1[3] - bbox1[1]
    text_height2 = bbox2[3] - bbox2[1]

    x1 = (img_width - text_width1) // 2
    x2 = (img_width - text_width2) // 2
    y1 = PADDING_TOP
    y2 = y1 + text_height1 + LINE_SPACING

    # Draw dropshadow (black, slight offset)
    for line, x, y in [(MOD_TITLE_LINE1, x1, y1), (MOD_TITLE_LINE2, x2, y2)]:
        draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET), line, font=font, fill=SHADOW_COLOR)

    # Draw white text on top
    for line, x, y in [(MOD_TITLE_LINE1, x1, y1), (MOD_TITLE_LINE2, x2, y2)]:
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)

    img.save(output_path, 'PNG')
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f'Saved {output_path} ({THUMBNAIL_SIZE[0]}x{THUMBNAIL_SIZE[1]})')
    print(f'File size: {size_mb:.2f} MB')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: python {sys.argv[0]} <input_image> <output_image>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    generate_thumbnail(input_path, output_path)
