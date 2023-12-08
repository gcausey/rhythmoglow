# Group 6
# LED Test Scipt

import math
import pyaudio
import time
from rpi_ws281x import *

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 150
LED_INVERT = False
LED_CHANNEL = 0

def pulse(strip, color, pulse_duration=5, steps=100):
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

