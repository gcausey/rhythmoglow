import pygame
import math
import pyaudio

# Initialize Pygame
pygame.init()

#screen setup
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Audio Reaction Test")

#Audio variable initialization
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

#Open audio stream - arguments are the initialized audio variables
stream = p.open(format = FORMAT,
                channels =CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


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


#Draws light map as squares  and changes color of square based on certain amplitude of audio input
def draw_light_map(amplitude):
    screen.fill((0,0,0))


#initialize square values
    color = (0,0,0)
    margin = 5
    square_size = 15


#Draw lights
    
    for row in range(15):
        for col in range(15):
            if row == 0 or row == 15 or col == 0 or col == 15:
                x = col * (square_size + margin) + margin
                y = row * (square_size + margin) + margin
                pygame.draw.rect(screen, color, pygame.Rect(x, y, square_size, square_size))
                
                #Change the color of the lights based on amplitude

                if amplitude > 20:
                    new_color = (0, 255, 255)
                    for row in range(15):
                        for col in range(15):
                            if row == 0 or row == 15 or col == 0 or col == 15:
                                x = col * (square_size + margin) + margin
                                y = row * (square_size + margin) + margin
                                pygame.draw.rect(screen, new_color, pygame.Rect(x, y, square_size, square_size))

    pygame.display.flip()
    

#Clock Setup
clock = pygame.time.Clock()

running = True
amplitude = 100


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    amplitude_adjustment = get_microphone_input_level() / 50
    amplitude  = max(10, amplitude_adjustment)


    draw_light_map(amplitude)
    #print(get_microphone_input_level())
    
    #frame rate cap
    clock.tick(60)

pygame.quit()

