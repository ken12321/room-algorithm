import constants

class Enemy:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.health = difficulty * 5
        self.damage = difficulty * 2
        self.enemyType = self.InitEnemyType()
        self.sprite = self.InitSprite()

    def InitEnemyType(self):
        if self.difficulty <= 1:
            return constants.PIPPER
        elif 2 <= self.difficulty <= 3:
            return constants.SLUGGA
        elif 4 <= self.difficulty <= 5:
            return constants.LIZASAUR
        elif 6 <= self.difficulty <= 7:
            return constants.SKRELL
        elif 8 <= self.difficulty <= 9:
            return constants.CULTIST
        elif 10 <= self.difficulty <= 11:
            return constants.SIREN
        elif self.difficulty < 12:
            return constants.DEMON

    def InitSprite(self):
        if self.enemyType == constants.PIPPER:
            return constants.SPRITE_PIPPER
        elif self.enemyType == constants.SLUGGA:
            return constants.SPRITE_SLUGGA
        elif self.enemyType == constants.LIZASAUR:
            return constants.SPRITE_LIZASAUR
        elif self.enemyType == constants.SKRELL:
            return constants.SPRITE_SKRELL
        elif self.enemyType == constants.CULTIST:
            return constants.SPRITE_CULTIST
        elif self.enemyType == constants.SIREN:
            return constants.SPRITE_SIREN
        elif self.enemyType == constants.DEMON:
            return constants.SPRITE_DEMON