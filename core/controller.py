class Controller:

    def __init__(self):

        self.paused = False
        self.stop = False

    def toggle_pause(self):

        self.paused = not self.paused

    def stop_typing(self):

        self.stop = True

    def reset(self):

        self.paused = False
        self.stop = False