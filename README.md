Go to https://betts6430.github.io/guitar-robot/ to check the sim out


# guitarbot

Robot guitar, Phase 1: play chord charts with a stationary solenoid grid
and a pick hand. Runs on a Raspberry Pi 5.

## How it fits together

```
songs/demo.txt --parse--> Song (events) --arrange--> checked --schedule--> Actions --play--> hardware
```

| File | Stage | Status |
| --- | --- | --- |
| `robot/events.py` | The event format every stage shares | Done |
| `robot/config.py` | Timings, grid frets, GPIO pin map | Done, numbers to tune |
| `robot/chords.py` | Chord name -> frets | Done, add your own |
| `robot/parse.py` | Chord chart text -> events | **Yours** |
| `robot/arrange.py` | Check every chord fits the wired grid | **Yours** |
| `robot/schedule.py` | Events in beats -> actions in seconds | **Yours** (`Action` given) |
| `robot/play.py` | Command line + timing loop | Glue done, **`run_timeline` yours** |
| `robot/hardware.py` | Dry-run and real backends | Dry run done, **`PiHardware` yours** |
| `tests/` | Checks the rules in each file's docstring | Done |
| `bench/` | One-off hardware tests | Done |

Each file you write starts with its rules in the docstring. The tests check
exactly those rules, so read the docstring, then the test, then write the code.

## Suggested order

1. `pip install -r requirements.txt`, then `pytest`. All 13 tests fail at
   first: that's your to-do list.
2. `arrange.positions_needed`: the shortest one. `pytest tests/test_arrange.py`
3. `parse.parse_chart`: `pytest tests/test_parse.py`
4. `schedule.schedule`: `pytest tests/test_schedule.py`
5. `play.run_timeline`, then `python -m robot.play --dry-run`. This runs the
   whole song on your laptop or the Pi, printing instead of moving.
6. `python -m robot.play --list` prints every event and action, which helps
   when a timing looks wrong.
7. `hardware.PiHardware`: start with press, release and all_off. Use
   `bench/solenoid_test.py` to check the wiring first.

## Choices already made (change them if you disagree)

- Strings are 0-5 from low E to high e, like a chord chart (`x32010` = C).
- Beats count from 0. Bar 1 starts at beat 0.0.
- A strum covers the lowest played string up to high e, so x strings are
  skipped (D7 in the brief). No muting actuator.
- A Mute releases every finger.
- New chords are pressed `PRESS_S` before their beat; strums fire on the beat.

## Pin budget

The 8 basic open chords (C A G E D Am Em Dm) need 12 solenoid positions.
Everything in `chords.py` needs 18. The Pi has 24 free GPIO pins once I2C
(GPIO2 and GPIO3) is taken by the servo board, so no expander is needed.
