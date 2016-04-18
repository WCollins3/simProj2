from agent import *
from food import *
from event import *
from map import *
import rngs
import rvgs
import matplotlib.pyplot as plt




class Statistcs:
    def __init__(self):
        self.lives = []

def runSim(numAgents):
    map = Map()
    currTime = 0
    events = []
    agents = []
    agentCounter = 0
    for i in range(numAgents):
        #create agent
        x = rvgs.equilikely(0, 49)
        y = rvgs.equilikely(0, 49)
        ag = Agent(currTime, agentCounter, x, y)
        agents.append(ag)
        agentCounter += 1

        #set events

        #start puberty
        pubStart = Event("PubertyStart", ag.puberty, ag.agentId)
        events.append(pubStart)

        #end puberty
        pubEnd = Event("PubertyEnd", ag.fert, ag.agentId)
        events.append(pubEnd)

        #endLife
        endLife = Event("EndLife", ag.lifespan, ag.agentId)
        events.append(endLife)

        #endFood
        endFood = Event("EndFood", ag.wealth / ag.met, ag.agentId)
        events.append(endFood)

        #move to next space
        fov = ag.fov
        #find desired food
        largest = 0
        loc = [0, 0]
        for j in range(1, fov + 1):
            if ag.y + j < 50:
                map.getFood(ag.x, ag.y + j).updateAmount(currTime)
                fd = map.getFood(ag.x, ag.y + j).getAmount()
                if largest < fd:
                    largest = fd
                    loc = [ag.x, ag.y + j]
        for j in range(1, fov + 1):
            if ag.y - j > -1:
                map.getFood(ag.x, ag.y +-j).updateAmount(currTime)
                fd = map.getFood(ag.x, ag.y - j).getAmount()
                if largest < fd:
                    largest = fd
                    loc = [ag.x, ag.y - j]
        for j in range(1, fov + 1):
            if ag.x + j < 50:
                map.getFood(ag.x + j, ag.y).updateAmount(currTime)
                fd = map.getFood(ag.x + j, ag.y).getAmount()
                if largest < fd:
                    largest = fd
                    loc = [ag.x + j, ag.y]
        for j in range(1, fov + 1):
            if ag.x - j > -1:
                map.getFood(ag.x - j, ag.y).updateAmount(currTime)
                fd = map.getFood(ag.x - j, ag.y).getAmount()
                if largest < fd:
                    largest = fd
                    loc = [ag.x - j, ag.y]
        ag.setDest(loc[0], loc[1])

        #Set event for next step taken
        nextStep = Event("TakeStep", ag.movement, ag.agentId)
        events.append(nextStep)

    #sort events
    events.sort(key=lambda x: x.time, reverse = False)

    while len(events) != 0:
        e = events[0]
        currTime = e.getTime()

        #Start Puberty
        if e.getType() == "PubertyStart":
            if agents[e.getAgentID()].isAlive(currTime):
                agents[e.getAgentID()].hitPuberty(currTime)
            #else:
                #print("Agent", e.getAgentID(), "is kill")

        #endPuberty
        elif e.getType() == "PubertyEnd":
            if agents[e.getAgentID()].isAlive(currTime):
                agents[e.getAgentID()].stopFert(currTime)
            #else:
                #print("Agent", e.getAgentID(), "is kill")

        #End lifespan
        elif e.getType() == "EndLife":
            agents[e.getAgentID()].alive = False
            #print("Agent", e.getAgentID(), "is kill")

        #End food
        elif e.getType() == "EndFood":
            if agents[e.getAgentID()].isAlive(currTime):
                agents[e.getAgentID()].loseWealth(currTime)
                if agents[e.getAgentID()].getWealth() <= 0:
                    agents[e.getAgentID()].alive = False
                    #print("Agent", e.getAgentID(), "is kill")
                else:
                    endFood = Event("EndFood", currTime + agents[e.getAgentID()].wealth / agents[e.getAgentID()].met, agents[e.getAgentID()].agentId)
                    events.append(endFood)
            #else:
                #print("Agent", e.getAgentID(), "is kill")

        #Take step
        elif e.getType() == "TakeStep":
            if agents[e.getAgentID()].isAlive(currTime):
                if agents[e.getAgentID()].destX > agents[e.getAgentID()].x:
                    agents[e.getAgentID()].x += 1
                if agents[e.getAgentID()].destX < agents[e.getAgentID()].x:
                    agents[e.getAgentID()].x -= 1
                if agents[e.getAgentID()].destY > agents[e.getAgentID()].y:
                    agents[e.getAgentID()].y += 1
                if agents[e.getAgentID()].destY < agents[e.getAgentID()].y:
                    agents[e.getAgentID()].y -= 1

                #check for baby-making ;)
                if agents[e.getAgentID()].isFert() and agents[e.getAgentID()].preg == False:
                    for i in range(len(agents)):
                        if agents[e.getAgentID()].x == agents[i].x and agents[e.getAgentID()].y == agents[i].y and agents[i].isAlive(currTime) and agents[i].isFert():
                            if agents[i].sex != agents[e.getAgentID()].sex and agents[i].preg == False:
                                gestation = rvgs.uniform(1, 2) #get pregnant
                                if agents[e.getAgentID()].wealth > gestation * agents[e.getAgentID()].met + 25:
                                    if agents[i].wealth > gestation * agents[i].met + 25:
                                        agents[e.getAgentID()].wealth -= 25 / 2
                                        agents[i].wealth -= 25 / 2
                                        agents[e.getAgentID()].preg = True
                                        agents[i].preg = True
                                        if agents[e.getAgentID()].sex == 0:
                                            birth = Event("Birth", currTime + gestation, e.getAgentID())
                                            birth.parents = [e.getAgentID(), i]
                                            events.append(birth)
                                        else:
                                            birth = Event("Birth", currTime + gestation, i)
                                            birth.parents = [e.getAgentID(), i]
                                            events.append(birth)

                #check for destination
                if agents[e.getAgentID()].x == agents[e.getAgentID()].destX and agents[e.getAgentID()].y == agents[e.getAgentID()].destY:
                    map.grid[x][y].updateAmount
                    fd = map.grid[x][y].foodTaken(currTime)
                    agents[e.getAgentID()].gainWealth(currTime, fd)

                    #get next destination
                    largest = 0
                    loc = [0, 0]
                    fov = agents[e.getAgentID()].fov
                    for j in range(1, fov + 1):
                        if agents[e.getAgentID()].y + j < 50:
                            map.getFood(agents[e.getAgentID()].x, agents[e.getAgentID()].y + j).updateAmount(currTime)
                            fd = map.getFood(agents[e.getAgentID()].x, agents[e.getAgentID()].y + j).getAmount()
                            if largest < fd:
                                largest = fd
                                loc = [agents[e.getAgentID()].x, agents[e.getAgentID()].y + j]
                    for j in range(1, fov + 1):
                        if agents[e.getAgentID()].y - j > -1:
                            map.getFood(agents[e.getAgentID()].x, agents[e.getAgentID()].y +-j).updateAmount(currTime)
                            fd = map.getFood(agents[e.getAgentID()].x, agents[e.getAgentID()].y - j).getAmount()
                            if largest < fd:
                                largest = fd
                                loc = [agents[e.getAgentID()].x, agents[e.getAgentID()].y - j]
                    for j in range(1, fov + 1):
                        if agents[e.getAgentID()].x + j < 50:
                            map.getFood(agents[e.getAgentID()].x + j, agents[e.getAgentID()].y).updateAmount(currTime)
                            fd = map.getFood(agents[e.getAgentID()].x + j, agents[e.getAgentID()].y).getAmount()
                            if largest < fd:
                                largest = fd
                                loc = [agents[e.getAgentID()].x + j, agents[e.getAgentID()].y]
                    for j in range(1, fov + 1):
                        if agents[e.getAgentID()].x - j > -1:
                            map.getFood(agents[e.getAgentID()].x - j, agents[e.getAgentID()].y).updateAmount(currTime)
                            fd = map.getFood(agents[e.getAgentID()].x - j, agents[e.getAgentID()].y).getAmount()
                            if largest < fd:
                                largest = fd
                                loc = [agents[e.getAgentID()].x - j, agents[e.getAgentID()].y]
                    agents[e.getAgentID()].setDest(loc[0], loc[1])
            #else:
                #print("Agent", e.getAgentID(), "is kill")
        #Birth
        elif e.getType() == "Birth":
            #print("birth")
            e1 = e.parents[0]
            e2 = e.parents[1]
            agents[e1].preg = False
            agents[e2].preg = False
            x = 0
            y = 0
            if agents[e1].sex == 0:
                x = agents[e1].x
                y = agents[e1].y
            else:
                x = agents[e2].x
                y = agents[e2].y

            ag = Agent(currTime,agentCounter, x, y)
            agentCounter += 1
            agents.append(ag)

            #start puberty
            pubStart = Event("PubertyStart", currTime + ag.puberty, ag.agentId)
            events.append(pubStart)

            #end puberty
            pubEnd = Event("PubertyEnd", currTime + ag.fert, ag.agentId)
            events.append(pubEnd)

            #endLife
            endLife = Event("EndLife", currTime + ag.lifespan, ag.agentId)
            events.append(endLife)

            #endFood
            endFood = Event("EndFood", currTime + ag.wealth / ag.met, ag.agentId)
            events.append(endFood)

            #move to next space
            fov = ag.fov
            #find desired food
            largest = 0
            loc = [0, 0]
            for j in range(1, fov + 1):
                if ag.y + j < 50:
                    map.getFood(ag.x, ag.y + j).updateAmount(currTime)
                    fd = map.getFood(ag.x, ag.y + j).getAmount()
                    if largest < fd:
                        largest = fd
                        loc = [ag.x, ag.y + j]
            for j in range(1, fov + 1):
                if ag.y - j > -1:
                    map.getFood(ag.x, ag.y +-j).updateAmount(currTime)
                    fd = map.getFood(ag.x, ag.y - j).getAmount()
                    if largest < fd:
                        largest = fd
                        loc = [ag.x, ag.y - j]
            for j in range(1, fov + 1):
                if ag.x + j < 50:
                    map.getFood(ag.x + j, ag.y).updateAmount(currTime)
                    fd = map.getFood(ag.x + j, ag.y).getAmount()
                    if largest < fd:
                        largest = fd
                        loc = [ag.x + j, ag.y]
            for j in range(1, fov + 1):
                if ag.x - j > -1:
                    map.getFood(ag.x - j, ag.y).updateAmount(currTime)
                    fd = map.getFood(ag.x - j, ag.y).getAmount()
                    if largest < fd:
                        largest = fd
                        loc = [ag.x - j, ag.y]
            ag.setDest(loc[0], loc[1])

            #Set event for next step taken
            nextStep = Event("TakeStep", currTime + ag.movement, ag.agentId)
            events.append(nextStep)
        else:
            print(e.getType())
        events.remove(e)
    total = 0
    for agent in agents:
        total += agent.deathTime
    total = total / len(agents)

    return total, len(agents), len(agents) - numAgents




answer = runSim(100)
print(answer)

lifespans = []
agents = []
births = []
for i in range(100, 1000, 100):
    numAgents = i
    lifeTotal = 0
    agentTotal = 0
    birthTotal = 0
    print(i)
    for j in range(100):
        answer = runSim(numAgents)
        lifeTotal += answer[0]
        agentTotal += answer[1]
        birthTotal += answer[2]
    lifespans.append(lifeTotal / 100)
    agents.append(agentTotal / 100)
    births.append(birthTotal / 100)

print(lifespans)
print(agents)
print(births)


def plotValues(values, label, title, saveAs):
    plt.scatter(range(100, 1000, 100), values)
    plt.xlabel("Number of agents at beginning of sim")
    plt.ylabel(label)
    plt.title(title)
    plt.savefig(saveAs)
    plt.clf()

plotValues(lifespans, "Average Lifespan", "Average lifespan as starting number of agents increases", "lifeSpan.png")
plotValues(births, "Average amount of births", "Average amount of births as starting number of agents increases", "births.png")

# Current Agent Variable Vals
# puberty = uniform(12, 15)
# sex = bernoulli(0.5)
# lifespan = uniform(60,100)
# fov = equilikely(1,6)
# metabolism = uniform(1,4)
# movement = equilikely(10, 20)
# fert.men = uniform(40,50)
# fert.women = uniform(50,60)
# wealth = 100


