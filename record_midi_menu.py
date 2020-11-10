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

    note_pressed = []
    for i in range(129):
        note_pressed.append(0)

    midis2events.midis2events(MIDI_INPUT.read(40), MIDI_INPUT).clear()
    running = True
    while running:
        WIN.fill(TAN)
        pianoKeyboard.draw(WIN)

        for note in notes:
            if note.is_pressed:
                note.incrementHeight(note_vel)
                note.drawNote(WIN)
            else:
                note.moveNoteUp(note_vel)
                note.drawNote(WIN)

        for event in midis2events.midis2events(MIDI_INPUT.read(40), MIDI_INPUT):
            if event.command == midis2events.NOTE_ON:
                note_number = event.data1
                if event.data2 != 0:  # note on
                    note_pressed[note_number] = 1
                    print(f"ON %s %s" % (event.data1, event.data2))

                    if pianoKeyboard.keys[note_number].is_white:
                        WHITE_NOTE_RECT = pygame.Rect((pianoKeyboard.keys[note_number].x + 3, HEIGHT - 100),
                                                      (WIDTH // NR_WHITE_NOTES, 0))
                        note = Note(number=note_number, velocity=event.data2, timestamp=event.timestamp,
                                    x=pianoKeyboard.keys[note_number].x + 3,  # +3 for padding adjustment
                                    y=HEIGHT - 150, rect=WHITE_NOTE_RECT, is_pressed=True, is_white=True)
                    else:
                        BLACK_NOTE_RECT = pygame.Rect((pianoKeyboard.keys[note_number].x, HEIGHT - 100),
                                                      (WIDTH // 100, 0))
                        note = Note(number=note_number, velocity=event.data2, timestamp=event.timestamp,
                                    x=pianoKeyboard.keys[note_number].x,
                                    y=HEIGHT - 150, rect=BLACK_NOTE_RECT, is_pressed=True, is_white=False)

                    # add note to keys list
                    notes.append(note)

                else:  # note off
                    # search for note in notes vector and set is_pressed to False
                    for note in notes:
                        if note.number == event.data1 and note.is_pressed:
                            note.is_pressed = False
                    note_pressed[note_number] = 0
                    print(f"OFF %s %s" % (event.data1, event.data2))
            # elif event.command == midis2events.NOTE_OFF:
            #     note_pressed[event.data1] = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        CLOCK.tick(FPS)
