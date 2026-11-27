from gpiozero import DigitalOutputDevice
from time import sleep, perf_counter

solenoid = DigitalOutputDevice(23)  # GPIO23 = physical pin 16, to the MOSFET gate

HOLD_S = 0.5   # seconds to hold the string down
REST_S = 1.0   # seconds between presses
PRESSES = 5

try:
    for n in range(PRESSES):
        t0 = perf_counter()
        solenoid.on()
        sleep(HOLD_S)
        solenoid.off()
        print(f"press {n + 1}: held {perf_counter() - t0:.3f} s")
        sleep(REST_S)
finally:
    solenoid.off()  # never leave a solenoid powered
