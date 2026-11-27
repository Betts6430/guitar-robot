# Numbers you'll tune. Put measured values from the test rig here.

PRESS_S = 0.08     # seconds from solenoid on to string pressed (sim guess, measure it)
LEAD_IN_S = 1.0    # quiet time before the first beat so the first chord can settle

DEFAULT_SONG = "songs/demo.txt"

GRID_FRETS = (1, 2, 3, 4)   # the stationary grid covers frets 1-4

# Which GPIO number drives the solenoid at (string, fret).
# Strings: 0 = low E, 1 = A, 2 = D, 3 = G, 4 = B, 5 = high e.
# Add a line each time you wire a solenoid.
PIN_MAP = {
    (2, 2): 23,   # D string, fret 2 -> GPIO23 (pin 16), the bench test solenoid
}
