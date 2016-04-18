
class Event:

    def __init__(self, type, time, id):
        self.type = type
        self.time = time
        self.agent_id = id
        self.parents = []

    def getType(self):
        return self.type

    def getTime(self):
        return self.time

    def getAgentID(self):
        return self.agent_id

    def __iter__(self):
        return