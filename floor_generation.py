import pygame
import random
import math

from setup import screen, background
import constants

xSize = constants.DEFAULT_X_SIZE
ySize = constants.DEFAULT_Y_SIZE

# max rooms in x and y
TOTAL_FLOOR_LENGTH = 10

xScreenScaling = xSize / TOTAL_FLOOR_LENGTH
yScreenScaling = ySize / TOTAL_FLOOR_LENGTH

# how many tiles will generate (will crash after 30)
USE_RECOMMENDED_ROOM_AMOUNT = True
ROOMS_TO_GENERATE = 15
if USE_RECOMMENDED_ROOM_AMOUNT:
    ROOMS_TO_GENERATE = math.floor((TOTAL_FLOOR_LENGTH ** 2) / 3)

# how many enemy tiles will generate
enemy_room_total = ROOMS_TO_GENERATE // 2.5


def GenerateRooms(floor):
    starter = GenerateStartingRoom(floor)
    lastGenerated = starter
    print("Generating rooms...")
    enemyCounter = 0
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
            if enemyCounter <= enemy_room_total:
                determineIfEnemy = [constants.ROOM, constants.ROOM, constants.ENEMY]
                room.roomType = random.choice(determineIfEnemy)
            lastGenerated = room
            loadPercent = (roomNum / ROOMS_TO_GENERATE)

            room.difficulty = roomNum // 3
            if room.difficulty == 0:
                room.difficulty += 1

            print("Loading: {:.2%}".format(loadPercent))
    print("Loading: 100%")


def PossibleRooms(room, floor):
    # Generates a list of possible rooms to generate next
    movesList = []
    floor_size = floor.size
    tempList = []

    def CheckForExistingRoom(possible_room_coords):
        # Checks that the tile is not already a room
        isRoom = False
        possible_room = floor.GetRoomAt(possible_room_coords)
        if possible_room.roomType != constants.SOLID:
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
                    if room.roomType != constants.SOLID:
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
    starter.roomType = constants.CURRENT
    floor.currentRoom = starter
    return starter


def DrawSquare(room):
    x = room.x * xScreenScaling
    y = room.y * yScreenScaling
    if room.roomType == constants.SOLID:
        pygame.draw.rect(screen, constants.BLACK, (x, y, xScreenScaling, yScreenScaling))

    elif room.roomType == constants.ROOM:
        pygame.draw.rect(screen, constants.BLANK_ROOM, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, constants.BORDER_COLOR, (x, y, xScreenScaling, yScreenScaling), 2)

    elif room.roomType == constants.CURRENT:
        pygame.draw.rect(screen, constants.PLAYER_BLOCK, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, constants.BORDER_COLOR, (x, y, xScreenScaling, yScreenScaling), 2)

    elif room.roomType == constants.TEST:
        pygame.draw.rect(screen, constants.TESTCOL, (x, y, xScreenScaling, yScreenScaling))

    elif room.roomType == constants.ENEMY:
        pygame.draw.rect(screen, constants.ENEMY_BLOCK, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, constants.ENEMY_BORDER, (x, y, xScreenScaling, yScreenScaling), 2)
        diff = str(room.difficulty)
        if diff == 0:
            diff = str(1)
        test = constants.ROBOTO_30.render(diff, False, (0, 0, 0))
        screen.blit(test, (x, y))

    if room.debugger:
        pygame.draw.rect(screen, constants.DEBUG, (x, y, xScreenScaling, yScreenScaling))


def DrawRooms(floor):
    background.fill((0, 0, 0))
    floor_array = floor.floor_array
    for room in floor_array:
        DrawSquare(room)
