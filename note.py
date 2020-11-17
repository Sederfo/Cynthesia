import pygame
from constants import *


def number_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number % 12]


class Note:
    def __init__(self, number, velocity, start_time, rect, is_pressed, is_white):
        self.number = number
        self.velocity = velocity
        self.ascii = number_to_note(number)
        self.start_time = start_time
        self.rect = rect
        self.is_pressed = is_pressed
        self.is_white = is_white

    def __str__(self):
        return "Note with number %s and velocity %s at time %s" % (self.number, self.velocity, self.start_time)

    def incrementHeight(self, x):
        self.rect.h += x
        self.rect.move_ip(0, -x)

    def drawNote(self, WIN):
        # WIN.blit(self.image, (self.x, self.y))
        if self.is_white:
            if self.number < 60:
                pygame.draw.rect(WIN, COLOR1, self.rect)
            else:
                pygame.draw.rect(WIN, COLOR3, self.rect)
        else:
            if self.number < 60:
                pygame.draw.rect(WIN, COLOR2, self.rect)
            else:
                pygame.draw.rect(WIN, COLOR4, self.rect)

    def moveNoteUp(self, vel):
        self.rect.move_ip(0, -vel)


