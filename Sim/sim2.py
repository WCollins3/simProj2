from agent import *
from event import *
from food import *
from map import *
def check_best_spot(locx, locy, fov, m):
    vals = []
    loc = []
    for i in range(1,fov+1):
        if locx+i<5:
            valxup = m[locx+i][locy]
            vals.append(valxup)
            loc.append([locx+i,locy])
        if locx-i>=0:
            valxdown = m[locx-i][locy]
            vals.append(valxdown)
            loc.append([locx-i, locy])
        if locy+i<5:
            valyup = m[locx][locy+i]
            vals.append(valyup)
            loc.append([locx,locy+i])
        if locy-i>=0:
            valydown = m[locx][locy-i]
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





