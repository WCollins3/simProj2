
class Food:

    def __init__(self):
        self.amount = 0
        self.lastAccess = 0

    def access(self, time):
        self.lastAccess = time

    def getAmount(self):

        #Enter alg from sheet

        ret = self.amount
        self.amount = 0
        return ret
