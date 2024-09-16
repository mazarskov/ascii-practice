from PIL import Image, ImageDraw, ImageFont
import shutil
import time
import os

# Define ASCII characters from dense to light
LIGHT = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
LIGHT_REVERSE = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
LIGHT_REVERSE.reverse()
ASCII_CHARS = ['$', '@', 'B', '%', '8', '&', 'W', 'M', '#', '*', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', 'Z', 'O', '0', 'Q', 'L', 'C', 'J', 'U', 'Y', 'X', 
               'z', 'c', 'v', 'u', 'n', 'x', 'r', 'j', 'f', 't', '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']', '?', '-', '_', '+', '~', '<', '>', 
               'i', '!', 'l', 'I', ';', ':', ',', '"', '^', '`', "'", '.', ' ']
MEDIUM = []
for char in ASCII_CHARS:
    if ASCII_CHARS.index(char) % 2 != 0:
        MEDIUM.append(char)

# Write-Host "^[[1;34mBold red^[[0m ^[[1;32mBold green^[[0m"

width = 0
approx = []
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

def rgb_to_ansi(r, g, b):
    # For grayscale (r, g, b are roughly the same), use the grayscale ramp in ANSI 256 color
    if r == g == b:
        if r < 8:
            return 16  # The darkest color in the grayscale range
        if r > 248:
            return 231  # The lightest color in the grayscale range
        # Map the value to the 24 grayscale levels in the ANSI palette
        return 232 + ((r - 8) // 10)

    # For non-grayscale colors, map to the 6x6x6 color cube
    ansi_r = int((r / 255.0) * 5)  # Red value mapped to 0-5
    ansi_g = int((g / 255.0) * 5)  # Green value mapped to 0-5
    ansi_b = int((b / 255.0) * 5)  # Blue value mapped to 0-5

    # Compute the ANSI 256 color code
    return 16 + (ansi_r * 36) + (ansi_g * 6) + ansi_b

def image_to_ascii(image_path, asci_list, new_width=width, retainAspect=True, color=False, true_color=False):
    # Load image and convert to RGB
    print("\033[?25l", end="") # Makes the cursor invisble in the terminal

    image = Image.open(image_path).convert('RGB')
    width_ter, height_ter = shutil.get_terminal_size()
    width, height = image.size
    ratio = height / width  / 2 # Adjust height for aspect ratio
    if retainAspect == True:
        # Resize image based on desired width
        if width_ter >= height_ter:
            new_width = width_ter - 1
            new_height = int(new_width * ratio)
            image = image.resize((new_width, new_height))
        elif height_ter > width_ter:
            new_height = height_ter - 1
            new_width = int(new_height * (1/ratio))
            image = image.resize((new_width, new_height))
        
        if new_height >= height_ter:
            new_height = height_ter - 1
            new_width = int(new_height * (1/ratio))
            image = image.resize((new_width, new_height))

    else:
        new_width = width_ter - 1
        new_height = height_ter - 1
        image = image.resize((new_width, new_height))
    # Convert pixels to ASCII and extract colors
    # Pixels in my case of "RGB" are a list of tuples, every tuple is threee values. So 'pixel' is (0, 0, 0)
    pixels = image.getdata()
    ascii_str = ""
    colors = []

    for pixel in pixels:
        # Calculate ASCII character based on grayscale approximation
        avg_color = sum(pixel) // 3
        #char = asci_list[avg_color // 25]
        index = min(avg_color // (256 // len(asci_list)), len(asci_list) - 1)
        char = asci_list[index]

        ascii_str += char
        colors.append(pixel)
        approx.append(avg_color)
    # Format ASCII string into lines
    # Unused method as I don't really understand the syntax. Below is the re-written method.
    # ascii_img = "\n".join([ascii_str[i:(i + new_width)] for i in range(0, len(ascii_str), new_width)])
    # return ascii_img, colors
    # ascii_str is all the correct characters but in one line, so here i space them accordingly to the 'new_width' that i myself provide
    
    ascii_img = ""
    if color == False:
        for i in range(0, len(ascii_str), new_width):
            # Starts at i and goes up to new width + i (non incusive)
            ascii_img += ascii_str[i:(i + new_width)] + "\n"
    else:
        j = 0
        for o in range(0, len(ascii_str)):
            if j == new_width:
                ascii_img += "\n"
                j = 0
            if true_color == False:
                ascii_img += f"\033[38;5;{rgb_to_ansi(colors[o][0], colors[o][1], colors[o][2])}m{ascii_str[o]}\033[0m"
            else:
                ascii_img += f"\033[38;2;{colors[o][0]};{colors[o][1]};{colors[o][2]}m{ascii_str[o]}\033[0m"
            j += 1

    # Strip used here to get rid of the last \n
    print("\033[H" + ascii_img.strip()) # Escape code to print on top of text insted of first removing it.
    return ascii_img.strip(), colors

def fill_terminal_with_text_dynamic(image_path, ascii_set, retain_aspect, color, true_color):
    previous_frame = [0, 0]
    try:
        while True:
            current_size = shutil.get_terminal_size()
            if current_size[0] < previous_frame[0]:
                if os.name == 'nt':
                    
                    os.system('cls')
                else:
                    os.system('clear')
            previous_frame = current_size
            terminal_width = current_size.columns
            image_to_ascii(image_path, ascii_set, terminal_width, retain_aspect, color, true_color)
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nExiting...")


width_ter, height_ter = shutil.get_terminal_size()

if __name__ == "__main__":

    # Parameters: Image path, ascii character set, retain aspect ratio, color mode, (if color mode True) true color mode
    fill_terminal_with_text_dynamic("drawingicon.png", LIGHT, True, False, True)