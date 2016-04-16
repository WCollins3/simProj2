
class Event:

    def __init__(self, type, time):
        self.type = type
        self.time = time

    def getType(self):
        return self.type

    def getTime(self):
        return self.time
