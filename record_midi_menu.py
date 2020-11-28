import sys
import pygame.midi
from piano_keyboard import PianoKeyboard
from note import Note
from constants import *
import midis2events
import time as t
from midiutil.MidiFile import MIDIFile
from pychord import note_to_chord
import re
import random
from particle import Particle


def number_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number % 12]


def draw_text(WIN, text, font_size, x, y, text_color, center_vertically, center_horizontally, x_right=False,
              y_down=False):
    font = pygame.font.SysFont(FONT_NAME, font_size)
    text = font.render(text, True, text_color)
    text_rect = text.get_rect()

    if center_horizontally:
        text_rect.x = x - text_rect.w // 2  # this centers the text horizontally
    elif x_right:
        text_rect.x = x - text_rect.w
    else:
        text_rect.x = x

    if center_vertically:
        text_rect.y = y - text_rect.h // 2  # this centers the text vertically
    elif y_down:
        text_rect.y = y - text_rect.h
    else:
        text_rect.y = y

    WIN.blit(text, text_rect)


def draw_button(text, font, font_size, color, surface, x, y):
    # button text
    fontobj = pygame.font.SysFont(font, font_size)
    textobj = fontobj.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x - textobj.get_width(), (y - textobj.get_height()) // 2)

    # button rect
    button = pygame.Rect(x - textobj.get_width(), (y - textobj.get_height()) // 2,
                         textobj.get_width(), textobj.get_height())
    pygame.draw.rect(surface, WHITE, button)

    surface.blit(textobj, textrect)

    return button


def enter_text(WIN):
    insert_text = True
    surf = pygame.Surface((WIDTH // 3, HEIGHT // 10))
    surf.fill(WHITE)
    text = ""
    while insert_text:
        WIN.blit(surf, ((WIDTH - surf.get_width()) // 2, (HEIGHT - surf.get_height()) // 2))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if 65 <= event.key <= 122:
                    text += chr(event.key)
                    surf.fill(WHITE)
                    draw_text(surf, text, 20, surf.get_width() // 2, surf.get_height() // 2, 0, BLACK, True, True)

                if event.key == pygame.K_RETURN:
                    insert_text = False

                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    surf.fill(WHITE)
                    draw_text(surf, text, 20, surf.get_width() // 2, surf.get_height() // 2, 0, BLACK, True, True)

            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()

    return text


def record_midi_menu(WIN):
    # the velocity with which the notes move up
    note_vel = 2

    # list of currently pressed notes, used for drawing
    notes = []

    # list of currently pressed notes, used for chords
    notes_pressed = []

    # particles list
    particles = []

    pianoKeyboard = PianoKeyboard()
    pianoKeyboard.init()

    # clear input buffer
    midis2events.midis2events(MIDI_INPUT.read(40), MIDI_INPUT).clear()

    # start time of the function
    start = t.perf_counter()

    click = False

    mf = None
    track = None
    channel = None

    running = True
    recording = False
    entering_text = False
    while running:
        # fill background color and draw keyboard over it
        WIN.fill(TAN)
        pianoKeyboard.draw(WIN, notes_pressed)

        # draw notes
        for note in notes:
            if note.is_pressed:
                note.incrementHeight(note_vel)
                note.drawNote(WIN)
                # generate particles
                COLOR = None
                if note.is_white:
                    if note.number < 60:
                        COLOR = COLOR1
                    else:
                        COLOR = COLOR3
                else:
                    if note.number < 60:
                        COLOR = COLOR2
                    else:
                        COLOR = COLOR4

                p = Particle([pianoKeyboard.keys[note.number].x + 6, HEIGHT - WHITE_NOTE_HEIGHT], random.randint(1, 5),
                             [random.randint(0, 20) / 10 - 1, random.randint(0, 20) / 10 - 2], 6, COLOR)
                particles.append(p)
            else:
                note.moveNoteUp(note_vel)
                note.drawNote(WIN)

            if note.rect.y + note.rect.h + 100 < 0:
                notes.remove(note)

        # remove expired particles
        for particle in particles:
            if particle.radius <= 0:
                particles.remove(particle)

        # draw top bar
        pygame.draw.rect(WIN, WHITE, (0, 0, WIDTH, HEIGHT // 17))
        pygame.draw.rect(WIN, BLACK, (0, HEIGHT // 17, WIDTH, 2))

        # draw text on bar
        draw_text(WIN, "Record MIDI", 25, WIDTH // 2, HEIGHT // 17 // 2, BLACK, True, True)
        back_button = draw_button('Main Menu', FONT_NAME, 25, BLACK, WIN, WIDTH - 5, HEIGHT // 17)

        if not recording:
            draw_text(WIN, "Press P to start recording", 20, WIDTH - 5, HEIGHT // 17 * 1.5, BLACK, True, False, True)
        else:
            draw_text(WIN, "Press P to stop recording", 20, WIDTH - 5, HEIGHT // 17 * 1.5, BLACK, True, False, True)

        # draw currently pressed chord name on screen
        if len(notes_pressed) > 0:
            notes_pressed_char = []
            for note in notes_pressed:
                notes_pressed_char.append(number_to_note(note))

            notes_pressed_char.sort()
            if len(notes_pressed_char) == 1:
                draw_text(WIN, notes_pressed_char[0], 25, 5, HEIGHT // 17 // 2, BLACK, True, False)
            elif len(notes_pressed_char) == 2 and abs(notes_pressed[0] - notes_pressed[1]) == 12:
                draw_text(WIN, notes_pressed_char[0] + " with perfect octave", 25, 5, HEIGHT // 17 // 2, BLACK, True,
                          False)
            elif note_to_chord(notes_pressed_char):
                # REGEX
                chords = re.findall(r'<Chord: ([^>]*)', str(note_to_chord(notes_pressed_char)))
                text = ", ".join(chords)
                draw_text(WIN, "Chord: " + text, 25, 5, HEIGHT // 17 // 2, BLACK, True, False)

        # check for midi events from the input port
        for event in midis2events.midis2events(MIDI_INPUT.read(40), MIDI_INPUT):

            # for some reason, all events are NOTE_ON events
            # a NOTE_ON event with velocity 0 represents a NOTE_OFF event
            if event.command == midis2events.NOTE_ON:
                # extract data from event
                note_number = event.data1
                velocity = event.data2

                if velocity != 0:  # note on
                    print(f"ON %s %s %s" % (event.data1, velocity, t.perf_counter() - start))

                    if pianoKeyboard.keys[note_number].is_white:
                        WHITE_NOTE_RECT = pygame.Rect((pianoKeyboard.keys[note_number].x + 6,
                                                       HEIGHT - WHITE_NOTE_HEIGHT), (WIDTH // NR_WHITE_NOTES - 3, 0))
                        note = Note(number=note_number, velocity=velocity, start_time=t.perf_counter() - start,
                                    rect=WHITE_NOTE_RECT, is_pressed=True, is_white=True)
                    else:
                        BLACK_NOTE_RECT = pygame.Rect((pianoKeyboard.keys[note_number].x + 3,
                                                       HEIGHT - WHITE_NOTE_HEIGHT), (WIDTH // 100 - 3, 0))
                        note = Note(number=note_number, velocity=velocity, start_time=t.perf_counter() - start,
                                    rect=BLACK_NOTE_RECT, is_pressed=True, is_white=False)

                    # add note to notes list
                    notes.append(note)

                    # add note number to currently pressed notes list
                    notes_pressed.append(note_number)

                else:  # note off
                    # search for note in notes list and set note.is_pressed to False
                    for note in notes:
                        if note.number == note_number and note.is_pressed:
                            note.is_pressed = False

                            # write note to MIDI file
                            try:
                                if recording:
                                    mf.addNote(track, channel, note_number, note.start_time,
                                               t.perf_counter() - start - note.start_time, note.velocity)
                            except:
                                print("Something went wrong with writing the MIDI file.")

                            # remove note from notes_pressed list
                            notes_pressed.remove(note_number)

                            print("turn off note %s with start time %s" % (note.number, note.start_time))

                    print(f"OFF %s %s %s" % (event.data1, event.data2, t.perf_counter() - start))
            # elif event.command == midis2events.NOTE_OFF:

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_p and recording == False:
                    recording = True
                    # create MIDI object
                    mf = MIDIFile(1)  # only 1 track
                    track = 0  # the only track
                    mf.addTrackName(track, 0, "Sample Track")
                    mf.addTempo(track, 0, 60)
                    channel = 0
                    start = t.perf_counter()

                elif event.key == pygame.K_p and recording == True:
                    recording = False
                    filename = enter_text(WIN)
                    if filename != "":
                        with open(filename + ".mid", 'wb') as outf:
                            mf.writeFile(outf)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if back_button.collidepoint((mx, my)) and click:
            running = False

        pygame.display.update()
        CLOCK.tick(FPS)
