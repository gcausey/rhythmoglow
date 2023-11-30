import math
import pyaudio
import time
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 41400

RECORD_SECONDS = 10
OUTPUT_FILE = "recorded_audio.wav"

pyaud = pyaudio.PyAudio()

stream = pyaud.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)

print("Recording...")

frames = []

# Record audio data
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop and close the stream
stream.stop_stream()
stream.close()
pyaud.terminate()

# Save recorded audio to a WAV file
with wave.open(OUTPUT_FILE, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaud.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved to '{OUTPUT_FILE}'")


