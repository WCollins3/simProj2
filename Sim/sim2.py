from agent import *
from event import *
from food import *
from map import *
import rvgs
import random
import math
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

def has_kids(ag, max):
    if ag.preg or ag.is_fertile==False or ag.wealth<(ag.met*0.75+max/2):
        return False
    return True

def check_left_preg(ag, list, max):
    for agents in list:
        if agents.x+1==ag.x and agents.y == ag.y:
            if has_kids(agents, max) and has_kids(ag, max):
                if agents.sex == 1 and ag.sex == 0:
                    return True
                if agents.sex == 0 and ag.sex == 1:
                    return True
    return False

def check_right_preg(ag, list, max):
    for agents in list:
        if agents.x-1==ag.x and agents.y == ag.y:
            if has_kids(agents, max) and has_kids(ag, max):
                if agents.sex == 1 and ag.sex == 0:
                    return True
                if agents.sex == 0 and ag.sex == 1:
                    return True
    return False

def check_up_preg(ag, list, max):
    for agents in list:
        if agents.x==ag.x and agents.y-1 == ag.y:
            if has_kids(agents, max) and has_kids(ag, max):
                if agents.sex == 1 and ag.sex == 0:
                    return True
                if agents.sex == 0 and ag.sex == 1:
                    return True
    return False

def check_down_preg(ag, list, max):
    for agents in list:
        if agents.x==ag.x and agents.y+1 == ag.y:
            if has_kids(agents, max) and has_kids(ag, max):
                if agents.sex == 1 and ag.sex == 0:
                    return True
                if agents.sex == 0 and ag.sex == 1:
                    return True
    return False

def check_down_birth(ag, list):
    for agents in list:
        if agents.x==ag.x and agents.y+1 == ag.y:
            return False
    return True


def check_up_birth(ag, list):
    for agents in list:
        if agents.x==ag.x and agents.y-1 == ag.y:
            return False
    return True


def check_right_birth(ag, list):
    for agents in list:
        if agents.x==ag.x+1 and agents.y == ag.y:
            return False
    return True


def check_left_birth(ag, list):
    for agents in list:
        if agents.x==ag.x and agents.y+1 == ag.y:
            return False
    return True

def create_agents(num, events):
    locs = []
    agents = []
    id = 0
    for n in range(num):
        x = random.randint(0,49)
        y = random.randint(0,49)
        not_found = True
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

def sim(num_agents, max_wealth, end_time):
    agents, events = create_agents(num_agents, [])
    sim_map = Map()
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
    while curr_time<=end_time and len(events)>0:
        ev = events[0]
        #print(ev.type, ev.time)
        ag = agents[ev.agent_id]
        count = 0
        for i in agents:
            if i.alive:
                count+=1
        #print(count, curr_time)
        if not ag.alive:
            events.pop(0)
            continue
        else:
            curr_time = ev.time
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
                movement(ag, sim_map.grid, curr_time, events)
                events.sort(key = lambda x:x.time, reverse = False)
            elif ev.type=="Puberty":
                events.pop(0)
                ag.hitPuberty(curr_time)
            elif ev.type=="Fertility":
                events.pop(0)
            elif ev.type=="DeathFromAge":
                ag.alive = False
                events.pop(0)
    return events

sim(25,100.0,3000.0)




