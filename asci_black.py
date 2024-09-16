from PIL import Image, ImageDraw, ImageFont
import os

#ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
ASCII_CHARS = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
ASCII_CHARS_REVERSE = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
ASCII_CHARS_REVERSE.reverse()

box = 10
font = 15
width = 200


def image_to_ascii(image_path, new_width=width, ):
    # Load image and convert to grayscale
    image = Image.open(image_path).convert('L')
    
    # Resize image based on desired width
    width, height = image.size
    ratio = height / width / 1  # Adjust height for aspect ratio
    new_height = int(new_width * ratio)
    image = image.resize((new_width, new_height))
    
    # Convert pixels to ASCII
    pixels = image.getdata()
    ascii_str = "".join([ASCII_CHARS_REVERSE[pixel // 25] for pixel in pixels])
    
    # Format ASCII string into lines
    ascii_img = "\n".join([ascii_str[i:(i + new_width)] for i in range(0, len(ascii_str), new_width)])
    return ascii_img

def ascii_to_image(ascii_str, box_size=20, font_size=None, font_path=None, output_path='output.png'):
    # Break ASCII string into lines
    ascii_lines = ascii_str.splitlines()
    width = len(ascii_lines[0])
    height = len(ascii_lines)
    
    # Set up the font and image size
    if font_path:
        font = ImageFont.truetype(font_path, font_size or box_size)
    else:
        font = ImageFont.load_default()
    
    # Calculate the actual size of characters
    dummy_image = Image.new('RGB', (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_image)
    left, top, right, bottom = dummy_draw.textbbox((0, 0), 'X', font=font)
    char_width, char_height = right - left, bottom - top
    
    img_width = width * box_size
    img_height = height * box_size
    #image = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    image = Image.new('RGB', (img_width, img_height), color=(50, 50, 50))
    draw = ImageDraw.Draw(image)
    
    # Draw each character
    for y, line in enumerate(ascii_lines):
        for x, char in enumerate(line):
            # Calculate position to center the character in the box
            char_x = x * box_size + (box_size - char_width) // 2
            char_y = y * box_size + (box_size - char_height) // 2
            #draw.text((char_x, char_y), char, font=font, fill=(0, 0, 0))
            draw.text((char_x, char_y), char, font=font, fill=(255, 255, 255))
    
    # Save the final image
    image.save(output_path)

image_path = "picture.jpg"
ascii_art = image_to_ascii(image_path)

if os.name == 'nt':
    ascii_to_image(ascii_art, box_size=box, font_size=font, font_path="font\\SpaceMono-Bold.ttf", output_path='output_black.png')
else:
    ascii_to_image(ascii_art, box_size=box, font_size=font, font_path="font/SpaceMono-Bold.ttf", output_path='output_black.png')