def number_to_note(number):
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number % 12]


class Note:
    def __init__(self, note_number, velocity, timestamp, x, y, note_img):
        self.note_number = note_number
        self.velocity = velocity
        self.note_name = number_to_note(note_number)
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.note_img = note_img

    def __str__(self):
        return "Note with number %s and velocity %s at time %s" % (self.note_number, self.velocity, self.timestamp)

    def drawNote(self, WIN):
        WIN.blit(self.note_img, (self.x, self.y))

    def moveNoteUp(self, vel):
        self.y -= vel

    def moveNoteDown(self, vel):
        self.y += vel
