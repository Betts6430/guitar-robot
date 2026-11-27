import pytest

from robot.parse import parse_chart

ONE_BAR = """
# a one-bar test chart
title: Test
tempo: 120
beats_per_bar: 4
pattern: D . D U

| C |
"""


def test_header():
    song = parse_chart(ONE_BAR)
    assert song["title"] == "Test"
    assert song["tempo"] == 120
    assert song["beats_per_bar"] == 4


def test_one_bar():
    assert parse_chart(ONE_BAR)["events"] == [
        (0, "shape", "C", (None, 3, 2, 0, 1, 0)),
        (0, "strum", "down", 1, 5),   # C skips the muted low E
        (2, "strum", "down", 1, 5),
        (3, "strum", "up", 1, 5),
        (4, "mute"),
    ]


def test_eighth_notes_over_two_lines():
    chart = """
title: Eighths
tempo: 90
beats_per_bar: 4
pattern: D . . . . . . U
| G |
| Em |
"""
    assert parse_chart(chart)["events"] == [
        (0, "shape", "G", (3, 2, 0, 0, 0, 3)),
        (0, "strum", "down", 0, 5),
        (3.5, "strum", "up", 0, 5),
        (4, "shape", "Em", (0, 2, 2, 0, 0, 0)),
        (4, "strum", "down", 0, 5),
        (7.5, "strum", "up", 0, 5),
        (8, "mute"),
    ]


def test_d_chord_strums_four_strings():
    chart = "title: D\ntempo: 60\nbeats_per_bar: 4\npattern: D\n| D |\n"
    strums = [e for e in parse_chart(chart)["events"] if e[1] == "strum"]
    assert strums == [(0, "strum", "down", 2, 5)]


def test_unknown_chord_is_an_error():
    chart = "title: Bad\ntempo: 60\nbeats_per_bar: 4\npattern: D\n| G | Q7 |\n"
    with pytest.raises(ValueError, match="Q7"):
        parse_chart(chart)
