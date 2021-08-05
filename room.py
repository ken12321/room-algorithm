import constants

class Room:
    def __init__(self, position):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.roomType = constants.SOLID
        self.debugger = False
        self.difficulty = 1

