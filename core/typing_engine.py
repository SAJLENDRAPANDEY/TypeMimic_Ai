"""Typing engine for TypeMimic."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import random
import time

import pygame
import pyautogui

from core.path_helper import resource_path

import core.config as config


DEFAULT_SOUND_PATH = resource_path(
    "sounds/click.wav"
)

DEFAULT_SOUND_VOLUME = 0.3
DEFAULT_THINKING_PAUSE = (0.2, 0.6)

_sound_channel = None

def _clean_text(text: str) -> str:

    # Keep line breaks
    text = text.replace("\r", "")

    # Remove tabs
    text = text.replace("\t", " ")

    # Clean extra spaces in each line
    lines = []

    for line in text.split("\n"):

        cleaned = " ".join(line.split())

        lines.append(cleaned)

    return "\n".join(lines)


KEYBOARD_NEIGHBORS = {
    "a": ["s", "q", "z"],
    "b": ["v", "g", "h", "n"],
    "c": ["x", "d", "f", "v"],
    "d": ["s", "e", "r", "f", "c", "x"],
    "e": ["w", "s", "d", "r"],
    "f": ["d", "r", "t", "g", "v", "c"],
    "g": ["f", "t", "y", "h", "b", "v"],
    "h": ["g", "y", "u", "j", "n", "b"],
    "i": ["u", "j", "k", "o"],
    "j": ["h", "u", "i", "k", "m", "n"],
    "k": ["j", "i", "o", "l"],
    "l": ["k", "o", "p"],
    "m": ["n", "j", "k"],
    "n": ["b", "h", "j", "m"],
    "o": ["i", "k", "l", "p"],
    "p": ["o", "l"],
    "q": ["w", "a"],
    "r": ["e", "d", "f", "t"],
    "s": ["a", "w", "e", "d", "x", "z"],
    "t": ["r", "f", "g", "y"],
    "u": ["y", "h", "j", "i"],
    "v": ["c", "f", "g", "b"],
    "w": ["q", "a", "s", "e"],
    "x": ["z", "s", "d", "c"],
    "y": ["t", "g", "h", "u"],
    "z": ["a", "s", "x"],
}


def _configure_failsafe() -> None:
    try:
        pyautogui.FAILSAFE = True
    except Exception:
        pass


def _normalize_profile(profile: Any) -> dict[str, Any]:
    if not isinstance(profile, Mapping):
        profile = {}

    min_delay = float(profile.get("min_delay", config.MIN_DELAY))
    max_delay = float(profile.get("max_delay", config.MAX_DELAY))

    if max_delay < min_delay:
        min_delay, max_delay = max_delay, min_delay

    error_rate = float(profile.get("error_rate", 0.03))
    thinking_pause = profile.get("thinking_pause", DEFAULT_THINKING_PAUSE)

    if not isinstance(thinking_pause, (tuple, list)) or len(thinking_pause) != 2:
        thinking_pause = DEFAULT_THINKING_PAUSE
    else:
        thinking_pause = (
            float(thinking_pause[0]),
            float(thinking_pause[1]),
        )

    return {
        "min_delay": min_delay,
        "max_delay": max_delay,
        "error_rate": max(0.0, error_rate),
        "thinking_pause": thinking_pause,
        "sound": str(profile.get("sound", DEFAULT_SOUND_PATH)),
        "volume": float(profile.get("volume", DEFAULT_SOUND_VOLUME)),
    }


def _initialize_sound(sound_path: str, volume: float):
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(
                frequency=44100,
                size=-16,
                channels=2,
                buffer=512,
            )
    except Exception:
        return None

    try:
        pygame.mixer.set_num_channels(max(8, pygame.mixer.get_num_channels()))
    except Exception:
        pass

    try:
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(max(0.0, min(1.0, volume)))
        return sound
    except Exception:
        return None


def _play_sound(sound) -> None:
    global _sound_channel
    if sound is None:
        return

    try:

        # Create channel once
        if _sound_channel is None:

            _sound_channel = pygame.mixer.Channel(0)

        # Stop previous unfinished sound
        _sound_channel.stop()

        # Play fresh sound
        _sound_channel.play(sound)

    except Exception:

        pass


def _sleep(delay: float, controller: Any | None = None, step: float = 0.05) -> bool:
    end_time = time.monotonic() + max(0.0, delay)

    while True:
        if controller is not None and getattr(controller, "stop", False):
            return False

        remaining = end_time - time.monotonic()

        if remaining <= 0:
            return True

        time.sleep(min(step, remaining))


def _random_sleep(min_delay: float, max_delay: float, controller: Any | None = None) -> bool:
    return _sleep(random.uniform(min_delay, max_delay), controller=controller)


def _send_key(char: str, controller) -> None:

    if char == "\n":

        pyautogui.press("enter")

    elif char == "\t":

        pyautogui.press("tab")

    elif char == " ":

        pyautogui.press("space")

    else:

        pyautogui.write(char)

    # Statistics
    controller.characters_typed += 1

def _make_realistic_typo(char: str) -> str:
    if not char.isalpha():
        return char

    neighbors = KEYBOARD_NEIGHBORS.get(char.lower())
    if not neighbors:
        return char

    typo = random.choice(neighbors)
    return typo.upper() if char.isupper() else typo


def _type_character(
    char,
    typing_sound,
    controller
):

    _play_sound(typing_sound)

    _send_key(char, controller)


def _maybe_type_typo(
    char: str,
    profile: dict[str, Any],
    typing_sound,
    controller: Any,
) -> bool:
    error_rate = profile["error_rate"]

    if not char.isalpha() or random.random() >= error_rate:
        return False

    typo_char = _make_realistic_typo(char)
    if typo_char == char:
        return False

    controller.errors += 1

    _type_character(
    char,
    typing_sound,
    controller
    )

    if not _sleep(random.uniform(0.06, 0.16), controller=controller):
        return True

    try:
        pyautogui.press("backspace")
        controller.corrections += 1
    except Exception:
        return True

    _sleep(random.uniform(0.05, 0.12), controller=controller)
    return True


def _wait_for_start(controller: Any) -> bool:
    print("Place cursor in typing area...")
    return _sleep(3.0, controller=controller)


def type_text(text, controller, profile):
    text = _clean_text(text)
    _configure_failsafe()

    settings = _normalize_profile(profile)
    typing_sound = _initialize_sound(settings["sound"], settings["volume"])

    if not _wait_for_start(controller):
        return

    try:
        current_x, current_y = pyautogui.position()
        print(f"Typing starts at: {current_x}, {current_y}")
    except Exception as exc:
        print("Mouse position error:", exc)
        return

    try:
        active_window = pyautogui.getActiveWindow()
        if active_window is None:
            print("No active window found.")
            return

        print("Typing in:", active_window.title)
    except Exception as exc:
        print("Window detection failed:", exc)
        return

    line_count = 0

    for char in text:
        if controller.stop:
            break

        while controller.paused:
            if controller.stop:
                break
            if not _sleep(0.1, controller=controller):
                break

        if controller.stop:
            break

        typo_applied = _maybe_type_typo(char, settings, typing_sound, controller)

        if controller.stop:
            break

        if not typo_applied:
            _type_character(
            char,
            typing_sound,
            controller
            )

        if char == "\n":
            line_count += 1
            if not _sleep(random.uniform(*config.LINE_DELAY), controller=controller):
                break

            if line_count % config.LONG_PAUSE_EVERY == 0:
                if not _sleep(
                    random.uniform(*config.LONG_PAUSE_DURATION),
                    controller=controller,
                ):
                    break

        elif char in {".", ",", "!", "?"}:
            if not _sleep(
                random.uniform(*config.PUNCTUATION_DELAY),
                controller=controller,
            ):
                break

        elif char == " ":
            if not _random_sleep(
                settings["min_delay"],
                settings["max_delay"],
                controller=controller,
            ):
                break

        else:
            if not _random_sleep(
                settings["min_delay"],
                settings["max_delay"],
                controller=controller,
            ):
                break

            if random.random() < 0.02:
                thinking_pause = settings["thinking_pause"]
                if not _sleep(random.uniform(*thinking_pause), controller=controller):
                    break

    try:

        pygame.mixer.stop()

    except Exception:
        pass


    if controller.stop:

        print("Typing stopped.")

    else:

        print("Typing completed.")