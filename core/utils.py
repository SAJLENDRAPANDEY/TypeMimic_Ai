import time
import random
import string

# ---------------- RANDOM DELAY ---------------- #

def random_delay(min_delay, max_delay):
    """
    Human-like random typing delay
    """

    delay = random.uniform(min_delay, max_delay)

    time.sleep(delay)

# ---------------- ERROR SIMULATION ---------------- #

def should_make_error(error_rate):
    """
    Decide whether to make a typing mistake
    """

    return random.random() < error_rate

# ---------------- RANDOM WRONG CHARACTER ---------------- #

def get_random_char():
    """
    Return random keyboard character
    """

    characters = (
        string.ascii_letters +
        string.digits
    )

    return random.choice(characters)

# ---------------- HUMAN THINKING PAUSE ---------------- #

def thinking_pause(min_time=0.5, max_time=2):
    """
    Simulate human thinking pause
    """

    pause = random.uniform(min_time, max_time)

    time.sleep(pause)

# ---------------- VARIABLE TYPING SPEED ---------------- #

def variable_typing_speed(base_speed):
    """
    Slightly vary typing speed naturally
    """

    variation = random.uniform(-0.02, 0.02)

    speed = base_speed + variation

    return max(0.01, speed)

# ---------------- BACKSPACE DELAY ---------------- #

def backspace_delay():
    """
    Delay before correcting mistakes
    """

    delay = random.uniform(0.05, 0.2)

    time.sleep(delay)

# ---------------- LINE PAUSE ---------------- #

def line_pause():
    """
    Pause after completing line
    """

    delay = random.uniform(0.3, 1.0)

    time.sleep(delay)

# ---------------- LONG BREAK ---------------- #

def long_break():
    """
    Simulate long human break
    """

    delay = random.uniform(2, 5)

    time.sleep(delay)

# ---------------- PUNCTUATION PAUSE ---------------- #

def punctuation_pause():
    """
    Extra pause after punctuation
    """

    delay = random.uniform(0.2, 0.6)

    time.sleep(delay)