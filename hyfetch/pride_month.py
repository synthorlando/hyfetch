import math
import random
from time import sleep

from hyfetch import presets
from hyfetch.color_util import RGB, color
from hyfetch.neofetch_util import term_size
from hyfetch.presets import PRESETS


def start_animation():
    text = r"""
.======================================================.
| .  .              .__       .     .  .       , .   | |
| |__| _.._ ._   .  [__)._.* _| _   |\/| _ ._ -+-|_  | |
| |  |(_][_)[_)\_|  |   [  |(_](/,  |  |(_)[ ) | [ ) * |
|        |  |  ._|                                     |
'======================================================'""".strip("\n")
    text_lines = text.split("\n")
    text_height = len(text_lines)
    text_width = len(text_lines[0])

    speed = 2
    frame_delay = 1 / 25

    colors: list[RGB] = []
    frame = 0

    w, h = term_size()
    blocks = 9
    block_width = w // blocks

    text_start_y = h // 2 - text_height // 2
    text_end_y = text_start_y + text_height
    text_start_x = w // 2 - text_width // 2
    text_end_x = text_start_x + text_width

    colors += PRESETS['rainbow'].colors
    colors += PRESETS['transgender'].colors
    colors += PRESETS['nonbinary'].colors
    colors += PRESETS['agender'].colors
    last_idx = len(colors) - 1

    preset_items = set(PRESETS.items())

    black = RGB(0, 0, 0)
    white = RGB(255, 255, 255)

    def draw_frame():
        nonlocal colors, last_idx
        buf = ""

        # Loop over the height
        for y in range(h):
            # Print the starting color
            buf += colors[((frame + y) // block_width) % len(colors)].to_ansi_rgb(foreground=False)
            buf += white.to_ansi_rgb(foreground=True)

            # Loop over the width
            x = 0
            while x < w:
                idx = frame + x + y + int(math.sin(y + 0.5 * frame) * 2)
                y_text = text_start_y <= y < text_end_y

                border = 1 + int(not (y == text_start_y or y == text_end_y - 1))

                # If it's a switching point
                if idx % block_width == 0 or x == text_start_x - border or x == text_end_x + border:
                    cidx = (idx // block_width) % len(colors)

                    # Print the color at the current frame
                    c = colors[cidx]
                    if y_text and text_start_x - border <= x < text_end_x + border:
                        # buf += c.set_light(0.3).to_ansi_rgb(foreground=False)
                        buf += c.overlay(black, 0.5).to_ansi_rgb(foreground=False)
                    else:
                        buf += c.to_ansi_rgb(foreground=False)

                    # If it's the last color of the last line, check if it's time to randomize new colors
                    if y == h - 1 and x > w - speed - 1:
                        # If idx = last_idx, it's time to randomize
                        if cidx == last_idx:
                            print("Hit")
                            input()
                            # Randomize colors
                            new = random.choice(list(preset_items))[1].colors
                            for c in new:
                                colors[last_idx] = c
                                last_idx = (last_idx + 1) % len(colors)

                # If text should be printed, print text
                if y_text and text_start_x <= x < text_end_x:
                    # Add white background
                    buf += text_lines[y - text_start_y][x - text_start_x]
                else:
                    buf += ' '

                x += 1

            # New line if it isn't the last line
            if y != h - 1:
                buf += color('&r\n')

        print(buf, end='', flush=True)

    while 1:
        # Clear the screen
        # print("\033[2J\033[H", end="")
        draw_frame()
        frame += speed
        sleep(frame_delay)


if __name__ == '__main__':
    start_animation()


