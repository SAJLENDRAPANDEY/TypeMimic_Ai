import time


class Controller:

    def __init__(self):

        self.paused = False

        self.stop = False

        # Statistics
        self.characters_typed = 0

        self.corrections = 0

        self.errors = 0

        self.start_time = None

    def toggle_pause(self):

        self.paused = not self.paused

    def stop_typing(self):

        self.stop = True

    def reset(self):

        self.paused = False

        self.stop = False

        self.characters_typed = 0

        self.corrections = 0

        self.errors = 0

        self.start_time = time.time()

    def typing_duration(self):

        if not self.start_time:

            return 0

        return int(
            time.time() - self.start_time
        )

    def average_speed(self):

        duration = self.typing_duration()

        if duration == 0:

            return 0

        return round(
            self.characters_typed / duration,
            2
        )