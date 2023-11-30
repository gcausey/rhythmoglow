import time
from rpi_ws281x import *
import argparse

LED_COUNT      = 300     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def pulse(strip, color, pulse_duration=5, steps=100):
    """Creates a pulsing effect by gradually increasing and decreasing brightness."""
    for i in range(steps):
        brightness = int((1 - abs((i % (steps // 2)) - (steps // 4)) / (steps // 4)) * 255)
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, Color(int(color >> 16) * brightness // 255, int((color >> 8) & 0xFF) * brightness // 255, int(color & 0xFF) * brightness // 255))
        strip.show()
        time.sleep(pulse_duration / steps)

if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    while True:
        pulse(strip, Color(255, 0, 0))

