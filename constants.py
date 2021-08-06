import pygame

# screen sizing defaults
DEFAULT_X_SIZE = 700
DEFAULT_Y_SIZE = 700


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

# region colour constants
# block colours
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
# endregion

# region room types
SOLID = "solid"
ROOM = "room"
CURRENT = "current"
TEST = "test"
ENEMY = "enemy"
# endregion

# region enemy types
PIPPER = "pipper"
SLUGGA = "slugga"
LIZASAUR = "lizasaur"
SKRELL = "skrell"
CULTIST = "cultist"
SIREN = "siren"
DEMON = "demon"
# endregion

# region fonts
pygame.font.init()
ROBOTO_30 = pygame.font.SysFont('Roboto', 45)
# endregion

# region weapons

# default dagger
DAGGER_NAME = "Default Dagger"
DAGGER_DESCRIPTION = "A tiny, blunt dagger."

SHORTSWORD_NAME = "Shabby Shortsword"
SHORTSWORD_DESCRIPTION = "A short, moderately pointy sword."

FLAIL_NAME = "Fair Flail"
FLAIL_DESCRIPTION = "An average sized metal ball attached by an average chain to an averagly sturdy wooden handle."

LONGSWORD_NAME = "Legendary Longsword"
LONGSWORD_DESCRIPTION = "A long, razor sharp blade with a sturdy handle."

WAND_NAME = "Magic Wand"
WAND_DESCRIPTION = "It just looks like a stick, surely it could not take down a foe."
# endregion weapons