import math
import pyaudio
import time
from rpi_ws281x import *

LED_COUNT      = 300     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def pulse(strip, color, pulse_duration):
    """Creates a pulsing effect by gradually increasing and decreasing brightness."""
    steps = 100
    for i in range(steps):
        brightness = int((1 - abs((i % (steps // 2)) - (steps // 4)) / (steps // 4)) * 255)
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, Color(int(color >> 16) * brightness // 255, int((color >> 8) & 0xFF) * brightness // 255, int(color & 0xFF) * brightness // 255))
        strip.show()
        time.sleep(pulse_duration / steps)

    for j in range(strip.numPixels()):
        strip.setPixelColor(j, Color(0, 0, 0))
    strip.show()

#Audio variable initialization
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

#Open audio stream - arguments are the initialized audio variables
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)


#root mean sqaured (rms) is the average height of the sound wave in a period of time
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

    pulsing = False

    while True:

       amplitude_adjustment = get_microphone_input_level() / 50
       amplitude  = max(10, amplitude_adjustment)

       if amplitude > threshold and not pulsing:
           pulse_duration = 3
           pulse(strip, Color(255, 0, 0), pulse_duration)
           pulsing = True

       if amplitude <= threshold and pulsing:
           pulsing = False
