import pygame.midi
import pygame
import midis2events
from settings import *

white_note_surf = pygame.Surface((100, 100))

white_note_rect = pygame.Rect((500, 500), (50, 200))

WIN = pygame.display.set_mode((1000, 1000))

WIN.fill(TAN)
pygame.draw.rect(WIN, BLACK, white_note_rect)

x=[]

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                WIN.fill(TAN)
                #white_note_rect = white_note_rect.inflate(0, 50)\
                #white_note_rect.y-=10
                white_note_rect.move_ip(0, -1)
                pygame.draw.rect(WIN, BLACK, white_note_rect)
                x.append(1)
            if event.key == pygame.K_d:
                WIN.fill(TAN)
                white_note_rect.h+=10
                white_note_rect.move_ip(0, -10)
                pygame.draw.rect(WIN, BLACK, white_note_rect)
                x.remove(1)

    pygame.display.update()



