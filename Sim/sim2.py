from agent import *
from event import *
from food import *
from map import *
import rvgs
import random
import matplotlib.pyplot as plt
def check_best_spot(locx, locy, fov, m, curr_time):
    vals = []
    loc = []
    for i in range(1,fov+1):
        if locx+i<5:
            m[locx+i][locy].updateAmount(curr_time)
            valxup = m[locx+i][locy].curr_cap
            vals.append(valxup)
            loc.append([locx+i,locy])
        if locx-i>=0:
            m[locx-i][locy].updateAmount(curr_time)
            valxdown = m[locx-i][locy].curr_cap
            vals.append(valxdown)
            loc.append([locx-i, locy])
        if locy+i<5:
            m[locx][locy+i].updateAmount(curr_time)
            valyup = m[locx][locy+i].curr_cap
            vals.append(valyup)
            loc.append([locx,locy+i])
        if locy-i>=0:
            m[locx][locy-i].updateAmount(curr_time)
            valydown = m[locx][locy-i].curr_cap
            vals.append(valydown)
            loc.append([locx,locy-i])
    best = 0
    best_index = -1
    for i in range(len(vals)):
        if vals[i]>best:
            best = vals[i]
            best_index = i
    return loc[best_index]

def has_kids(ag, mx):
    if ag.preg or ag.is_fertile==False or ag.wealth<(ag.met*0.75+mx/2.0):
        return False
    return True

def check_left_preg(ag, list, mx, curr_time):
    for agents in list:
        if agents.x+1==ag.x and agents.y == ag.y and curr_time-agents.when_born+0.75<agents.lifespan and \
                                curr_time-ag.when_born+0.75<ag.lifespan:
            if has_kids(agents, mx) and has_kids(ag, mx):
                if agents.sex == 1 and ag.sex == 0:
                    return True, agents
                if agents.sex == 0 and ag.sex == 1:
                    return True, agents
    return False, None

def check_right_preg(ag, list, mx, curr_time):
    for agents in list:
        if agents.x-1==ag.x and agents.y == ag.y and curr_time-agents.when_born+0.75<agents.lifespan and \
                                curr_time-ag.when_born+0.75<ag.lifespan:
            if has_kids(agents, mx) and has_kids(ag, mx):
                if agents.sex == 1 and ag.sex == 0:
                    return True, agents
                if agents.sex == 0 and ag.sex == 1:
                    return True, agents
    return False, None

def check_up_preg(ag, list, mx, curr_time):
    for agents in list:
        if agents.x==ag.x and agents.y-1 == ag.y and curr_time-agents.when_born+0.75<agents.lifespan and \
                                curr_time-ag.when_born+0.75<ag.lifespan:
            if has_kids(agents, mx) and has_kids(ag, mx):
                if agents.sex == 1 and ag.sex == 0:
                    return True, agents
                if agents.sex == 0 and ag.sex == 1:
                    return True, agents
    return False, None

def check_down_preg(ag, list, mx, curr_time):
    for agents in list:
        if agents.x==ag.x and agents.y+1 == ag.y and curr_time-agents.when_born+0.75<agents.lifespan and \
                                curr_time-ag.when_born+0.75<ag.lifespan:
            if has_kids(agents, mx) and has_kids(ag, mx):
                if agents.sex == 1 and ag.sex == 0:
                    return True, agents
                if agents.sex == 0 and ag.sex == 1:
                    return True, agents
    return False, None

def check_down_birth(ag, list):
    for agents in list:
        if agents.x==ag.x and agents.y-1 == ag.y and agents.y-1>=0:
            return False
    return True


def check_up_birth(ag, list):
    for agents in list:
        if agents.x==ag.x and agents.y+1 == ag.y and agents.y+1<50:
            return False
    return True


def check_right_birth(ag, list):
    for agents in list:
        if agents.x+1==ag.x and agents.y == ag.y and agents.x+1<50:
            return False, agents
    return True


def check_left_birth(ag, list):
    for agents in list:
        if agents.x-1==ag.x and agents.y == ag.y and agents.x-1>=0:
            return False
    return True

def create_agents(num, events):
    locs = []
    agents = []
    id = 0
    for n in range(num):
        x = random.randint(0,49)
        y = random.randint(0,49)
        i = 0
        while len(locs)>0 and i < len(locs):
            if locs[i][0]==x and locs[i][1]==y:
                i = 0
                x = random.randint(0,49)
                y = random.randint(0,49)
            i+=1
        ag = Agent(0, id, x, y)
        events.append(Event("Puberty",ag.puberty, ag.agentId))
        events.append(Event("Fertility", ag.fert, ag.agentId))
        events.append(Event("DeathFromAge", ag.lifespan, ag.agentId))
        locs.append([x,y])
        agents.append(ag)
        id+=1

    return agents, events

def calc_move_time(dist):
    total = 0
    for i in range(dist):
        total+=(0.5+rvgs.exponential(0.5))
    return total
def movement(ag, m, curr_time, events):
    ag.x = ag.destX
    ag.y = ag.destY
    loc = check_best_spot(ag.x,ag.y,ag.fov, m, curr_time)
    ag.destX = loc[0]
    ag.destY = loc[1]

    if not ag.x == ag.destX:
        dist = abs(ag.x-ag.destX)
    else:
        dist = abs(ag.y - ag.destY)
    events.append(Event("Movement", curr_time+calc_move_time(dist), ag.agentId))
    return events

def pregnancy(ag, curr_time, events, agents, mx):
    check, other_ag = check_up_preg(ag, agents, mx, curr_time)
    if check:
        events.append(Event("Birth", curr_time+0.75, ag.agentId, [ag, other_ag]))
       # print("Birth")
        ag.preg = True
        other_ag.preg = True
        for i in events:
            if i.agent_id == ag.agentId or i.agent_id == other_ag.preg:
                if i.type == "Movement":
                    i.time += 0.75
        return events
    check, other_ag = check_down_preg(ag, agents, mx, curr_time)
    if check:
        events.append(Event("Birth", curr_time+0.75, ag.agentId, [ag, other_ag]))
        #print("Birth")
        ag.preg = True
        other_ag.preg = True
        for i in events:
            if i.agent_id == ag.agentId or i.agent_id == other_ag.preg:
                if i.type == "Movement":
                    i.time += 0.75
        return events
    check, other_ag = check_left_preg(ag, agents, mx, curr_time)
    if check:
        events.append(Event("Birth", curr_time+0.75, ag.agentId, [ag, other_ag]))
        #print("birth")
        ag.preg = True
        other_ag.preg = True
        for i in events:
            if i.agent_id == ag.agentId or i.agent_id == other_ag.preg:
                if i.type == "Movement":
                    i.time += 0.75
        return events
    check, other_ag = check_right_preg(ag, agents, mx, curr_time)
    if check:
        events.append(Event("Birth", curr_time+0.75, ag.agentId, [ag, other_ag]))
        #print("birth")
        ag.preg = True
        other_ag.preg = True
        for i in events:
            if i.agent_id == ag.agentId or i.agent_id == other_ag.preg:
                if i.type == "Movement":
                    i.time += 0.75
        return events
    return events

def birth():


    return 0

def sim(num_agents, mx_wealth, end_time):
    population = []
    agents, events = create_agents(num_agents, [])
    agents.append(Agent(0,-1,-1,-1))
    sim_map = Map()
    people = []
    for i in range(5,end_time+1, 5):
        events.append(Event("Check", i,-1))
    #for i in range(50):
     #   for j in range(50):
      #      print(sim_map.grid[i][j].getAmount())
    for ag in agents:
        loc = check_best_spot(ag.x,ag.y,ag.fov, sim_map.grid, 0)
        ag.destX = loc[0]
        ag.destY = loc[1]
        if not ag.x == ag.destX:
            dist = abs(ag.x-ag.destX)
        else:
            dist = abs(ag.y - ag.destY)
        #print(calc_move_time(dist))
        events.append(Event("Movement", calc_move_time(dist), ag.agentId))
    curr_time = 0
    events.sort(key=lambda x: x.time, reverse = False)
    while curr_time<=end_time and len(events) != 0: #and len(events)>0:
        ev = events[0]
        #print(ev.type, ev.time)
        ag = agents[ev.agent_id]
        count = 0
        for i in agents:
            if i.alive:
                count+=1
        #print(count, curr_time, ev.type, len(events))
        if not ag.alive:
            events.pop(0)
            continue
        else:
            curr_time = ev.time
            #print(curr_time)
            if ev.type=="Movement":
                curr_time = ev.time
                #print("hurr")
                events.remove(ev)
                ag.loseWealth(curr_time)
                if not ag.alive:
                    continue
                sim_map.grid[ag.destX][ag.destY].updateAmount(curr_time)
                food_gained = sim_map.grid[ag.destX][ag.destY].getAmount()
                ag.gainWealth(food_gained)
                #print(food_gained)
                sim_map.grid[ag.destX][ag.destY].foodTaken(curr_time)
                #print(sim_map.grid[ag.destX][ag.destY].amount)
                events = movement(ag, sim_map.grid, curr_time, events)
                events = pregnancy(ag, curr_time, events, agents, mx_wealth)
                events.sort(key=lambda x: x.time, reverse = False)
            elif ev.type=="Puberty":
                #print("Pub")
                events.remove(ev)
                ag.hitPuberty(curr_time)
            elif ev.type=="Fertility":
                events.remove(ev)
                ag.stopFert(curr_time)
            elif ev.type=="DeathFromAge":
                ag.alive = False
                ag.dies()
                events.remove(ev)
            elif ev.type == "Birth":
                events.remove(ev)
                #print("Birth")
                other_ag = ev.parents[1]
                ag.preg = False
                other_ag.preg = False
                x = ag.x
                y = ag.y
                if check_up_birth(ag, agents):
                    y += 1
                elif check_down_birth(ag, agents):
                    y -= 1
                elif check_right_birth(ag, agents):
                    x += 1
                elif check_left_birth(ag, agents):
                    x -= 1
                else:
                    x = random.randint(0,49)
                    y = random.randint(0,49)
                    i = 0
                    while i < len(agents):
                        if agents[i].x==x and agents[i].y==y:
                            i = 0
                            x = random.randint(0,49)
                            y = random.randint(0,49)
                        i+=1
                new_ag = Agent(curr_time, len(agents), x, y)
                new_ag.other_constructor(ag.puberty, other_ag.puberty, ag.lifespan, other_ag.lifespan,ag.fov, other_ag.fov, ag.met, other_ag.met)
                agents.append(new_ag)
                events.append(Event("Puberty",new_ag.puberty+curr_time, new_ag.agentId))
                events.append(Event("Fertility", new_ag.fert+curr_time, new_ag.agentId))
                events.append(Event("DeathFromAge", new_ag.lifespan+curr_time, new_ag.agentId))
                loc = check_best_spot(new_ag.x,new_ag.y,new_ag.fov, sim_map.grid, 0)
                new_ag.destX = loc[0]
                new_ag.destY = loc[1]
                if not new_ag.x == new_ag.destX:
                    dist = abs(new_ag.x-new_ag.destX)
                else:
                    dist = abs(new_ag.y - new_ag.destY)
                #print(calc_move_time(dist))
                events.append(Event("Movement", curr_time+calc_move_time(dist), new_ag.agentId))
                events.sort(key=lambda x: x.time, reverse = False)
            elif ev.type== "Check":
                events.remove(ev)
                count = 0
                for a in agents:
                    if a.alive:
                        count+=1
                population.append(count)

    agPub = 0
    agFov = 0
    agMet = 0
    agDeath = 0
    agDeathCount = 0
    for a in agents:
        agPub += a.puberty
        agFov += a.fov
        agMet += a.met
        if a.alive == False:
            agDeath += a.deathTime
            agDeathCount += 1
    return population, agPub/len(agents), agFov/len(agents), agMet//len(agents), agDeath/len(agents)


pops = []
xs= []
pubs = []
fovs = []
mets = []
deaths = []
for i in range(100, 1000, 100):
    pop = []
    pub = 0
    fov = 0
    met = 0
    death = 0
    for j in range(1):
        print(j, i)
        s = sim(i, 100, 1000)
        pop += s[0]
        pub += s[1]
        fov += s[2]
        met += s[3]
        death += s[4]
    pops.append(pop)
    xVals = []
    count = 5
    for num in pop:
        xVals.append(count)
        count += 5
    xs.append(xVals)
    plt.scatter(xVals, pop)
    plt.plot(xVals, pop)
    plt.title("Population as time increases")
    plt.ylabel("Population")
    plt.xlabel("Time")
    plt.savefig("Population" + str(i) + ".png")
    plt.clf()

    pubs.append(pub)
    fovs.append(fov)
    mets.append(met)
    deaths.append(death)

for i in range(len(pops)):
    plt.scatter(xs[i], pops[i], label=str((i + 1)*100)+" starting agents")
plt.legend()
plt.savefig("allPops.png")
plt.clf()

xVals = range(100, 1000, 100)
plt.plot(xVals, pubs)
plt.title("Average Puberty age as starting population increases")
plt.ylabel("Puberty age")
plt.xlabel("Starting amount of agents")
plt.savefig("pubs.png")
plt.clf()

plt.plot(xVals, fovs)
plt.title("Average Field of view as starting population increases")
plt.ylabel("Field of view")
plt.xlabel("Starting amount of agents")
plt.savefig("fov.png")
plt.clf()

plt.plot(xVals, mets)
plt.title("Average metabolism as starting population increases")
plt.ylabel("metabolism")
plt.xlabel("Starting amount of agents")
plt.savefig("fov.png")
plt.clf()

plt.plot(xVals, pubs)
plt.title("Average death age as starting population increases")
plt.ylabel("Death age")
plt.xlabel("Starting amount of agents")
plt.savefig("death.png")
plt.clf()


# pop = sim(400, 100.0, 250)
# print(pop[0])
# #xVals = range(5, 250 + 1, 5)
# xVals = []
# count = 5
# for num in pop:
#     xVals.append(count)
#     count += 5
# print(len(pop))
# print(len(xVals))
#
# plt.scatter(xVals, pop)
# plt.plot(xVals, pop)
# plt.title("Population as time increases")
# plt.ylabel("Population")
# plt.xlabel("Time")
# plt.savefig("Population.png")



