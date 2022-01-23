# A simple game in which you move around rooms and can pick up items that are stored.

class Room:

    def __init__(self,name,north,east,south,west,up,down,contents):
        self.name = name
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.up = up
        self.down = down
        self.contents = contents
        
    def displayRoom(self):
        print("Room name:", self.name)
        if self.north != None:
            print("   Room to the north: ", self.north)
        if self.east != None:
            print("   Room to the east:  ", self.east)
        if self.south != None:
            print("   Room to the south: ", self.south)
        if self.west != None:
            print("   Room to the west:  ", self.west)
        if self.up != None:
            print("   Room above:        ", self.up)
        if self.down != None:
            print("   Room below:        ", self.down)
        if self.contents != None:
            print("   Room contents:     ", self.contents)
        print("")

def createRoom(roomData):
    name,north,east,south,west,up,down,*contents = [i for i in roomData]
    return Room(name,north,east,south,west,up,down,contents)
    
def look():
    print("You are currently in the", current.name + ".")
    print("Contents of the room:")
    contents = current.contents
    if contents == []:
        print("   None")
    else:
        print("   "+"\n   ".join(contents))

def getRoom(name):
    for i in floorPlan:
        if i.name == name:
            return i
    
def move(direction):
    global current
    if direction == "north":
        if current.north != None:
            print("You are now in the", current.north)
            current = getRoom(current.north)
        else:
            print("You can't move in that direction.")
            current = current
    if direction == "east":
        if current.east != None:
            print("You are now in the", current.east)
            current = getRoom(current.east)
        else:
            print("You can't move in that direction.")
            current = current
    if direction == "south":
        if current.south != None:
            print("You are now in the", current.south)
            current = getRoom(current.south)
        else:
            print("You can't move in that direction.")
            current = current
    if direction == "west":
        if current.west != None:
            print("You are now in the", current.west)
            current = getRoom(current.west)
        else:
            print("You can't move in that direction.")
            current = current
    if direction == "up":
        if current.up != None:
            print("You are now in the", current.up)
            current = getRoom(current.up)
        else:
            print("You can't move in that direction.")
            current = current
    if direction == "down":
        if current.down != None:
            print("You are now in the", current.down)
            current = getRoom(current.down)
        else:
            print("You can't move in that direction.")
            current = current

def displayAllRooms():
    for i in floorPlan:
        if i != None:
            i.displayRoom()

def pickup(item):
    global current
    global inventory
    contents = current.contents
    if item in contents:
        inventory.append(item)
        contents.remove(item)
        print("You now have the", item + ".")
    else:
        print("That item is not in this room.")

def drop(item):
    global current
    global inventory
    contents = current.contents
    if item in inventory:
        contents.append(item)
        inventory.remove(item)
        print("You have dropped the", item + ".")
    else:
        print("You don't have that item.")

def listInventory():
    global inventory
    print("   "+"\n   ".join(inventory))
        
def loadMap():

    global floorPlan    # make the variable "floorPlan" a global variable

    f = open("ProjectData.txt")
    
    rooms = []
    for line in f:
        rooms.append(line.strip().split(","))

    roomx = [[],[],[],[],[],[],[]]
    c = 0
    for i in rooms:
        for x in i:
            m = eval(x)
            roomx[c].append(m)
        c += 1
        
    room1,room2,room3,room4,room5,room6,room7 = [i for i in roomx]

    floorPlan = [createRoom(room1),createRoom(room2),createRoom(room3),createRoom(room4),createRoom(room5),createRoom(room6),createRoom(room7)]

def main():

    global current      # make the variable "current" a global variable

    global inventory
    inventory = []
    
    loadMap()
    
    displayAllRooms()
    
    current = floorPlan[0]      # start in the living room
    look()                      # Living Room

    command = input("\nEnter a command: ")
    while command != "exit":
        if command == "help":
            print(" ")
            print("look:        display the name of the current room and its contents")
            print("north:       move north")
            print("east:        move east")
            print("south:       move south")
            print("west:        move west")
            print("up:          move up")
            print("down:        move down")
            print("inventory:   list what items you're currently carrying")
            print("get <item>:  pick up an item currently in the room")
            print("drop <item>: drop an item you're currently carrying")
            print("help:        print this list")
            print("exit:        quit the game")
            command = input("\nEnter a command: ")
        if command == 'north' or command == 'east' or command == 'south' or command == 'west' or command == 'up' or command == 'down':
            move(command)
            command = input("\nEnter a command: ")
        if command == 'look':
            look()
            command = input("\nEnter a command: ")
        if command == 'inventory':
            print("You are currently carrying: ")
            if not inventory:
                print("   nothing.")
            else:
                listInventory()
            command = input("\nEnter a command: ")
        if 'get' in command:
            x = command.split(" ")
            item = x[1]
            pickup(item)
            command = input("\nEnter a command: ")
        if 'drop' in command:
            x = command.split(" ")
            item = x[1]
            drop(item)
            command = input("\nEnter a command: ")

    if command == 'exit':
        print("Quitting game.")
    

main()
