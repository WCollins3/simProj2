import rvgs
import food
class Map:

    def __init__(self):
        self.x = 50
        self.y = 50
        self.grid = 50*[50*[0]]
        def littlef(self, x, y):
            return 4*rvgs.exponential(-(x/0.3*self.x)**2-(y/0.3*self.y)**2)
        for i in range(50):
            for j in range(50):
                val = littlef(i-self.x/4, j-self.y/4)+littlef(i-self.x*3/4,y-3*self.y/4)
                self.grid[i][j] = Food(val)




