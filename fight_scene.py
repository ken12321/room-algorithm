import pygame
import enemy
import constants
from setup import screen, xSize, ySize
from floor_generation import xScreenScaling, yScreenScaling

def InitFightScreen(enemy_difficulty):
    screen.fill((0, 0, 0))
    textBarSize = yScreenScaling * 3
    curr_enemy = InitEnemy(enemy_difficulty)
    DisplayInventory(textBarSize)
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
    
def DisplayInventory(textBarSize):
    inventory_bar_size = yScreenScaling * 1.25
    inventory_top_pos = ySize - textBarSize - inventory_bar_size - 8
    pygame.draw.rect(screen, constants.INVENTORY_COLOR, (0, inventory_top_pos, xSize, inventory_bar_size))
    pygame.draw.rect(screen, constants.INVENTORY_BORDER_COLOR, (0, inventory_top_pos, xSize, inventory_bar_size), 10)
    screen.blit(constants.SPRITE_DAGGER, (30, inventory_top_pos + 10))