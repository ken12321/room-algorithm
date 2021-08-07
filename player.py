
import constants
from weapon import Weapon

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.potions_inventory = []
        self.weapons_inventory = []
        self.gold = 0
        self.GiveInitialWeapon()

    def TakeDamage(self, damage):
        self.health -= damage

    def GiveInitialWeapon(self):
        dagger_damage = 2
        dagger = Weapon(constants.DAGGER_NAME, constants.DAGGER_DESCRIPTION, dagger_damage)
        self.AddToWeaponsInventory(dagger)

    def DisplayInventory(self):
        display_weapons_inventory = []
        for weapon in self.weapons_inventory:
            display_weapons_inventory.append(weapon.name)
        return(display_weapons_inventory)

    def AddToWeaponsInventory(self, weapon):
        self.weapons_inventory.append(weapon)

    def RemoveFromWeaponsInventory(self, weapon):
        self.weapons_inventory.remove(weapon)