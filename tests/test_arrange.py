import pytest

from robot.arrange import check_song, positions_needed
from robot.chords import CHORDS


def test_c_chord():
    assert positions_needed(CHORDS["C"]) == {(1, 3), (2, 2), (4, 1)}


def test_open_and_muted_strings_need_nothing():
    assert positions_needed((None, None, 0, 0, 0, 0)) == set()


def test_f_barre_presses_all_six_strings():
    assert positions_needed(CHORDS["F"]) == {(0, 1), (1, 3), (2, 3), (3, 2), (4, 1), (5, 1)}


def test_song_that_fits():
    song = {"events": [(0, "shape", "Em", CHORDS["Em"]), (0, "strum", "down", 0, 5)]}
    check_song(song, {(1, 2), (2, 2)})   # should not raise


def test_song_that_does_not_fit():
    song = {"events": [(0, "shape", "Am", CHORDS["Am"])]}
    with pytest.raises(ValueError, match="Am"):
        check_song(song, {(2, 2)})
