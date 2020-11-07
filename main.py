import sys
import pygame
import pygame.midi
import itertools
from settings import *

pygame.midi.init()
pygame.font.init()

CLOCK = pygame.time.Clock()

# initialize midi input
MIDI_INPUT = pygame.midi.Input(1)

# initialize screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PianoKeyGame")


NR_WHITE_NOTES = 75
NR_BLACK_NOTES = 53
LOWEST_NOTE = None
HIGHEST_NOTE = None

# load images
PIANO_KEYBOARD = pygame.image.load("graphics/pianoKeyboard.png")
PIANO_KEYBOARD = pygame.transform.scale(PIANO_KEYBOARD, (WIDTH, 120))
PIANO_NOTE_WHITE = pygame.image.load("graphics/white_note.png")
PIANO_NOTE_WHITE = pygame.transform.scale(PIANO_NOTE_WHITE, (WIDTH // NR_WHITE_NOTES, 80))
PIANO_NOTE_BLACK = pygame.image.load("graphics/black_note.png")
PIANO_NOTE_BLACK = pygame.transform.scale(PIANO_NOTE_BLACK, (WIDTH // 100, 80))



def number_to_note(number):
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number % 12]


class Note:
    def __init__(self, note_number, velocity, timestamp, x, y, note_img):
        self.note_number = note_number
        self.velocity = velocity
        self.note_name = number_to_note(note_number)
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.note_img = note_img

    def __str__(self):
        return "Note with number %s and velocity %s at time %s" % (self.note_number, self.velocity, self.timestamp)

    def drawNote(self, WIN):
        WIN.blit(self.note_img, (self.x, self.y))

    def moveNoteUp(self, vel):
        self.y -= vel


class PianoKeyboard:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT
        self.note_width = WIDTH // 52
        self.keys = []
        self.white_notes = []
        self.lowest_note = None

    class KeyCoords:
        def __init__(self, x, width, note_number, is_white):
            self.x = x
            self.width = width
            self.note_number = note_number
            self.is_white = is_white

    def init(self, lowest_note):
        black_note_pattern = [1, 1, 0, 1, 1, 1, 0]
        note_nr = lowest_note

        bn_iter = itertools.cycle(black_note_pattern)

        for i in range(128):
            self.keys.append(-1)

        #assign white keys to keys[] list
        for i in range(NR_WHITE_NOTES):
            #print(note_nr)
            temp = self.KeyCoords(i * (WIDTH // NR_WHITE_NOTES), WIDTH // NR_WHITE_NOTES, note_nr, True)
            self.keys[note_nr]=temp

            note_nr += 1
            note_nr = note_nr + next(bn_iter)

        #assign black keys to keys[], they are the remaining -1 elements
        for i in range(128):
            if self.keys[i]==-1:
                temp = self.KeyCoords(self.keys[i - 1].x + 10, WIDTH // 100, self.keys[i + 1].note_number - 1, False)
                self.keys[i]=temp

        for i in range(128):
            print(f"%s is_white: %s" % (self.keys[i].note_number, self.keys[i].is_white))




    def create_rect(self, width, height, border, color, border_color):
        surf = pygame.Surface((width + border * 2, height + border * 2), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (border, border, width, height), 0)
        for i in range(1, border):
            pygame.draw.rect(surf, border_color, (border - i, border - i, width + 5, height + 5), 1)
        return surf

    def draw(self):
        #draw white keys first
        white_note_surface = self.create_rect(WIDTH // NR_WHITE_NOTES, 100, 3, WHITE, BLACK)
        for i in range(75):
            WIN.blit(white_note_surface, (i * (WIDTH // NR_WHITE_NOTES), HEIGHT - 100))

        #draw black keys over them
        black_note_surface = self.create_rect(WIDTH//150, 50, 3, BLACK, BLACK)
        #check for black keys and their x coordinate
        for i in range(128):
            if not self.keys[i].is_white:
                x = self.keys[i].x
                WIN.blit(black_note_surface, (x, HEIGHT-100))




def draw_button(text, font, font_size, color, surface, x, y):
    # button text
    fontobj = pygame.font.SysFont(font, font_size)
    textobj = fontobj.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x - textobj.get_width() // 2, y)

    # button rect
    button = pygame.Rect(x - (textobj.get_width() + BUTTON_PADDING) // 2, y - BUTTON_PADDING // 2,
                         textobj.get_width() + BUTTON_PADDING, textobj.get_height() + BUTTON_PADDING)
    pygame.draw.rect(WIN, WHITE, button)

    surface.blit(textobj, textrect)

    return button


def main_menu():
    while True:

        WIN.fill(TAN)
        draw_button('Main Menu', FONT_NAME, FONT_SIZE, BLACK, WIN, WIDTH // 2, 50)
        free_play_button = draw_button('Free Play', FONT_NAME, FONT_SIZE - 20, BLACK, WIN, WIDTH // 2, 300)
        exit_button = draw_button('Exit', FONT_NAME, FONT_SIZE - 20, BLACK, WIN, WIDTH // 2, 375)

        mx, my = pygame.mouse.get_pos()

        if free_play_button.collidepoint((mx, my)) and click:
            freeplay_menu()

        if exit_button.collidepoint((mx, my)) and click:
            sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        CLOCK.tick(FPS)


def freeplay_menu():
    note_vel = 7

    notes = []

    pianoKeyboard = PianoKeyboard()
    pianoKeyboard.init(0)

    running = True
    while running:

        WIN.fill([255, 255, 190])

        for note in notes:
            note.moveNoteUp(note_vel)
            note.drawNote(WIN)
            if note.y + PIANO_NOTE_WHITE.get_height() <= 0:
                notes.remove(note)

        pianoKeyboard.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    running = False
                running = False

        if MIDI_INPUT.poll():  # if there is data from the midi input
            event = MIDI_INPUT.read(1)  # read the data
            if event[0][0][2] != 0:  # if note is pressed
                # instantiate note
                note_number = event[0][0][1]
                note_velocity = event[0][0][2]
                timestamp = event[0][1]
                if pianoKeyboard.keys[note_number].is_white:
                    note = Note(note_number, note_velocity, timestamp,
                                pianoKeyboard.keys[note_number].x + 3,
                                HEIGHT - 150, PIANO_NOTE_WHITE)
                else:
                    note = Note(note_number, note_velocity, timestamp,
                                pianoKeyboard.keys[note_number].x,
                                HEIGHT - 150, PIANO_NOTE_BLACK)

                # add note to keys list
                notes.append(note)

                print(note)

        pygame.display.update()
        CLOCK.tick(FPS)


main_menu()
