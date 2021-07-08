import pygame
import random
import sys
import math

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
DEBUG = (248, 172, 172)

TESTCOL = (135, 73, 73)

# room types
SOLID = "solid"
ROOM = "room"
CURRENT = "current"
TEST = "test"

# max rooms in x and y
TOTAL_FLOOR_LENGTH = 500

# how many tiles will generate (will crash after 30)
USE_RECOMMENDED_ROOM_AMOUNT = True
ROOMS_TO_GENERATE = 1250
if USE_RECOMMENDED_ROOM_AMOUNT:
    ROOMS_TO_GENERATE = math.floor((TOTAL_FLOOR_LENGTH ** 2) / 2)

xScreenScaling = xSize / TOTAL_FLOOR_LENGTH
yScreenScaling = ySize / TOTAL_FLOOR_LENGTH


def RandomisationDebugger(isInDebug):
    if isInDebug:
        seed = 503555941980892426
        print("Seed was:", seed)
        random.seed(seed)
    else:
        seed = random.randrange(sys.maxsize)
        print("Seed was:", seed)
        random.seed(seed)


RandomisationDebugger(False)  # if false, random seed is used. If true, set seed is used


class Floor:
    def __init__(self, size):
        self.size = size
        self.floor_array = self.InitFloorArray()
        self.nonSolidRooms = []
        self.roomsWithLikelyMoves = set()
        self.currentRoom = None

    def InitFloorArray(self):
        # Initializes the floor's rooms
        floor = []
        for r in range(self.size):
            for c in range(self.size):
                coords = [c, r]
                floor.append(Room(coords))
        return floor

    def InitNonSolidRoomsArray(self):
        # Initializes an array of NON SOLID rooms for easy lookup
        for room in self.floor_array:
            if room.roomType != SOLID:
                self.nonSolidRooms.append(room)

    def GetRoomAt(self, coords):
        for room in self.floor_array:
            if room.position == coords:
                return room


class Room:
    def __init__(self, position):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.roomType = SOLID
        self.debugger = False


def GenerateRooms(floor):
    starter = GenerateStartingRoom(floor)
    lastGenerated = starter

    # Range is directly proportional to the amount of rooms it will generate (EXCLUDING STARTING ROOM)
    for roomNum in range(ROOMS_TO_GENERATE):
        floor.InitNonSolidRoomsArray()
        possibleNextRooms = PossibleRooms(lastGenerated, floor)
        # In the case that there are no valid rooms to generate
        while len(possibleNextRooms) == 0:
            if len(floor.roomsWithLikelyMoves) > 0:
                # Use up the rooms which are more likely to contain possible moves before trying a random one.
                nextAttempt = floor.roomsWithLikelyMoves.pop()
                possibleNextRooms = PossibleRooms(nextAttempt, floor)

            else:
                nextAttempt = random.choice(floor.nonSolidRooms)
                possibleNextRooms = PossibleRooms(nextAttempt, floor)

        else:
            nextRoom = random.choice(possibleNextRooms)
            room = floor.GetRoomAt(nextRoom)
            room.roomType = ROOM
            lastGenerated = room
            loadPercent = (roomNum / ROOMS_TO_GENERATE)
            print("Loading: {:.2%}".format(loadPercent))


def PossibleRooms(room, floor):
    # Generates a list of possible rooms to generate next
    movesList = []
    floor_size = floor.size
    tempList = []

    def CheckForExistingRoom(possible_room_coords):
        # Checks that the tile is not already a room
        isRoom = False
        possible_room = floor.GetRoomAt(possible_room_coords)
        if possible_room.roomType != SOLID:
            isRoom = True
        return isRoom

    def CheckForThreeOrMoreAdjacentRooms(possible_room_coords):
        threeOrMore = False
        counter = 0
        right = [possible_room_coords[0] + 1, possible_room_coords[1]]
        left = [possible_room_coords[0] - 1, possible_room_coords[1]]
        up = [possible_room_coords[0], possible_room_coords[1] - 1]
        down = [possible_room_coords[0], possible_room_coords[1] + 1]

        leftRoom = floor.GetRoomAt(left)
        rightRoom = floor.GetRoomAt(right)
        upRoom = floor.GetRoomAt(up)
        downRoom = floor.GetRoomAt(down)
        possibleRoom = floor.GetRoomAt(possible_room_coords)

        adjacentRooms = [leftRoom, rightRoom, upRoom, downRoom, possibleRoom]

        for room in adjacentRooms:
            if room.x != 0 and room.x != floor_size - 1:
                if room.y != 0 and room.y != floor_size - 1:
                    if room.roomType != SOLID:
                        counter += 1
        if counter >= 2:
            threeOrMore = True
        return threeOrMore

    # checks the tile is in bounds
    if room.x - 1 != 0 and room.x - 1 != floor_size - 1:
        tempList.append([room.x - 1, room.y])
    if room.y - 1 != 0 and room.y - 1 != floor_size - 1:
        tempList.append([room.x, room.y - 1])
    if room.x + 1 != 0 and room.x + 1 != floor_size - 1:
        tempList.append([room.x + 1, room.y])
    if room.y + 1 != 0 and room.y + 1 != floor_size - 1:
        tempList.append([room.x, room.y + 1])

    for possibleRoom in tempList:
        if CheckForExistingRoom(possibleRoom):
            pass
        elif CheckForThreeOrMoreAdjacentRooms(possibleRoom):
            pass
        else:
            movesList.append(possibleRoom)

    if len(movesList) > 2:
        floor.roomsWithLikelyMoves.add(room)  # This set contains moves which likely have an available move

    return movesList


def GenerateStartingRoom(floor):  # Generates the first room
    floor_array = floor.floor_array
    possible_starters = []
    for room in floor_array:
        # Finds all squares one square from the edge.
        if room.x == 1 or room.x == floor.size - 2 or room.y == 1 or room.y == floor.size - 2:
            if room.x == 0 or room.y == floor.size - 1 or room.y == 0 or room.x == floor.size - 1:
                pass
            # Removes corners.
            elif room.x != room.y and not (
                    (room.x == 1 and room.y == floor.size - 2) or (room.y == 1 and room.x == floor.size - 2)):
                possible_starters.append(room)

    starter = random.choice(possible_starters)
    starter.roomType = CURRENT
    floor.currentRoom = starter
    return starter


def DrawSquare(room):
    x = room.x * xScreenScaling
    y = room.y * yScreenScaling
    if room.roomType == SOLID:
        pygame.draw.rect(screen, BLACK, (x, y, xScreenScaling, yScreenScaling))

    elif room.roomType == ROOM:
        pygame.draw.rect(screen, WHITE, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, xScreenScaling, yScreenScaling), 2)

    elif room.roomType == CURRENT:
        pygame.draw.rect(screen, BLUE, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, xScreenScaling, yScreenScaling), 2)

    elif room.roomType == TEST:
        pygame.draw.rect(screen, TESTCOL, (x, y, xScreenScaling, yScreenScaling))

    if room.debugger:
        pygame.draw.rect(screen, DEBUG, (x, y, xScreenScaling, yScreenScaling))


def DrawRooms(floor):
    floor_array = floor.floor_array
    for room in floor_array:
        DrawSquare(room)


def GetClickedRoom(mouse_position, floor):
    mouseX = mouse_position[0]
    mouseY = mouse_position[1]

    for room in floor.floor_array:
        roomX = room.x * xScreenScaling
        roomY = room.y * yScreenScaling
        current_room = floor.currentRoom
        if room != current_room and room.roomType != SOLID:
            if roomY <= mouseY <= roomY + yScreenScaling:  # if the room has the same coords as the mouse click
                if roomX <= mouseX <= roomX + xScreenScaling:
                    right = [room.x + 1, room.y]
                    left = [room.x - 1, room.y]
                    up = [room.x, room.y - 1]
                    down = [room.x, room.y + 1]
                    if floor.GetRoomAt(right) == current_room or floor.GetRoomAt(left) == current_room or floor.GetRoomAt(up) == current_room or floor.GetRoomAt(down) == current_room:
                        current_room.roomType = ROOM
                        floor.currentRoom = room
                        room.roomType = CURRENT


mainFloor = Floor(TOTAL_FLOOR_LENGTH)
GenerateRooms(mainFloor)
DrawRooms(mainFloor)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            GetClickedRoom(mouse_position, mainFloor)
            DrawRooms(mainFloor)
            print("Loading: 100%")
            print(mouse_position)

    # updates the screen
    pygame.display.update()
