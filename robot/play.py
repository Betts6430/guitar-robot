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


def do_action(hw, action):
    event_type = action[1]

    if event_type == "press":
        _, _, string, fret = action
        hw.press(string, fret)

    elif event_type == "release":
        _, _, string, fret = action
        hw.release(string, fret)

    elif event_type == "strum":
        _, _, direction, low, high = action
        hw.strum(direction, low, high)

    else:
        raise ValueError(f"Unknown action {event_type}")


def run_timeline(actions, hw):
    """Do each action at its time, counting from when this function starts.
    Ctrl+C stops it, and every solenoid is switched off however it ends.
    """
    start_time = time.perf_counter()
    try:
        for action in actions:
            # Action time is the start_time + desired_time
            target_time = start_time + action[0]

            # Sleep until we reach the target_time (or 0s if actions are on the same beat)
            time.sleep(max(0, target_time - time.perf_counter()))

            late = time.perf_counter() - target_time
            if late > 0.01:
                print(f"warning: {late * 1000:.0f} ms late")

            do_action(hw, action)

    except KeyboardInterrupt:
        print("Stopped.")

    finally:
        hw.all_off()


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
