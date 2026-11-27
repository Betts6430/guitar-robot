"""The parts that move. Both classes have the same four methods,
so play.py works with either one."""
import time


class DryRunHardware:
    """Prints instead of moving, so the whole program runs on your laptop."""

    def __init__(self):
        self.start = time.perf_counter()

    def say(self, text):
        print(f"{time.perf_counter() - self.start:6.2f} s  {text}")

    def press(self, string, fret):
        self.say(f"press   string {string} fret {fret}")

    def release(self, string, fret):
        self.say(f"release string {string} fret {fret}")

    def strum(self, direction, low, high):
        self.say(f"strum   {direction} strings {low}-{high}")

    def all_off(self):
        self.say("all off")


class PiHardware:
    """Solenoids through MOSFETs on the GPIO pins."""

    def __init__(self, pin_map):
        from gpiozero import DigitalOutputDevice   # only installed on the Pi
        # TODO: make one DigitalOutputDevice per pin in pin_map and keep them
        # in a dict, e.g. self.solenoids[(string, fret)]

    def press(self, string, fret):
        pass   # TODO: turn that solenoid on

    def release(self, string, fret):
        pass   # TODO: turn it off

    def strum(self, direction, low, high):
        print("strum", direction, low, high)   # TODO: move the pick servo

    def all_off(self):
        pass   # TODO: turn every solenoid off
