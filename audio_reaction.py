import math
import pyaudio
import time
import random
from rpi_ws281x import *

LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 65
LED_INVERT = False
LED_CHANNEL = 0

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def random_int():
    return random.randint(0, 255)

def strip_on(strip):
    r = random_int()
    g = random_int()
    b = random_int()
    color = Color(r, g, b)
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

    threshold = 20

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)

    while True:

       amplitude_adjustment = get_microphone_input_level() / 50
       amplitude  = max(10, amplitude_adjustment)

       if amplitude > threshold:
            strip_on(strip)
       else:
            strip_off(strip)
