import pyautogui
import time
import random
import pygame

import core.config as config

from core.utils import (
    random_delay,
    should_make_error,
    get_random_char,
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

    wrong_words = [
        "hte",
        "helo",
        "recieve",
        "teh",
        "watre",
        "machien",
        "pythno",
        "developr"
    ]

    wrong = random.choice(wrong_words)

    # Avoid same word
    while wrong == real_word:
        wrong = random.choice(wrong_words)

    return wrong


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

                wrong_char = get_random_char()

                sound_channel.play(typing_sound)

                pyautogui.write(wrong_char)

                backspace_delay()

                pyautogui.press("backspace")

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