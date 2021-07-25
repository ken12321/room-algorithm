import pygame
import random
import sys
import math

pygame.init()
pygame.font.init()
ROBOTO_30 = pygame.font.SysFont('Roboto', 45)

# region Sprites
# region ENEMY SPRITES
SPRITE_PIPPER = pygame.image.load('./images/enemies/pipper.png')
SPRITE_PIPPER = pygame.transform.scale(SPRITE_PIPPER, (150, 150))

SPRITE_SLUGGA = pygame.image.load('./images/enemies/slugga.png')
SPRITE_SLUGGA = pygame.transform.scale(SPRITE_SLUGGA, (150, 150))

SPRITE_LIZASAUR = pygame.image.load('./images/enemies/lizasaur.png')
SPRITE_LIZASAUR = pygame.transform.scale(SPRITE_LIZASAUR, (150, 150))

SPRITE_SKRELL = pygame.image.load('./images/enemies/skrell.png')
SPRITE_SKRELL = pygame.transform.scale(SPRITE_SKRELL, (150, 150))

SPRITE_CULTIST = pygame.image.load('./images/enemies/cultist.png')
SPRITE_CULTIST = pygame.transform.scale(SPRITE_CULTIST, (150, 150))

SPRITE_SIREN = pygame.image.load('./images/enemies/siren.png')
SPRITE_SIREN = pygame.transform.scale(SPRITE_SIREN, (150, 150))

SPRITE_DEMON = pygame.image.load('./images/enemies/demon.png')
SPRITE_DEMON = pygame.transform.scale(SPRITE_DEMON, (150, 150))
# endregion

SPRITE_ARROW = pygame.image.load('./images/misc/arrow.png')
SPRITE_ARROW = pygame.transform.scale(SPRITE_ARROW, (75, 75))
# endregion

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
PLAYER_BLOCK = (0, 218, 157)
BORDER_COLOR = (25, 94, 75)
BLANK_ROOM = (202, 235, 226)

ENEMY_BLOCK = (255, 160, 132)
ENEMY_BORDER = (243, 53, 1)

BLUE = (110, 110, 223)
BLACK = (10, 10, 10)
DEBUG = (248, 172, 172)

TESTCOL = (135, 73, 73)

# fight screen colors
MAIN_TEXT_SCREEN = (222, 229, 229)
MAIN_TEXT_BORDER = (157, 197, 187)

# 23, 184, 144
# 94, 128, 127
# 8, 45, 15

# room types
SOLID = "solid"
ROOM = "room"
CURRENT = "current"
TEST = "test"
ENEMY = "enemy"

# enemy types
PIPPER = "pipper"
SLUGGA = "slugga"
LIZASAUR = "lizasaur"
SKRELL = "skrell"
CULTIST = "cultist"
SIREN = "siren"
DEMON = "demon"


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


class Enemy:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.health = difficulty * 5
        self.damage = difficulty * 2
        self.enemyType = self.InitEnemyType()
        self.sprite = self.InitSprite()

    def InitEnemyType(self):
        if self.difficulty <= 1:
            return PIPPER
        elif 2 <= self.difficulty <= 3:
            return SLUGGA
        elif 4 <= self.difficulty <= 5:
            return LIZASAUR
        elif 6 <= self.difficulty <= 7:
            return SKRELL
        elif 8 <= self.difficulty <= 9:
            return CULTIST
        elif 10 <= self.difficulty <= 11:
            return SIREN
        elif self.difficulty < 12:
            return DEMON

    def InitSprite(self):
        if self.enemyType == PIPPER:
            return SPRITE_PIPPER
        elif self.enemyType == SLUGGA:
            return SPRITE_SLUGGA
        elif self.enemyType == LIZASAUR:
            return SPRITE_LIZASAUR
        elif self.enemyType == SKRELL:
            return SPRITE_SKRELL
        elif self.enemyType == CULTIST:
            return SPRITE_CULTIST
        elif self.enemyType == SIREN:
            return SPRITE_SIREN
        elif self.enemyType == DEMON:
            return SPRITE_DEMON


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
                determineIfEnemy = [ROOM, ROOM, ENEMY]
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
        pygame.draw.rect(screen, BLANK_ROOM, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, xScreenScaling, yScreenScaling), 2)

    elif room.roomType == CURRENT:
        pygame.draw.rect(screen, PLAYER_BLOCK, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, xScreenScaling, yScreenScaling), 2)

    elif room.roomType == TEST:
        pygame.draw.rect(screen, TESTCOL, (x, y, xScreenScaling, yScreenScaling))

    elif room.roomType == ENEMY:
        pygame.draw.rect(screen, ENEMY_BLOCK, (x, y, xScreenScaling, yScreenScaling))
        pygame.draw.rect(screen, ENEMY_BORDER, (x, y, xScreenScaling, yScreenScaling), 2)
        diff = str(room.difficulty)
        if diff == 0:
            diff = str(1)
        test = ROBOTO_30.render(diff, False, (0, 0, 0))
        screen.blit(test, (x, y))

    if room.debugger:
        pygame.draw.rect(screen, DEBUG, (x, y, xScreenScaling, yScreenScaling))


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
        if room != current_room and room.roomType != SOLID:
            if roomY <= mouseY <= roomY + yScreenScaling:  # if the room has the same coords as the mouse click
                if roomX <= mouseX <= roomX + xScreenScaling:
                    right = [room.x + 1, room.y]
                    left = [room.x - 1, room.y]
                    up = [room.x, room.y - 1]
                    down = [room.x, room.y + 1]
                    if floor.GetRoomAt(right) == current_room or floor.GetRoomAt(left) == current_room or floor.GetRoomAt(up) == current_room or floor.GetRoomAt(down) == current_room:
                        if room.roomType == ENEMY:
                            return room
                        current_room.roomType = ROOM
                        floor.currentRoom = room
                        return room


def InitFightScreen(enemy_difficulty):
    screen.fill((0, 0, 0))
    textBarSize = yScreenScaling * 3
    curr_enemy = InitEnemy(enemy_difficulty)
    pygame.draw.rect(screen, MAIN_TEXT_SCREEN, (0, ySize - textBarSize, xSize, textBarSize))
    pygame.draw.rect(screen, MAIN_TEXT_BORDER, (0, ySize - textBarSize, xSize, textBarSize), 10)
    enemy_encounter_string = "Enemy encounter! A {} approaches!".format(curr_enemy.enemyType)
    initial_enemy_encounter_text = ROBOTO_30.render(enemy_encounter_string, False, (0, 0, 0))
    screen.blit(initial_enemy_encounter_text, (round(xScreenScaling / 3), ySize - textBarSize + 25))
    screen.blit(SPRITE_ARROW, (xSize - 95, ySize - 95))

    # testing text
    test_text = ROBOTO_30.render("win", False, (0, 0, 0))
    screen.blit(test_text, (0, ySize - 40))



def InitEnemy(enemy_difficulty):
    current_enemy = Enemy(enemy_difficulty)
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
                    if room_clicked.roomType == ROOM:
                        room_clicked.roomType = CURRENT
                        DrawRooms(mainFloor)
                    elif room_clicked.roomType == ENEMY:
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
                    mainFloor.currentRoom.roomType = ROOM
                    room_clicked.roomType = CURRENT
                    mainFloor.currentRoom = room_clicked
                    in_fight = False
                    DrawRooms(mainFloor)


    # updates the screen
    pygame.display.update()
