import sys
import pygame.midi
from constants import *


def settings_menu(WIN):
    running = True
    while running:

        # fill background color
        WIN.fill(TAN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        CLOCK.tick(FPS)
