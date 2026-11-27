"""Stage 1: chord chart text -> song.

A song is a dict:
    {"title": "Demo", "tempo": 90, "beats_per_bar": 4, "events": [...]}

Each event is a tuple that starts with its beat (the first beat is 0):
    (0, "shape", "C", (None, 3, 2, 0, 1, 0))   hold this chord
    (0, "strum", "down", 1, 5)                 strum strings 1 to 5
    (4, "mute")                                let go of every string
Strings go from 0 (low E) to 5 (high e). In frets, None means muted (x).

Rules (tests/test_parse.py checks them):
1. "key: value" lines set title, tempo, beats_per_bar and pattern.
   Skip blank lines and lines starting with #.
2. Lines starting with | hold bars, one chord per bar.
   Bars carry on from one line to the next.
3. Each bar starts with a shape event, frets taken from CHORDS.
   An unknown chord raises ValueError with the chord's name in it.
4. The pattern splits each bar into equal slots: D = down, U = up, . = rest.
   Slot i of bar b is at beat  b * beats_per_bar + i * beats_per_bar / len(slots)
5. A strum goes from the lowest string the chord uses up to string 5.
6. After the last bar, add a mute where the next bar would start.
7. Return the events sorted (sorted() puts them in time order for you).
"""
from robot.chords import CHORDS


def parse_chart(text):
    song = {"title"}




    raise NotImplementedError("parse_chart")


def parse_file(path):
    with open(path) as f:
        return parse_chart(f.read())
