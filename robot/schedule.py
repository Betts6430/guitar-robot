"""Stage 3: events in beats -> actions in seconds.

Each action is a tuple that starts with its time in seconds:
    (0.92, "press", 1, 2)          solenoid on at string 1, fret 2
    (2.92, "release", 1, 2)        solenoid off
    (1.00, "strum", "down", 0, 5)  pick across strings 0 to 5

Rules (tests/test_schedule.py checks them):
1. The time of a beat is  lead_in + beat * 60 / tempo
2. For a shape at time t, compare it with the chord held now (use
   positions_needed). Release what isn't in the new chord and press what's
   new, both at t - press_time. Positions in both chords stay down.
3. A strum at time t becomes one strum action at t.
4. A mute at time t releases everything that's pressed.
5. Return sorted(actions).
"""
from robot import config
from robot.arrange import positions_needed


def schedule(song, press_time=config.PRESS_S, lead_in=config.LEAD_IN_S):
    # TODO: your code here. Keep a set of the positions that are pressed
    # right now and update it as you go through song["events"].
    raise NotImplementedError("schedule")
