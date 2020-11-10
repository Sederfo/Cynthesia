import pygame
from settings import *


def number_to_note(number):
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number % 12]


class Note:
    def __init__(self, number, velocity, timestamp, x, y, rect, is_pressed, is_white):
        self.number = number
        self.velocity = velocity
        self.ascii = number_to_note(number)
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.rect = rect
        self.is_pressed = is_pressed
        self.is_white=is_white

    def __str__(self):
        return "Note with number %s and velocity %s at time %s" % (self.number, self.velocity, self.timestamp)

    def incrementHeight(self, x):
        self.rect.h += x
        self.rect.move_ip(0, -x)

    def drawNote(self, WIN):
        # WIN.blit(self.image, (self.x, self.y))
        if self.is_white:
            pygame.draw.rect(WIN, LIGHTBLUE, self.rect)
        else:
            pygame.draw.rect(WIN, BLUE, self.rect)

    def moveNoteUp(self, vel):
        self.rect.move_ip(0, -vel)

    def moveNoteDown(self, vel):
        self.y += vel
