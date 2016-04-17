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
        self.lastTime = curr_time
        if self.sex == 1:
            self.fert = rvgs.uniform(40,50)
        else:
            self.fert = rvgs.uniform(50,60)
        self.wealth = 25.0
        self.is_fertile = False
        self.x = x
        self.y = y


    def getWealth(self):
        return self.wealth

    def loseWealth(self, curr_time):
        self.wealth -= (self.met*(curr_time-self.lastTime))
        self.lastTime = curr_time
        if curr_time-self.when_born > self.lifespan:
            self.alive = False
        if self.wealth <= 0:
            self.alive = False

    def gainWealth(self, curr_time, food_gained):
        self.wealth += food_gained
        self.lastTime = curr_time

    def isFert(self):
        return self.is_fertile

    def hitPuberty(self, curr_time):
        self.is_fertile = True
        self.lastTime = curr_time

    def stopFert(self, curr_time):
        self.is_fertile = False
        self.lastTime = curr_time

    def isAlive(self):
        return self.alive

    def getFOV(self):
        return self.fov



