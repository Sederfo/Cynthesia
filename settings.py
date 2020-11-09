import pygame
import pygame.midi

TITLE = "PianoKeyGame"
WIDTH = 1280
HEIGHT = 720
FPS = 60
FONT_NAME = "arial"
FONT_SIZE = 50
BUTTON_PADDING = 20

NR_WHITE_NOTES = 75
NR_BLACK_NOTES = 53
LOWEST_NOTE = None
HIGHEST_NOTE = None

CLOCK = pygame.time.Clock()

# load images
PIANO_KEYBOARD = pygame.image.load("graphics/pianoKeyboard.png")
PIANO_KEYBOARD = pygame.transform.scale(PIANO_KEYBOARD, (WIDTH, 120))
PIANO_NOTE_WHITE = pygame.image.load("graphics/white_note.png")
PIANO_NOTE_WHITE = pygame.transform.scale(PIANO_NOTE_WHITE, (WIDTH // NR_WHITE_NOTES, 80))
PIANO_NOTE_BLACK = pygame.image.load("graphics/black_note.png")
PIANO_NOTE_BLACK = pygame.transform.scale(PIANO_NOTE_BLACK, (WIDTH // 100, 80))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
TAN = (255, 255, 190)
BGCOLOR = LIGHTBLUE