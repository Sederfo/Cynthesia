import sys

import pygame
import pygame.midi
from piano_keyboard import PianoKeyboard
from note import Note
from settings import *

pygame.midi.init()

# initialize midi input
MIDI_INPUT = pygame.midi.Input(1)


def freeplay_menu(WIN):
    note_vel = 5

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

        pianoKeyboard.draw(WIN)

        if MIDI_INPUT.poll():  # if there is data from the midi input
            event = MIDI_INPUT.read(1)  # read the data
            if event[0][0][2] != 0:  # if note is pressed
                # instantiate note
                note_number = event[0][0][1]
                note_velocity = event[0][0][2]
                timestamp = event[0][1]
                if pianoKeyboard.keys[note_number].is_white:
                    note = Note(note_number, note_velocity, timestamp,
                                pianoKeyboard.keys[note_number].x + 3,  # +3 for padding adjustment
                                HEIGHT - 150, PIANO_NOTE_WHITE)
                else:
                    note = Note(note_number, note_velocity, timestamp,
                                pianoKeyboard.keys[note_number].x,
                                HEIGHT - 150, PIANO_NOTE_BLACK)

                # add note to keys list
                notes.append(note)
                print(note)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    running = False
                MIDI_INPUT.close()
                running = False

        pygame.display.update()
        CLOCK.tick(FPS)
