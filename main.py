import pygame

pygame.init()

# creates screen
xSize = 500
ySize = 500
screen = pygame.display.set_mode((xSize, ySize))

# setup
pygame.display.set_caption("Test game")

# screen background color
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

# white room
WHITE = (255, 255, 255)
BORDER_COLOR = (200, 95, 95)

# black room
BLACK = (10, 10, 10)

# room types
SOLID = "solid"
ROOM = "room"

xScreenScaling = xSize / 10
yScreenScaling = ySize / 10







class Floor:
    def __init__(self, size):
        self.size = size

    def FloorArray(self):
        floor = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                coords = [c, r]
                row.append(Room(coords))
            floor.append(row)
        return floor


class Room:
    def __init__(self, position):
        self.position = position
        self.roomType = SOLID

    def setRoomType(self, new_type):
        self.roomType = new_type


def DrawSquare(room):
    x = room.position[0] * xScreenScaling
    y = room.position[1] * yScreenScaling
    if room.roomType == SOLID:
        pygame.draw.rect(screen, BLACK, (x, y, 50, 50))
    elif room.roomType == ROOM:
        pygame.draw.rect(screen, WHITE, (x, y, 50, 50))
        pygame.draw.rect(screen, BORDER_COLOR, (x, y, 50, 50), 2)


def DrawRooms(floor_array):
    for i in floor_array:
        for k in i:
            DrawSquare(k)


testFloor = Floor(10)
print(testFloor.FloorArray())
for i in testFloor.FloorArray():
    for k in i:
        if k.position[0] % 2 == 1:
            print(k.position)
            k.roomType = ROOM
DrawRooms(testFloor.FloorArray())


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # updates the screen
    pygame.display.update()





# class Player:
#    def __init__(self, name, max_health):
#        self.name = name
#        self.max_health = max_health
#        self.current_health = max_health

#    def TakeDamage(self, damageTaken):
#        self.current_health -= damageTaken
#        print("{} has taken {} damage.".format(self.name, damageTaken))

#    def ShowHealth(self):
#        print("Health: {}/{}".format(self.current_health, self.max_health))


# player1 = Player("Joe", 100)

# player1.TakeDamage(40)
# player1.ShowHealth()
