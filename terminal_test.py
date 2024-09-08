import shutil
import os
import time

def fill_terminal_with_text_dynamic(text):
    previous_size = shutil.get_terminal_size()
    first_run = True  # Flag to handle the first print

    try:
        while True:
            # Get the current terminal size
            current_size = shutil.get_terminal_size()

            if current_size != previous_size:
                # Terminal size has changed, clear the screen and update content
                if os.name == 'nt':  # For Windows
                    os.system('cls')
                else:  # For Linux and Mac
                    os.system('clear')

                terminal_width = current_size.columns
                terminal_height = current_size.lines

                # Repeat the text to fill a single row of the terminal
                repeated_text = (text * (terminal_width // len(text) + 1))[:terminal_width]

                # Print the repeated text with color for every row
                for _ in range(terminal_height):
                    print(f"\033[38;5;204m{repeated_text}\033[0m")

                # Update previous_size to the new size
                previous_size = current_size

                first_run = False
            elif first_run:
                # Handle the first run to print content initially
                terminal_width = current_size.columns
                terminal_height = current_size.lines

                repeated_text = (text * (terminal_width // len(text) + 1))[:terminal_width]

                for _ in range(terminal_height):
                    print(f"\033[38;5;204m{repeated_text}\033[0m")

                first_run = False

            # Wait for 0.5 seconds before checking for resize
            time.sleep(0.5)

    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C to exit the program
        print("\nExiting...")

if __name__ == "__main__":
    # Example usage: fill the terminal with "ILOVEYOU" text in pinkish-red
    fill_terminal_with_text_dynamic("ILOVEYOU")
