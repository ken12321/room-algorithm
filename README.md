"# room-algorithm" 

A dungeon crawler-eqsue room generation algorithm. 
Rooms cannot have more than 2 adjacent rooms.
The amount of rooms generated is proportional to half of the area of the screen, unless USE_RECOMMENDED_ROOM_AMOUNT is set to False in the code, otherwise it is directly proportional to ROOMS_TO_GENERATE.
