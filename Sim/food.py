#I really really like cupcakes

class Food:

    def __init__(self, max_capacity):
        self.max_cap = max_capacity
        self.lastAccess = 0
        self.curr_cap = self.max_cap

    def updateAmount(self, curr_time): #call before getAmount
        self.curr_cap += (curr_time-self.lastAccess)
        if self.curr_cap>self.max_cap:
            self.curr_cap = self.max_cap
        #self.lastAccess = curr_time    Commented out because it will cause food to decrease with udated time

    def foodTaken(self, curr_time):
        ret = self.curr_cap
        self.curr_cap = 0
        self.lastAccess = curr_time
        return self.curr_cap

    def getAmount(self):
        return self.curr_cap