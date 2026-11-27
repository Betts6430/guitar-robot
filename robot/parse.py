"""Stage 1: chord chart text -> song.

A song is a dict:
    {"title": "Demo", "tempo": 90, "beats_per_bar": 4, "events": [...]}
"""


from robot.chords import CHORDS


def split_chart(text):
    '''Splits the song text into a dictionary, e.g.
       {"title": "hello", "tempo": "100", "beats_per_bar": "4", "chords": [...]}'''
    
    header = {}
    chords = []

    for line in text.splitlines():
        line = line.strip()

        # skip blanks and comments
        if line == "" or line.startswith("#"):
            continue

        # chord chart
        if line.startswith("|"):
            for name in line.split("|"):
                if name.strip() != "":
                    chords.append(name.strip())

        # song header info
        else:
            key, value = line.split(":", 1)
            header[key.strip()] = value.strip()

    return header, chords


def strum_range(frets):
    '''Returns a tuple of the lowest and highest strings that are strummed on a chord'''
    played = [string for string, fret in enumerate(frets) if fret is not None]
    if played:
        return played[0], played[-1]
    
    # Raise error if the strum range is empty
    raise ValueError("this chord doesn't play any strings")
    

def bar_events(bar, name, beats_per_bar, strum_pattern):
    """All the events for one bar: the chord, then a strum for each D or U.
    bar counts from 0. strum_pattern is the pattern split up, like ["D", ".", "D", "U"]."""

    if name not in CHORDS:
        raise ValueError(f"unknown chord {name} in bar {bar + 1}")
    
    frets = CHORDS[name]
    low, high = strum_range(frets)
    start = bar * beats_per_bar                        # first beat of this bar
    step_length = beats_per_bar / len(strum_pattern)   # beats between strokes

    events = [(start, "shape", name, frets)]
    for i, stroke in enumerate(strum_pattern):
        beat = start + i * step_length

        if stroke == "D":
            events.append((beat, "strum", "down", low, high))
        elif stroke == "U":
            events.append((beat, "strum", "up", low, high))
        elif stroke != ".":
            raise ValueError(f"unknown stroke {stroke} in the strum pattern")
        
    return events


def parse_chart(text):
    """Turn chord chart text into a song dict"""
    header, chords = split_chart(text)
    beats_per_bar = int(header["beats_per_bar"])
    strum_pattern = header["pattern"].split()

    events = []
    for bar, name in enumerate(chords):
        events += bar_events(bar, name, beats_per_bar, strum_pattern)
    events.append((len(chords) * beats_per_bar, "mute"))   # end of the song adds mutes

    return {
        "title": header.get("title", "Untitled"),
        "tempo": float(header["tempo"]),
        "beats_per_bar": beats_per_bar,
        "events": sorted(events),
    }


def parse_file(path):
    with open(path) as f:
        return parse_chart(f.read())
