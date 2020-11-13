import sys
import pygame
import pygame.midi
from piano_keyboard import PianoKeyboard
from note import Note
from settings import *
import midis2events
from pychord import note_to_chord

pygame.font.init()


def number_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number % 12]

def draw_chord(WIN, chord):
    font = pygame.font.SysFont(FONT_NAME, 30)
    text = font.render(chord, True, BLACK, TAN)
    text_rect = text.get_rect()
    text_rect.x = 0
    WIN.blit(text, text_rect)


def freeplay_menu(WIN):
    note_vel = 2
    notes = []

    pianoKeyboard = PianoKeyboard()
    pianoKeyboard.init(0)

    notes_pressed = []
    # notes_pressed.sort()
    # print(notes_pressed)
    #
    # print(note_to_chord(notes_pressed))

    midis2events.midis2events(MIDI_INPUT.read(40), MIDI_INPUT).clear()
    running = True
    while running:
        WIN.fill(TAN)

        if len(notes_pressed)>0:
            notes_pressed.sort()
            if len(notes_pressed) == 1:
                draw_chord(WIN, notes_pressed[0])
            elif note_to_chord(notes_pressed):
                draw_chord(WIN, str(note_to_chord(notes_pressed))[2:-2])
        pianoKeyboard.draw(WIN)

        for note in notes:
            if note.is_pressed:
                note.incrementHeight(note_vel)
            else:
                note.moveNoteUp(note_vel)

            note.drawNote(WIN)

            if note.rect.y + note.rect.h + 100 < 0:
                notes.remove(note)

        for event in midis2events.midis2events(MIDI_INPUT.read(40), MIDI_INPUT):
            if event.command == midis2events.NOTE_ON:

                note_number = event.data1
                # note on
                if event.data2 != 0:
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

                    # add note number to currently pressed keys list
                    notes_pressed.append(number_to_note(note_number))

                    print(notes_pressed)

                # note off
                else:
                    # search for note in notes vector and set is_pressed to False
                    for note in notes:
                        if note.number == event.data1 and note.is_pressed:
                            note.is_pressed = False

                    print(f"OFF %s %s" % (event.data1, event.data2))
                    notes_pressed.remove(number_to_note(note_number))
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
