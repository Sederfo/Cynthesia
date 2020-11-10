def number_to_note(number):
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number % 12]


class Note:
    def __init__(self, number, velocity, timestamp, x, y, image):
        self.number = number
        self.velocity = velocity
        self.ascii = number_to_note(number)
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.image = image

    def __str__(self):
        return "Note with number %s and velocity %s at time %s" % (self.number, self.velocity, self.timestamp)

    def drawNote(self, WIN):
        WIN.blit(self.image, (self.x, self.y))

    def moveNoteUp(self, vel):
        self.y -= vel

    def moveNoteDown(self, vel):
        self.y += vel
