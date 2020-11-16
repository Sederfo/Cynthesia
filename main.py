import sys
import pygame.midi
from constants import *
from freeplay_menu import freeplay_menu
from record_midi_menu import record_midi_menu
from settings_menu import settings_menu

pygame.midi.init()
pygame.font.init()

# initialize screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PianoKeyGame")


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


def main_menu(WIN):
    click = False
    while True:
        WIN.fill(TAN)

        draw_button('PianoKeyGame', FONT_NAME, FONT_SIZE, BLACK, WIN, WIDTH // 2, 50)
        free_play_button = draw_button('Free Play', FONT_NAME, FONT_SIZE - 20, BLACK, WIN, WIDTH // 2, 300)
        record_midi_button = draw_button('Record MIDI', FONT_NAME, FONT_SIZE - 20, BLACK, WIN, WIDTH // 2, 375)
        settings_button = draw_button('Settings', FONT_NAME, FONT_SIZE - 20, BLACK, WIN, WIDTH // 2, 450)
        exit_button = draw_button('Exit', FONT_NAME, FONT_SIZE - 20, BLACK, WIN, WIDTH // 2, 525)

        mx, my = pygame.mouse.get_pos()

        if free_play_button.collidepoint((mx, my)) and click:
            freeplay_menu(WIN)

        if record_midi_button.collidepoint((mx, my)) and click:
            record_midi_menu(WIN)

        if settings_button.collidepoint((mx, my)) and click:
            settings_menu(WIN)

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


main_menu(WIN)
