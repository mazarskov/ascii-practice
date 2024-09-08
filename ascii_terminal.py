from PIL import Image, ImageDraw, ImageFont

# Define ASCII characters from dense to light
LIGHT = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
ASCII_CHARS = ['$', '@', 'B', '%', '8', '&', 'W', 'M', '#', '*', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', 'Z', 'O', '0', 'Q', 'L', 'C', 'J', 'U', 'Y', 'X', 
               'z', 'c', 'v', 'u', 'n', 'x', 'r', 'j', 'f', 't', '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']', '?', '-', '_', '+', '~', '<', '>', 
               'i', '!', 'l', 'I', ';', ':', ',', '"', '^', '`', "'", '.', ' ']
MEDIUM = []
for char in ASCII_CHARS:
    if ASCII_CHARS.index(char) % 2 != 0:
        MEDIUM.append(char)

# Write-Host "^[[1;34mBold red^[[0m ^[[1;32mBold green^[[0m"

box_size = 8 #8
font_size = 10 #13
width = 100
approx = []



def image_to_ascii(image_path, asci_list, new_width=width):
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
        char = asci_list[avg_color // 25]
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

image_to_ascii("windows.jpg", LIGHT, 50)