"""Stage 2: check the song fits the robot.

The chord hand has one solenoid per (string, fret) in config.PIN_MAP.
Open (0) and muted (None) strings don't need one.
"""


def positions_needed(frets):
    """The positions a chord has to press, as a set of (string, fret).
    C = (None, 3, 2, 0, 1, 0)  ->  {(1, 3), (2, 2), (4, 1)}
    """
    positions = {(string, fret) for string, fret in enumerate(frets) if fret}

    return positions


def check_song(song, available):
    """Raise ValueError if any chord needs a position that isn't in
    `available` (a set of (string, fret)). Name the chord in the message.
    """
    missing_chords = {}

    for event in song["events"]:
        if event[1] == "shape":
            beat, kind, name, frets = event

            missing = positions_needed(frets) - available
            if missing:
                missing_chords[name] = sorted(missing)

    if missing_chords:
        lines = [f"  {name} needs {missing}" for name, missing in missing_chords.items()]
        raise ValueError("these chords need solenoids that aren't wired yet:\n" + "\n".join(lines))


