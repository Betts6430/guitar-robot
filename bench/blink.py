from gpiozero import LED
from time import sleep

led = LED(17)  # GPIO17 = physical pin 11

for i in range(10):
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)

print("Done")
