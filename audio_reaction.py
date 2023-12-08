# Group 6
# Final Script

import math
import pyaudio
import time
import random
from rpi_ws281x import *

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 150
LED_INVERT = False
LED_CHANNEL = 0

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def random_integer():
    return random.randint(0, 255)

def random_color():
    return Color(random_integer(), random_integer(), random_integer())

def contrast(previous):
    r = (previous >> 16) + random.randint(-75, 75)
    g = (previous >> 8 & 0xFF) + random.randint(-75, 75)
    b = (previous & 0xFF) + random.randint(-75, 75)

    min_threshold = 100
    if all(c < min_threshold for c in (r, g, b)):
        rand_index = random.randint(0, 2)
        if rand_index == 0:
            r = random.randint(min_threshold, 255)
        elif rand_index == 1:
            g = random.randint(min_threshold, 255)
        else:
            b = random.randint(min_threshold, 255)

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return Color(r, g, b)

def strip_on(strip, previous):
    color = contrast(previous)
    for j in range(strip.numPixels()):
        strip.setPixelColor(j, color)
    strip.show()

def strip_off(strip):
    for j in range(strip.numPixels()):
        strip.setPixelColor(j, Color(0, 0, 0))
    strip.show()

def get_microphone_input_level():
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
        samples = [int.from_bytes(data[i:i + 2], byteorder="little", signed=True) for i in range(0, len(data), 2)]
        rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples))
        return rms
    except IOError as ex:
        print("Error reading audio data: {}".format(ex))
        return 0.0

if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    threshold = 40

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)

    while True:

       amplitude_adjustment = get_microphone_input_level() / 50
       amplitude  = max(10, amplitude_adjustment)

       previous = Color(0, 0, 0)

       if amplitude > threshold:
            previous = strip_on(strip, previous)
       else:
            strip_off(strip)
