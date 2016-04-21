import rvgs
from food import *
def littlef(x, y, thetax, thetay):
    val = 4 * rvgs.exponential(-(x/thetax)**2-(y/thetay)**2)
    return val
def bigf(x, bigx, y, bigy):
    val = littlef(x-bigx/4.0, y-bigy/4.0, 0.3*bigx, 0.3*bigy)+littlef(x-3*bigx/4.0, y - 3*bigy/4.0,0.3*bigx,0.3*bigy)
    return val
class Map:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.grid = 50*[50*[0]]
        for i in range(50):
            #array = []
            for j in range(50):
                val = abs(bigf(i+1, 50, j+1, 50))
                #array.append(val)
                self.grid[i][j] = Food(val)


    def getFood(self, x, y):
        return self.grid[x][y]

#m = Map()
