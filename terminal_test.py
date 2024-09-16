import shutil
import time
import os

def fill_terminal_with_text_dynamic(text):
    previous_size = shutil.get_terminal_size()
    text_position = 0
    scroll_position = 0

    try:
        while True:
            current_size = shutil.get_terminal_size()

            if current_size != previous_size:
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')  # Clear the entire screen
                previous_size = current_size

            print("\033[H", end="")  # Move cursor to home position

            terminal_width = current_size.columns
            terminal_height = current_size.lines

            full_screen_text = ""
            for _ in range(terminal_height):
                line = ""
                for _ in range(terminal_width):
                    line += text[(text_position + scroll_position) % len(text)]
                    text_position += 1
                full_screen_text += line + "\n"

            # Remove the last newline and print the entire screen at once
            print(f"\033[38;5;203m{full_screen_text[:-1]}\033[0m", end="")

            scroll_position = (scroll_position + 1) % len(text)
            time.sleep(1)  # Adjust this value to change scroll speed

    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    fill_terminal_with_text_dynamic("ILOVEYOU")