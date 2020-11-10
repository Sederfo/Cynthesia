import pygame.midi
import pygame
import midis2events
pygame.midi.init()
input = pygame.midi.Input(3)
output = pygame.midi.Output(2)

while True:
    for event in midis2events.midis2events(input.read(40), input):
        if event.command == midis2events.NOTE_ON:
            if event.data2 != 0:
                print(f"ON %s %s" % (event.data1, event.data2))
            else:
                print(f"OFF %s %s" % (event.data1, event.data2))


