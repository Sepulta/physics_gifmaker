import random
import operator

def check_if_in_room(room, update_list, bool_val,pos_x,pos_y):
    new_update_list = update_list[:]
    #This can probably be far better written..
    if bool_val:
       try:
           if room.getRoomStatus(pos_x,pos_y) == 1:
               new_update_list.append([[pos_x,pos_y],2])
       except IndexError:
           pass
    return new_update_list

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height, ratio):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.
        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        main_list = []

        #Iterations to create room
        for i in range(self.width):
            sub_list = []
            for j in range(self.height):

                #Taking x as random fraction; 0 < x < 1
                x = random.random()

                #Testing whether it comes out bigger or smaller than given ratio (thus returning true or false)
                #Appending whether true or false: 0 or 1. 
                if x < ratio:
                    sub_list.append(1)
                else:
                    sub_list.append(0)
            #Appending the row in the total grid        
            main_list.append(sub_list)

        #Below is the function to change the uppermost row of tiles to burning tiles
        for i in range(0,width):
            main_list[i][height-1] = 2

        #Filling the room object with the list of values of all the tiles
        self.room = main_list
   
    def cleanTileAtPosition(self, pos, val):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.
        pos: a Position
        """

        #Changing the tile value in the grid. 
        self.room[pos[0]][pos[1]] = val

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.
        returns: an integer
        """
        return self.width * self.height
    
    def getRoomStatus(self, i, j):
        "Asks for value on position in room"
        return self.room[i][j]

    def getTotalRoomStatus(self):
        "Shows total room(matrix), all values"
        return self.room
    
    def getStatusCount(self,room,t=0):
        
        #Flattening the list, making counting less demanding for the program
        count_list = reduce(operator.add,room.getTotalRoomStatus())
        #Counting of tiles with different values
        #Tiles with value 0 are tiles that are empty, thus not able to burn
        a = count_list.count(0)

        #Tiles with value 1 are tiles with trees, thus tiles able to burn
        b = count_list.count(1)

        #Tiles with value 2 are burning tiles
        c = count_list.count(2)

        #Tiles with value 3 are tiles which are burnt
        d = count_list.count(3)

        #returning a list of this, along with the actual timestep
        return [a,b,c,d,t]

