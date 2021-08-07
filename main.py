import pygame
import random
import sys

import player
import constants
from floor import Floor
from setup import xSize, ySize
from fight_scene import InitFightScreen
from floor_generation import GenerateRooms, DrawRooms, TOTAL_FLOOR_LENGTH, xScreenScaling, yScreenScaling


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


# Create the main floor object
mainFloor = Floor(TOTAL_FLOOR_LENGTH)
current_player = player.Player("Ken")

print(current_player.name)


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
