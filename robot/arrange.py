"""Stage 2: check the song fits the robot.

The chord hand has one solenoid per (string, fret) in config.PIN_MAP.
Open (0) and muted (None) strings don't need one.
"""


def positions_needed(frets):
    """The positions a chord has to press, as a set of (string, fret).
    C = (None, 3, 2, 0, 1, 0)  ->  {(1, 3), (2, 2), (4, 1)}
    """
    # TODO: your code here
    raise NotImplementedError("positions_needed")


def check_song(song, available):
    """Raise ValueError if any chord needs a position that isn't in
    `available` (a set of (string, fret)). Name the chord in the message."""
    # TODO: your code here
    raise NotImplementedError("check_song")
