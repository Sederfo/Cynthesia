import pygame
import pygame.midi

TITLE = "PianoKeyGame"
WIDTH = 1280
HEIGHT = 720
FPS = 60
FONT_NAME = "arial"
FONT_SIZE = 50
BUTTON_PADDING = 20


def set_resolution(width, height):
    print("param names %s %s" % (width, height))
    global WIDTH
    WIDTH = width
    global HEIGHT
    HEIGHT = height
    print("global names %s %s" % (WIDTH, HEIGHT))


NR_WHITE_NOTES = 75
NR_BLACK_NOTES = 53

WHITE_NOTE_HEIGHT = HEIGHT // 7
BLACK_NOTE_HEIGHT = WHITE_NOTE_HEIGHT // 2

CLOCK = pygame.time.Clock()

# initialize midi input
pygame.midi.init()
MIDI_INPUT = pygame.midi.Input(3)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (49, 71, 158)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
TAN = (255, 255, 190)
AUTUMNORANGE = (235, 64, 52)
ORANGE = (247, 158, 79)
GREY = (213, 223, 237)

COLOR1 = LIGHTBLUE
COLOR2 = BLUE
COLOR3 = ORANGE
COLOR4 = AUTUMNORANGE
