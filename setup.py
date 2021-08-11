import pygame
from constants import DEFAULT_X_SIZE, DEFAULT_Y_SIZE

def ScreenSetup(xSize, ySize):
    pygame.init()
    
    # creates screen
    screen = pygame.display.set_mode((xSize, ySize))

    # setup
    pygame.display.set_caption("Test game")
    return screen


def BackgroundSetup(screen):
    # screen background color
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    return background

xSize = DEFAULT_X_SIZE
ySize = DEFAULT_Y_SIZE

screen = ScreenSetup(xSize, ySize)
background = BackgroundSetup(screen)