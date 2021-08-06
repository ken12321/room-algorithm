import pygame
import random
import sys

import player
import constants
import enemy
import floor
from setup import screen
from floor_generation import GenerateRooms, DrawRooms, TOTAL_FLOOR_LENGTH

xSize = constants.DEFAULT_X_SIZE
ySize = constants.DEFAULT_Y_SIZE


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

    # testing text, instant win condition for testing
    test_text = constants.ROBOTO_30.render("win", False, (0, 0, 0))
    screen.blit(test_text, (0, ySize - 40))


def InitEnemy(enemy_difficulty):
    current_enemy = enemy.Enemy(enemy_difficulty)
    current_enemy_sprite = current_enemy.sprite
    screen.blit(current_enemy_sprite, (100, 100))
    return current_enemy


# Create the main floor object
mainFloor = floor.Floor(TOTAL_FLOOR_LENGTH)
current_player = player.Player("Ken")


# Initialize the floor and draw the rooms
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
