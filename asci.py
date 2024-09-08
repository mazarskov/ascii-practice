from PIL import Image, ImageDraw, ImageFont

# Define ASCII characters from dense to light
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

box_size = 8 #8
font_size = 10 #13
width = 80
approx = []

def image_to_ascii(image_path, new_width=width):
    # Load image and convert to RGB
    image = Image.open(image_path).convert('RGB')
    file1 = open("ascifile.txt", "w")
    
    # Resize image based on desired width
    width, height = image.size
    ratio = height / width  / 2 # Adjust height for aspect ratio, this preserves the original aspect ratio of the image.
    new_height = int(new_width * ratio)
    image = image.resize((new_width, new_height))
    
    # Convert pixels to ASCII and extract colors
    # Pixels in my case of "RGB" are a list of tuples, every tuple is threee values. So 'pixel' is (0, 0, 0)
    pixels = image.getdata()
    ascii_str = ""
    colors = []
    
    
    for pixel in pixels:
        # Calculate ASCII character based on grayscale approximation
        avg_color = sum(pixel) // 3
        char = ASCII_CHARS[avg_color // 25]
        ascii_str += char
        colors.append(pixel)
        approx.append(avg_color)
    
    # Format ASCII string into lines
    # Unused method as I don't really understand the syntax. Below is the re-written method.
    # ascii_img = "\n".join([ascii_str[i:(i + new_width)] for i in range(0, len(ascii_str), new_width)])
    # return ascii_img, colors
    # ascii_str is all the correct characters but in one line, so here i space them accordingly to the 'new_width' that i myself provide
    
    ascii_img = ""
    for i in range(0, len(ascii_str), new_width):
        # Starts at i and goes up to new width + i (non incusive)
        ascii_img += ascii_str[i:(i + new_width)] + "\n"
    # Strip used here to get rid of the last \n
    file1.write(ascii_img.strip())
    file1.close()
    return ascii_img.strip(), colors

def ascii_to_colored_image(ascii_str, colors, box_size=20, font_size=None, font_path=None, output_path='output.png', back_color=None):
    # Break ASCII string into lines. "ascii_str" here refers to "ascii_img" that was return from the prevoius function.
    ascii_lines = ascii_str.splitlines()
    width = len(ascii_lines[0])
    height = len(ascii_lines)
    
    # Set up the font and image size
    if font_path:
        font = ImageFont.truetype(font_path, font_size or box_size)
    else:
        font = ImageFont.load_default()
    
    # Calculate the actual size of characters
    # Draws a 1x1 image with the letter 'X' to calculate how much space in takes inside the image.
    dummy_image = Image.new('RGB', (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_image)
    # This calculates the bounding box of the letter "X". It's not centered yet, so it start from the top left corner,
    # that's how we know that left and top are both 0
    left, top, right, bottom = dummy_draw.textbbox((0, 0), 'X', font=font)
    # Since top and left are both 0, we use that to easily calculate the width by doing right - left and height by bottom - top.
    char_width, char_height = right - left, bottom - top
    
    # Width here is len(ascii_lines[0]) and the img_width is the product of width and box_size.
    # image_width and image_height will be used as the dimensions for the output.
    img_width = width * box_size
    img_height = height * box_size
    # Draws a blank image with the approximation of the brightness of the image.
    # The approximation is done by finding the average grayscale value of the image.
    # The if statemtn here checks if optional paramater was specified when calling the function, to see which background color to choose.
    if back_color:
        background_color = int(back_color)
    else:
        background_color = int(sum(approx) / len(approx))
    #background_color = 135
    image = Image.new('RGB', (img_width, img_height), color=(background_color, background_color, background_color))
    draw = ImageDraw.Draw(image)
    
    # Draw each character with color
    # Itertaes over every line, y being the index and line being the line itself.

    for y, line in enumerate(ascii_lines):
        # Iterates over every char on the line, x being the index and char being char itself.
        for x, char in enumerate(line):
            # Get the color for the current character
            # Colors is just and array of tuples so every color is (0, 0, 0).
            # In the calculation colors[y * width + x] 'y' is the line index and 'x' is and index of character on the line. 
            color = colors[y * width + x]
            
            # Calculate position to center the character in the box
            char_x = x * box_size + (box_size - char_width) // 2
            char_y = y * box_size + (box_size - char_height) // 2
            draw.text((char_x, char_y), char, font=font, fill=color)

    # Save the final image
    image.save(output_path)

image_path = "windows.jpg"
ascii_art, colors = image_to_ascii(image_path)
ascii_to_colored_image(ascii_art, colors, box_size=box_size, font_size=font_size, font_path="font\\SpaceMono-Bold.ttf", output_path='output.png')
print(sum(approx) / len(approx))