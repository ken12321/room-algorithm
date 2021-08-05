import constants
import room

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
                floor.append(room.Room(coords))
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