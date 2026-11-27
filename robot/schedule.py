"""Stage 3: events in beats -> actions in seconds.

Each action is a tuple that starts with its time in seconds:
    (0.92, "press", 1, 2)          solenoid on at string 1, fret 2
    (2.92, "release", 1, 2)        solenoid off
    (1.00, "strum", "down", 0, 5)  pick across strings 0 to 5
"""
from robot import config
from robot.arrange import positions_needed


def beat_to_seconds(beat, tempo, lead_in):
    '''Converts each beat to a time in seconds'''
    return lead_in + 60 * beat / tempo


def change_chord(current, frets, when):
    '''Returns (actions, new_positions) for switching from current to the new chord'''
    new = positions_needed(frets)
    actions = []

    # Positions that aren't needed anymore are released
    for string, fret in current - new:
        actions.append((when, "release", string, fret))

    # Positions that aren't pressed yet but are needed are pressed
    for string, fret in new - current:
        actions.append((when, "press", string, fret))

    return actions, new


def schedule(song, press_time=config.PRESS_S, lead_in=config.LEAD_IN_S):
    '''Turns a songs events into a sorted list of actions'''
    current = set()
    actions = []

    for event in song["events"]:
        t = beat_to_seconds(event[0], song["tempo"], lead_in)
        event_type = event[1]

        if event_type == "shape":
            _, _, _, frets = event
            changes, current = change_chord(current, frets, t - press_time)
            actions += changes

        elif event_type == "strum":
            _, _, direction, low, high = event
            actions.append((t, "strum", direction, low, high))

        elif event_type == "mute":
            changes, current = change_chord(current, (None, None, None, None, None, None), t)
            actions += changes

    return sorted(actions)
