import pygame
import random

pygame.init()

# creates screen
xSize = 1000
ySize = 1000
screen = pygame.display.set_mode((xSize, ySize))

# setup
pygame.display.set_caption("Test game")

# screen background color
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

# colors
WHITE = (255, 255, 255)
BORDER_COLOR = (200, 95, 95)
BLUE = (110, 110, 223)
BLACK = (10, 10, 10)

TESTCOL = (135, 73, 73)

# room types
SOLID = "solid"
ROOM = "room"
STARTING = "starting"
TEST = "test"


xScreenScaling = xSize / 10
yScreenScaling = ySize / 10

#random.seed(7)


class Floor:
    def __init__(self, size):
        self.size = size
        self.floor_array = self.InitFloorArray()
        self.nonSolidRooms = []

    def InitFloorArray(self):
        # Initializes the floor's rooms
        floor = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                coords = [c, r]
                row.append(Room(coords))
            floor.append(row)
        return floor

    def InitNonSolidRoomsArray(self):
        # Initializes an array of playable rooms for easy lookup
        for row in self.floor_array:
            for room in row:
                if room.roomType != SOLID:
                    self.nonSolidRooms.append(room)


class Room:
    def __init__(self, position):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.roomType = SOLID


def GenerateRooms(floor):
    starter = GenerateStartingRoom(floor)
    lastGenerated = starter

    # Range is directly proportional to the amount of rooms it will generate (EXCLUDING STARTING ROOM)
    for roomNum in range(10):
        floor.InitNonSolidRoomsArray()
        possibleNextRooms = PossibleRooms(lastGenerated, floor)
        # In the case that there are no valid rooms to generate
        while len(possibleNextRooms) == 0:
            print("No more possible moves, retrying from list")
            nextAttempt = random.choice(floor.nonSolidRooms)
            possibleNextRooms = PossibleRooms(nextAttempt, floor)
        else:
            nextRoom = random.choice(possibleNextRooms)
            for row in floor.floor_array:
                for room in row:
                    if room.position == nextRoom:
                        room.roomType = ROOM
                        lastGenerated = room


def PossibleRooms(room, floor):
    movesList = []
    floor_size = floor.size
    tempList = []

    def CheckForExistingRoom(possibleRoomCoords):
        # Checks that the tile is not already a room
        isRoom = False
        for row in floor.floor_array:
            for room in row:
                if room.position == possibleRoomCoords:
                    if room.roomType != SOLID:
                        isRoom = True
        return isRoom

    # checks the tile is in bounds
    if room.x - 1 != 0 and room.x - 1 != floor_size - 1:
        tempList.append([room.x - 1, room.y])
    if room.y - 1 != 0 and room.y - 1 != floor_size - 1:
        tempList.append([room.x, room.y - 1])
    if room.x + 1 != 0 and room.x + 1 != floor_size - 1:
        tempList.append([room.x + 1, room.y])
    if room.y + 1 != 0 and room.y + 1 != floor_size - 1:
        tempList.append([room.x, room.y + 1])

    for possibleMove in tempList:
        if CheckForExistingRoom(possibleMove):
            pass
        else:
            movesList.append(possibleMove)

    return movesList


def GenerateStartingRoom(floor):  # Generates the first room
    floor_array = floor.floor_array
    possible_starters = []
    for row in floor_array:
        for room in row:
            # Finds all squares one square from the edge.
            if room.x == 1 or room.x == floor.size - 2 or room.y == 1 or room.y == floor.size - 2:
                if room.x == 0 or room.y == floor.size - 1 or room.y == 0 or room.x == floor.size - 1:
                    pass
                # Removes corners.
                elif room.x != room.y and not ((room.x == 1 and room.y == floor.size - 2) or (room.y == 1 and room.x == floor.size - 2)):
                    possible_starters.append(room)

    starter = random.choice(possible_starters)
    starter.roomType = STARTING
    return starter


def DrawSquare(room):
    x = room.x * xScreenScaling
    y = room.y * yScreenScaling
    if room.roomType == SOLID:
        pygame.draw.rect(screen, BLACK, (x, y, xScreenScaling, yScreenScaling))

    elif room.roomType == ROOM:
        pygame.draw.rect(screen, WHITE, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, xScreenScaling, yScreenScaling), 2)

    elif room.roomType == STARTING:
        pygame.draw.rect(screen, BLUE, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, xScreenScaling, yScreenScaling), 2)

    elif room.roomType == TEST:
        pygame.draw.rect(screen, TESTCOL, (x, y, xScreenScaling, yScreenScaling))


def DrawRooms(floor):
    floor_array = floor.floor_array
    for row in floor_array:
        for room in row:
            DrawSquare(room)


testFloor = Floor(10)
GenerateRooms(testFloor)
DrawRooms(testFloor)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # updates the screen
    pygame.display.update()
