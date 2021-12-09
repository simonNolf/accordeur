import time
import sys


class Timer(object):
    """ Timer met en mode sleep le thread jusqu a ce
        que le temps du set FPS soit termine. Si le temps
        est termine le Timer ne fait rien ou affiche un message
        en cas d'erreur"""

    def __init__(self, fps, warnings=False):
        self.fps = fps
        self.wait_time = 1 / self.fps
        self.last_time = time.time()
        self.warnings = warnings

    def wait(self):
        spend_time = time.time() - self.last_time
        sleep_time = self.wait_time - spend_time

        if sleep_time < 0:
            if self.warnings:
                sys.stderr.write("Warning: Timer delay of {} secs\n".format(round(-sleep_time, 4)))
        else:
            time.sleep(sleep_time)

        self.last_time = time.time()
