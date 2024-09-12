from PIL import Image, ImageDraw, ImageFont
import shutil
import time
import os
import cv2

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

width = 0
approx = []
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
f = open("log.txt", "w")

def image_to_ascii(image_path, asci_list, new_width=width, retainAspect=True):
    # Load image and convert to RGB
    print("\033[?25l", end="") # Makes the cursor invisble in the terminal

    image = image_path
    width_ter, height_ter = shutil.get_terminal_size()
    f.write(f"Width: {width_ter} and Height: {height_ter}\n")
    if retainAspect == True:
        # Resize image based on desired width
        width, height = image.size
        ratio = height / width  / 2 # Adjust height for aspect ratio
        new_height = int(new_width * ratio)
        if (new_height > height_ter):
            new_height = height_ter - 1
            new_width = int(height_ter * (1/ratio))

        image = image.resize((new_width, new_height))
    else:
        image = image.resize((width_ter, height_ter - 1)) # No idea what this "1" does but without it the ting breaks
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
    f.write(f"\n{str(len(ascii_img))}")
    print("\033[H" + ascii_img.strip()) # Escape code to print on top of text insted of first removing it.
    return ascii_img.strip(), colors

def fill_terminal_with_text_dynamic():
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
            image_to_ascii("kanagawa.jpg", LIGHT, terminal_width, True)
            #time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nExiting...")


width_ter, height_ter = shutil.get_terminal_size()
def video_to_ascii(video_path, ascii_list, new_width, fps):
    cap = cv2.VideoCapture(video_path)
    #print("\033[?25l", end="")
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    frame_duration = 1 / fps
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break  # Exit the loop if no more frames

        # Convert frame (cv2 image) to RGB and then to a PIL image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        
        # Call the ASCII conversion function
        #os.system('cls')
        previous_frame = [0, 0]
        current_size = shutil.get_terminal_size()
        if current_size[0] < previous_frame[0]:
            if os.name == 'nt':
                    
                os.system('cls')
            else:
                os.system('clear')
        previous_frame = current_size
        terminal_width = current_size.columns
        image_to_ascii(pil_image, ascii_list, new_width, True)
        
        # Control frame rate (adjust to match video FPS, e.g., 24 FPS -> 1/24)
        # Calculate how long the frame processing took
        processing_time = time.time() - start_time

        # Calculate the remaining time to sleep to match the desired FPS
        sleep_time = frame_duration - processing_time

        # Only sleep if there's time remaining to maintain FPS
        if sleep_time > 0:
            time.sleep(sleep_time)

    cap.release()
    f.close()

# Usage example


if __name__ == "__main__":

    width_ter, height_ter = shutil.get_terminal_size()
    video_path = 'Bad_Apple.mp4'
    video_to_ascii(video_path, LIGHT, width_ter, 60)


#image_to_ascii("kanagawa.jpg", LIGHT, width_ter, True)

#if __name__ == "__main__":
    #fill_terminal_with_text_dynamic()