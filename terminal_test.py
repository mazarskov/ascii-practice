import shutil
import os
import time

def fill_terminal_with_text_dynamic(text):
    previous_size = shutil.get_terminal_size()
    first_run = True
    text_position = 0  # Keep track of where we are in the text

    try:
        while True:
            current_size = shutil.get_terminal_size()

            if current_size != previous_size or first_run:
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')

                terminal_width = current_size.columns
                terminal_height = current_size.lines

                for _ in range(terminal_height):
                    line = ""
                    for _ in range(terminal_width):
                        line += text[text_position % len(text)]
                        text_position += 1
                    print(f"\033[38;5;203m{line}\033[0m")


                previous_size = current_size
                first_run = False

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    fill_terminal_with_text_dynamic("ILOVEYOU")