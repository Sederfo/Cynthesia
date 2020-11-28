import sys
import pygame.midi
from constants import *


def draw_button(text, font, font_size, color, surface, x, y):
    # button text
    fontobj = pygame.font.SysFont(font, font_size)
    textobj = fontobj.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x - textobj.get_width() // 2, y)

    # button rect
    button = pygame.Rect(x - (textobj.get_width() + BUTTON_PADDING) // 2, y - BUTTON_PADDING // 2,
                         textobj.get_width() + BUTTON_PADDING, textobj.get_height() + BUTTON_PADDING)
    pygame.draw.rect(surface, WHITE, button)

    surface.blit(textobj, textrect)

    return button


def settings_menu(WIN):
    running = True
    insert_text = False
    while running:

        # fill background color
        WIN.fill(TAN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    insert_text = True;
                    print("P")

        while insert_text:
            WIN.fill(WHITE)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        insert_text = False

        pygame.display.update()
        CLOCK.tick(FPS)
