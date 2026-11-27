from robot.chords import CHORDS
from robot.schedule import schedule


def rounded(actions):
    """Round the times so tiny float differences don't fail a test."""
    return [(round(a[0], 6),) + a[1:] for a in actions]


def test_em_to_am_then_mute():
    # 60 BPM = 1 second per beat, so the times are easy to check.
    song = {"title": "Test", "tempo": 60, "beats_per_bar": 4, "events": [
        (0, "shape", "Em", CHORDS["Em"]),   # presses (1,2) and (2,2)
        (0, "strum", "down", 0, 5),
        (2, "shape", "Am", CHORDS["Am"]),   # presses (2,2), (3,2) and (4,1)
        (2, "strum", "down", 1, 5),
        (4, "mute"),
    ]}
    assert rounded(schedule(song, press_time=0.1, lead_in=1.0)) == [
        (0.9, "press", 1, 2),
        (0.9, "press", 2, 2),
        (1.0, "strum", "down", 0, 5),
        (2.9, "press", 3, 2),     # (2,2) is in both chords, so it stays down
        (2.9, "press", 4, 1),
        (2.9, "release", 1, 2),   # not in Am
        (3.0, "strum", "down", 1, 5),
        (5.0, "release", 2, 2),
        (5.0, "release", 3, 2),
        (5.0, "release", 4, 1),
    ]


def test_tempo_sets_the_beat_length():
    song = {"title": "Test", "tempo": 120, "beats_per_bar": 4, "events": [(1, "strum", "up", 0, 5)]}
    assert rounded(schedule(song, press_time=0.1, lead_in=0)) == [(0.5, "strum", "up", 0, 5)]


def test_same_chord_twice_does_nothing_the_second_time():
    song = {"title": "Test", "tempo": 60, "beats_per_bar": 4, "events": [
        (0, "shape", "E", CHORDS["E"]),
        (4, "shape", "E", CHORDS["E"]),
    ]}
    assert rounded(schedule(song, press_time=0.1, lead_in=1.0)) == [
        (0.9, "press", 1, 2),
        (0.9, "press", 2, 2),
        (0.9, "press", 3, 1),
    ]
