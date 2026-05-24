import pyautogui
import time
import random
import pygame

import core.config as config

from core.utils import (
    random_delay,
    should_make_error,
    # get_random_char,
    backspace_delay
)

# ---------------- PYGAME INIT ---------------- #

pygame.mixer.init()

typing_sound = pygame.mixer.Sound(
    "sounds/click.wav"
)

typing_sound.set_volume(0.3)

# Dedicated sound channel
sound_channel = pygame.mixer.Channel(0)

# ---------------- SAFETY ---------------- #

# Move mouse to top-left corner to stop instantly
pyautogui.FAILSAFE = True


# ---------------- WRONG WORD GENERATOR ---------------- #

def get_wrong_word(real_word):

    if len(real_word) <= 3:
        return real_word

    word = list(real_word)

    error_type = random.choice([
        "missing",
        "double",
        "swap"
    ])

    # Missing character
    if error_type == "missing":

        index = random.randint(1, len(word)-1)

        del word[index]

    # Double character
    elif error_type == "double":

        index = random.randint(0, len(word)-1)

        word.insert(index, word[index])

    # Swap nearby letters
    elif error_type == "swap":

        index = random.randint(0, len(word)-2)

        word[index], word[index+1] = (
            word[index+1],
            word[index]
        )

    return "".join(word)

# ---------------- REALISTIC TYPO SYSTEM ---------------- #

KEYBOARD_NEIGHBORS = {

    'a': ['s', 'q', 'z'],
    'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'e': ['w', 's', 'd', 'r'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'j', 'k', 'o'],
    'j': ['h', 'u', 'i', 'k', 'm', 'n'],
    'k': ['j', 'i', 'o', 'l'],
    'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k'],
    'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'k', 'l', 'p'],
    'p': ['o', 'l'],
    'q': ['w', 'a'],
    'r': ['e', 'd', 'f', 't'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', 'f', 'g', 'y'],
    'u': ['y', 'h', 'j', 'i'],
    'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'a', 's', 'e'],
    'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'g', 'h', 'u'],
    'z': ['a', 's', 'x']
}


def get_realistic_typo(char):

    lower_char = char.lower()

    if lower_char in KEYBOARD_NEIGHBORS:

        typo = random.choice(
            KEYBOARD_NEIGHBORS[lower_char]
        )

        # Preserve uppercase
        if char.isupper():
            return typo.upper()

        return typo

    return char

# ---------------- MAIN FUNCTION ---------------- #

def type_text(text, controller):

    line_count = 0

    # ---------------- START MESSAGE ---------------- #

    print("Place cursor in typing area...")
    time.sleep(3)

    # ---------------- CURSOR POSITION CHECK ---------------- #

    try:

        current_x, current_y = pyautogui.position()

        print(
            f"Typing starts at: "
            f"{current_x}, {current_y}"
        )

    except Exception as e:

        print("Mouse position error:", e)
        return

    # ---------------- ACTIVE WINDOW CHECK ---------------- #

    try:

        active_window = pyautogui.getActiveWindow()

        if active_window is None:

            print("No active window found.")
            return

        print("Typing in:", active_window.title)

    except Exception as e:

        print("Window detection failed:", e)
        return

    # ---------------- SPLIT WORDS ---------------- #

    words = text.split(" ")

    # ---------------- MAIN LOOP ---------------- #

    for word_index, word in enumerate(words):

        # ---------------- STOP ---------------- #

        if controller.stop:

            sound_channel.stop()
            break

        # ---------------- PAUSE ---------------- #

        while controller.paused:

            sound_channel.stop()

            time.sleep(0.1)

            if controller.stop:

                sound_channel.stop()
                return

        # ==================================================
        # RANDOM WRONG WORD FEATURE
        # ==================================================

        # 10% chance
        if random.randint(1, 100) <= 10:

            wrong_word = get_wrong_word(word)

            # ---------------- TYPE WRONG WORD ---------------- #

            for char in wrong_word:

                sound_channel.play(typing_sound)

                pyautogui.write(char)

                random_delay(
                    config.MIN_DELAY,
                    config.MAX_DELAY
                )

            # Add space after wrong word
            pyautogui.write(" ")

            # Human thinking pause
            random_delay(0.5, 1.0)

            # ---------------- DELETE WRONG WORD ---------------- #

            # Remove word + space
            total_backspaces = len(wrong_word) + 1

            for _ in range(total_backspaces):

                pyautogui.press("backspace")

                backspace_delay()

            # Pause before correction
            random_delay(0.2, 0.5)

        # ==================================================
        # TYPE REAL WORD
        # ==================================================

        for char in word:

            # ---------------- SMALL TYPO ---------------- #

            if should_make_error(config.ERROR_RATE):

                wrong_char = get_realistic_typo(char)

                # Avoid same character
                if wrong_char != char:

                    # Type wrong character
                    sound_channel.play(typing_sound)

                    pyautogui.write(wrong_char)

                    # Make mistake visible
                    time.sleep(random.uniform(0.2, 0.5))

                    # Backspace correction
                    pyautogui.press("backspace")

                    time.sleep(random.uniform(0.1, 0.2))

            # ---------------- TYPE REAL CHARACTER ---------------- #

            sound_channel.play(typing_sound)

            pyautogui.write(char)

            # ---------------- HUMAN DELAY ---------------- #

            random_delay(
                config.MIN_DELAY,
                config.MAX_DELAY
            )

            # ---------------- PUNCTUATION PAUSE ---------------- #

            if char in [".", ",", "!", "?"]:

                random_delay(
                    *config.PUNCTUATION_DELAY
                )

            # ---------------- LINE PAUSE ---------------- #

            if char == "\n":

                line_count += 1

                random_delay(
                    *config.LINE_DELAY
                )

                # Long pause every few lines
                if (
                    line_count %
                    config.LONG_PAUSE_EVERY == 0
                ):

                    random_delay(
                        *config.LONG_PAUSE_DURATION
                    )

        # ---------------- SPACE BETWEEN WORDS ---------------- #

        # Avoid extra space at end
        if word_index != len(words) - 1:

            pyautogui.write(" ")

            random_delay(0.03, 0.15)

    # ---------------- FINISH ---------------- #

    sound_channel.stop()

    print("Typing completed.")