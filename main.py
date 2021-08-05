import pygame
import random
import sys
import math

import setup
import constants
import enemy

xSize = 500
ySize = 500

screen = setup.ScreenSetup(xSize, ySize)
background = setup.BackgroundSetup(screen)

# max rooms in x and y
TOTAL_FLOOR_LENGTH = 10

# how many tiles will generate (will crash after 30)
USE_RECOMMENDED_ROOM_AMOUNT = True
ROOMS_TO_GENERATE = 15
if USE_RECOMMENDED_ROOM_AMOUNT:
    ROOMS_TO_GENERATE = math.floor((TOTAL_FLOOR_LENGTH ** 2) / 3)

# how many enemy tiles will generate
ENEMY_ROOM_TOTAL = ROOMS_TO_GENERATE // 2.5

xScreenScaling = xSize / TOTAL_FLOOR_LENGTH
yScreenScaling = ySize / TOTAL_FLOOR_LENGTH


def UseRandomSeed(is_random):
    if is_random:
        seed = random.randrange(sys.maxsize)
        print("Seed was:", seed)
        random.seed(seed)
    else:
        seed = 503555941980892426
        print("Seed was:", seed)
        random.seed(seed)


UseRandomSeed(True)  # if true, random seed is used. If false, set seed is used


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
            if room.roomType != constants.SOLID:
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
        self.roomType = constants.SOLID
        self.debugger = False
        self.difficulty = 1


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
            if enemyCounter <= ENEMY_ROOM_TOTAL:
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


def GetClickedRoom(mouse_position, floor):
    mouseX = mouse_position[0]
    mouseY = mouse_position[1]

    for room in floor.floor_array:
        roomX = room.x * xScreenScaling
        roomY = room.y * yScreenScaling
        current_room = floor.currentRoom
        if room != current_room and room.roomType != constants.SOLID:
            if roomY <= mouseY <= roomY + yScreenScaling:  # if the room has the same coords as the mouse click
                if roomX <= mouseX <= roomX + xScreenScaling:
                    right = [room.x + 1, room.y]
                    left = [room.x - 1, room.y]
                    up = [room.x, room.y - 1]
                    down = [room.x, room.y + 1]
                    if floor.GetRoomAt(right) == current_room or floor.GetRoomAt(left) == current_room or floor.GetRoomAt(up) == current_room or floor.GetRoomAt(down) == current_room:
                        if room.roomType == constants.ENEMY:
                            return room
                        current_room.roomType = constants.ROOM
                        floor.currentRoom = room
                        return room


def InitFightScreen(enemy_difficulty):
    screen.fill((0, 0, 0))
    textBarSize = yScreenScaling * 3
    curr_enemy = InitEnemy(enemy_difficulty)
    pygame.draw.rect(screen, constants.MAIN_TEXT_SCREEN, (0, ySize - textBarSize, xSize, textBarSize))
    pygame.draw.rect(screen, constants.MAIN_TEXT_BORDER, (0, ySize - textBarSize, xSize, textBarSize), 10)
    enemy_encounter_string = "Enemy encounter! A {} approaches!".format(curr_enemy.enemyType)
    initial_enemy_encounter_text = constants.ROBOTO_30.render(enemy_encounter_string, False, (0, 0, 0))
    screen.blit(initial_enemy_encounter_text, (round(xScreenScaling / 3), ySize - textBarSize + 25))
    screen.blit(constants.SPRITE_ARROW, (xSize - 95, ySize - 95))

    # testing text
    test_text = constants.ROBOTO_30.render("win", False, (0, 0, 0))
    screen.blit(test_text, (0, ySize - 40))


def InitEnemy(enemy_difficulty):
    current_enemy = enemy.Enemy(enemy_difficulty)
    current_enemy_sprite = current_enemy.sprite
    screen.blit(current_enemy_sprite, (100, 100))
    return current_enemy


mainFloor = Floor(TOTAL_FLOOR_LENGTH)
GenerateRooms(mainFloor)
DrawRooms(mainFloor)

in_fight = False
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()

            if not in_fight:
                room_clicked = GetClickedRoom(mouse_position, mainFloor) # if room is invalid, will return None
                if room_clicked is not None:
                    if room_clicked.roomType == constants.ROOM:
                        room_clicked.roomType = constants.CURRENT
                        DrawRooms(mainFloor)
                    elif room_clicked.roomType == constants.ENEMY:
                        fight_difficulty = mainFloor.currentRoom.difficulty
                        in_fight = True
                        InitFightScreen(fight_difficulty)

            if in_fight:
                # Flee button
                if (xSize - 95 < mouse_position[0] < xSize - 10) and (ySize < mouse_position[1] < ySize - 95):
                    DrawRooms(mainFloor)
                    in_fight = False
                # Insta win button
                if (0 < mouse_position[0] < 50) and (ySize > mouse_position[1] > ySize - 40):
                    mainFloor.currentRoom.roomType = constants.ROOM
                    room_clicked.roomType = constants.CURRENT
                    mainFloor.currentRoom = room_clicked
                    in_fight = False
                    DrawRooms(mainFloor)


    # updates the screen
    pygame.display.update()
