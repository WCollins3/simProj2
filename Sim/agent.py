import rngs
import rvgs
import random

class Agent:

    currId = 0

    def __init__(self, curr_time, id, x, y):
        self.agentId = id
        self.alive = True
        self.when_born = curr_time
        self.puberty = rvgs.uniform(12,15)
        self.sex = rvgs.bernoulli(0.5)
        self.lifespan = rvgs.uniform(60,100)
        self.fov = rvgs.equilikely(1,6)
        self.met = rvgs.uniform(1,4)
        self.fert = 0
        self.movement = rvgs.equilikely(10, 20)
        self.preg = False
        self.deathTime = 0

        self.lastTime = curr_time
        if self.sex == 1: #male
            self.fert = rvgs.uniform(40,50)
        else:
            self.fert = rvgs.uniform(50,60)
        self.wealth = 100.0
        self.is_fertile = False
        self.x = x
        self.y = y
        self.destX = 0
        self.destY = 0


    def getWealth(self):
        return self.wealth

    def loseWealth(self, curr_time):
        self.wealth -= (self.met*(curr_time - self.lastTime))
        self.lastTime = curr_time
        if curr_time-self.when_born > self.lifespan and self.alive:
            self.alive = False
            self.dies()
            self.deathTime = curr_time
        if self.wealth <= 0 and self.alive:
            self.alive = False
            self.dies()
            self.deathTime = curr_time

    def gainWealth(self, food_gained):
        self.wealth += food_gained
        #self.lastTime = curr_time        Commented out because no food consumption

    def isFert(self):
        return self.is_fertile

    def hitPuberty(self, curr_time):
        self.is_fertile = True
        self.lastTime = curr_time

    def stopFert(self, curr_time):
        self.is_fertile = False
        self.lastTime = curr_time

    def isAlive(self, currTime):
        self.loseWealth(currTime)
        return self.alive


    def getFOV(self):
        return self.fov

    def setDest(self, x, y):
        self.destX = x
        self.destY = y

    def dies(self):
        self.destX = -1
        self.destY = -1




