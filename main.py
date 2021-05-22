import sys
import pygame.midi
from constants import *
from freeplay_menu import freeplay_menu
from record_midi_menu import record_midi_menu
from settings_menu import settings_menu

from particle import Particle
import random

pygame.midi.init()
pygame.font.init()

# initialize screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cynthesia")


def draw_button(text, font, font_size, color, surface, x, y, button_color):
    # button text
    fontobj = pygame.font.SysFont(font, font_size)
    textobj = fontobj.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x - textobj.get_width() // 2, y)

    # button rect
    button = pygame.Rect(x - (textobj.get_width() + BUTTON_PADDING) // 2, y - BUTTON_PADDING // 2,
                         textobj.get_width() + BUTTON_PADDING, textobj.get_height() + BUTTON_PADDING)
    pygame.draw.rect(surface, button_color, button)

    surface.blit(textobj, textrect)

    return button


def draw_text(WIN, text, font_size, x, y, text_color, center_vertically=True, center_horizontally=True):
    font = pygame.font.SysFont(FONT_NAME, font_size)
    text = font.render(text, True, text_color)
    text_rect = text.get_rect()

    if center_horizontally:
        text_rect.x = x - text_rect.w // 2  # this centers the text horizontally
    else:
        text_rect.x = x

    if center_vertically:
        text_rect.y = y - text_rect.h // 2  # this centers the text vertically
    else:
        text_rect.y = y

    WIN.blit(text, text_rect)


def main_menu(WIN):
    click = False
    for i in range(0,pygame.midi.get_count()):
        print(pygame.midi.get_device_info(i))
        
    while True:
        WIN.fill(BGCOLOR)

        # draw top bar
        pygame.draw.rect(WIN, WHITE, (0, 0, WIDTH, HEIGHT // 10))
        pygame.draw.rect(WIN, BLACK, (0, HEIGHT // 10, WIDTH, 2))

        # draw bottom bar
        pygame.draw.rect(WIN, WHITE, (0, HEIGHT-HEIGHT//20, WIDTH, HEIGHT // 20))
        pygame.draw.rect(WIN, BLACK, (0, HEIGHT-HEIGHT // 20, WIDTH, 2))

        # draw text in top bar
        draw_text(WIN, "Cynthesia", 50 * HEIGHT//720, WIDTH // 2, HEIGHT // 10 // 2, BLACK, True, True)

        # draw text in bottom bar
        draw_text(WIN, "  Version 1.0 ", 15 * HEIGHT // 720, 0, HEIGHT - HEIGHT // 20 // 2, BLACK, True, False)

        # draw buttons
        free_play_button = draw_button('Free Play', FONT_NAME, 30 * HEIGHT//720, FONTCOLOR, WIN, WIDTH // 2, 300, BUTTONCOLOR)
        record_midi_button = draw_button('Record MIDI', FONT_NAME, 30 * HEIGHT//720, FONTCOLOR, WIN, WIDTH // 2, 375, BUTTONCOLOR)
        exit_button = draw_button('Exit', FONT_NAME, 30 * HEIGHT//720, FONTCOLOR, WIN, WIDTH // 2, 450, BUTTONCOLOR)

        # check for mouse position and button clicking
        mx, my = pygame.mouse.get_pos()

        if free_play_button.collidepoint((mx, my)):
            draw_button('Free Play', FONT_NAME, 30 * HEIGHT//720, FONTCOLOR, WIN, WIDTH // 2, 300, CREAM)
            if click:
                freeplay_menu(WIN)

        if record_midi_button.collidepoint((mx, my)):
            draw_button('Record MIDI', FONT_NAME, 30 * HEIGHT//720, FONTCOLOR, WIN, WIDTH // 2, 375, CREAM)
            if click:
                record_midi_menu(WIN)

        if exit_button.collidepoint((mx, my)):
            exit_button = draw_button('Exit', FONT_NAME, 30 * HEIGHT//720, FONTCOLOR, WIN, WIDTH // 2, 450, CREAM)
            if click:
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


main_menu(WIN)
