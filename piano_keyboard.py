import itertools
from constants import *


def create_rect(width, height, border, color, border_color):
    surf = pygame.Surface((width + border * 2, height + border * 2), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (border, border, width, height), 0)
    for i in range(1, border):
        pygame.draw.rect(surf, border_color, (border - i, border - i, width + 5, height + 5), 1)
    return surf


class PianoKeyboard:
    def __init__(self):
        self.keys = []

    # more like a struct
    class KeyCoords:
        def __init__(self, x, width, note_number, is_white):
            self.x = x
            self.width = width
            self.note_number = note_number
            self.is_white = is_white

    def init(self):
        black_note_pattern = [1, 1, 0, 1, 1, 1, 0]
        note_nr = 0

        bn_iter = itertools.cycle(black_note_pattern)

        for i in range(128):
            self.keys.append(-1)

        # assign white keys to keys[] list
        for i in range(NR_WHITE_NOTES):
            temp = self.KeyCoords(i * (WIDTH // NR_WHITE_NOTES), WIDTH // NR_WHITE_NOTES, note_nr, True)
            self.keys[note_nr] = temp

            note_nr += 1
            note_nr = note_nr + next(bn_iter)

        # assign black keys to keys[], they are the remaining -1 elements
        for i in range(128):
            if self.keys[i] == -1:
                # print("%s" % (self.keys[i]))
                temp = self.KeyCoords(self.keys[i - 1].x + 10, WIDTH // 100, self.keys[i + 1].note_number - 1, False)
                self.keys[i] = temp

    def draw(self, WIN, notes_pressed_int):
        # draw white keys first
        white_note_surface = create_rect(WIDTH // NR_WHITE_NOTES, WHITE_NOTE_HEIGHT, 3, WHITE, BLACK)

        for i in range(NR_WHITE_NOTES):
            WIN.blit(white_note_surface, (i * (WIDTH // NR_WHITE_NOTES), HEIGHT - WHITE_NOTE_HEIGHT))

        # surface for a pressed key
        white_note_surface_pressed1 = create_rect(WIDTH // NR_WHITE_NOTES, WHITE_NOTE_HEIGHT, 3, LIGHTORANGE, BLACK)
        white_note_surface_pressed2 = create_rect(WIDTH // NR_WHITE_NOTES, WHITE_NOTE_HEIGHT, 3, LIGHTBLUE, BLACK)
        for i in notes_pressed_int:
            if self.keys[i].is_white:
                if i >= 60:
                    WIN.blit(white_note_surface_pressed1, (self.keys[i].x, HEIGHT - WHITE_NOTE_HEIGHT))
                else:
                    WIN.blit(white_note_surface_pressed2, (self.keys[i].x, HEIGHT - WHITE_NOTE_HEIGHT))

        # draw black keys over them
        black_note_surface = create_rect(WIDTH // 150, BLACK_NOTE_HEIGHT, 3, BLACK, BLACK)
        # check for black keys and their x coordinate
        for i in range(128):
            if not self.keys[i].is_white:
                x = self.keys[i].x
                WIN.blit(black_note_surface, (x, HEIGHT - WHITE_NOTE_HEIGHT))

        black_note_surface_pressed1 = create_rect(WIDTH // 150, BLACK_NOTE_HEIGHT, 3, AUTUMNORANGE, BLACK)
        black_note_surface_pressed2 = create_rect(WIDTH // 150, BLACK_NOTE_HEIGHT, 3, BLUE, BLACK)

        for i in notes_pressed_int:
            if not self.keys[i].is_white:
                if i >= 60:
                    WIN.blit(black_note_surface_pressed1, (self.keys[i].x, HEIGHT - WHITE_NOTE_HEIGHT))
                else:
                    WIN.blit(black_note_surface_pressed2, (self.keys[i].x, HEIGHT - WHITE_NOTE_HEIGHT))
