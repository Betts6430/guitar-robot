"""Runs the whole pipeline.

    python -m robot.play                  play songs/demo.txt on the robot
    python -m robot.play songs/other.txt  play a different song
    python -m robot.play --dry-run        print instead of moving (works on a laptop)
    python -m robot.play --list           print the events and actions, then stop
"""
import sys
import time

from robot import config
from robot.arrange import check_song
from robot.hardware import DryRunHardware, PiHardware
from robot.parse import parse_file
from robot.schedule import schedule


def run_timeline(actions, hw):
    """Do each action at its time, counting from when this function starts.
    (t, "press", s, f) means hw.press(s, f) at time t. Same for release and strum.

    Hints: start = time.perf_counter(), then before each action sleep until
    start + t. Put the loop in try/finally and call hw.all_off() in the
    finally, so Ctrl+C never leaves a solenoid on.
    """
    # TODO: your code here
    raise NotImplementedError("run_timeline")


def main():
    args = sys.argv[1:]
    files = [a for a in args if not a.startswith("--")]
    song = parse_file(files[0] if files else config.DEFAULT_SONG)

    # A dry run pretends the whole grid is built; a real run only allows what's wired.
    if "--dry-run" in args or "--list" in args:
        available = {(s, f) for s in range(6) for f in config.GRID_FRETS}
    else:
        available = set(config.PIN_MAP)
    check_song(song, available)
    actions = schedule(song)

    if "--list" in args:
        for line in song["events"] + actions:
            print(line)
        return

    hw = DryRunHardware() if "--dry-run" in args else PiHardware(config.PIN_MAP)
    print(f"Playing {song['title']}. Ctrl+C to stop.")
    run_timeline(actions, hw)


if __name__ == "__main__":
    main()
