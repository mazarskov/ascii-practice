def print_colored_string_256(input_string):
    for i, char in enumerate(input_string):
        color_code = 16 + (i % 240)  # Cycles through the 240 additional colors
        print(f"\033[38;5;{color_code}m{char}", end='')
    print("\033[0m")  # Reset color at the end

# Example usage
print_colored_string_256("Hello, 256-color World!")

def print_colored_string_rgb(input_string):
    for i, char in enumerate(input_string):
        # Create a simple gradient using RGB
        red = (i * 5) % 256
        green = (i * 7) % 256
        blue = (i * 11) % 256
        print(f"\033[38;2;{red};{green};{blue}m{char}", end='')
    print("\033[0m")  # Reset color at the end

# Example usage
print_colored_string_rgb("Hello, True Color World!")

def print_pinkish_colors():
    pinkish_colors = [196, 197, 198, 199, 200, 201, 202, 203, 204, 205]
    for color_code in pinkish_colors:
        print(f"\033[38;5;{color_code}mColor {color_code}", end=' ')
    print("\033[0m")  # Reset at the end

# Example usage
print_pinkish_colors()
print(f"\033[38;5;{203}mI", end='')
print(f"\033[38;5;{204}mLOVEYOU", end='')
print(f"\033[38;5;{203}mI", end='')
print(f"\033[38;5;{204}mLOVEYOU", end='')
print(f"\033[38;5;{203}mI", end='')
print(f"\033[38;5;{204}mLOVEYOU", end='')
print(f"\033[38;5;{203}mI", end='')
print(f"\033[38;5;{204}mLOVEYOU", end='')
print(f"\033[38;5;{203}mI", end='')
print(f"\033[38;5;{204}mLOVEYOU", end='')
print(f"\033[38;5;{203}mI", end='')
print(f"\033[38;5;{204}mLOVEYOU", end='')
print(f"\033[38;5;{203}mI", end='')
print(f"\033[38;5;{204}mLOVEYOU\033[0m", end='')