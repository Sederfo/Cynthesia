import sys
import pygame
import pygame.midi
from piano_keyboard import PianoKeyboard
from note import Note
from settings import *
import midis2events


def record_midi_menu(WIN):
    note_vel = 5
    notes = []

    pianoKeyboard = PianoKeyboard()
    pianoKeyboard.init(0)

    midis2events.midis2events(MIDI_INPUT.read(40), MIDI_INPUT).clear()
    running = True
    while running:
        WIN.fill(TAN)

        for note in notes:
            note.moveNoteUp(note_vel)
            note.drawNote(WIN)
            if note.y + PIANO_NOTE_WHITE.get_height() <= 0:
                notes.remove(note)

        pianoKeyboard.draw(WIN)

        for event in midis2events.midis2events(MIDI_INPUT.read(40), MIDI_INPUT):
            if event.command == midis2events.NOTE_ON:
                if event.data2 != 0:  # note on
                    print(f"ON %s %s" % (event.data1, event.data2))
                    note_number = event.data1
                    if pianoKeyboard.keys[note_number].is_white:
                        note = Note(number=event.data1, velocity=event.data2, timestamp=event.timestamp,
                                    x=pianoKeyboard.keys[note_number].x + 3,  # +3 for padding adjustment
                                    y=HEIGHT - 150, image=PIANO_NOTE_WHITE)
                    else:
                        note = Note(number=event.data1, velocity=event.data2, timestamp=event.timestamp,
                                    x=pianoKeyboard.keys[note_number].x,
                                    y=HEIGHT - 150, image=PIANO_NOTE_BLACK)

                    # add note to keys list
                    notes.append(note)

                else:  # note off
                    print(f"OFF %s %s" % (event.data1, event.data2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        CLOCK.tick(FPS)
