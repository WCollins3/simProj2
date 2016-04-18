import agent
import event
import food
import map
def check_best_spot(locx, locy, fov, map):
    vals = []
    loc = []
    for i in range(1,fov+1):
        if locx+i<5:
            valxup = map[locx+i][locy]
            vals.append(valxup)
            loc.append([locx+i,locy])
        if locx-i>=0:
            valxdown = map[locx-i][locy]
            vals.append(valxdown)
            loc.append([locx-i, locy])
        if locy+i<5:
            valyup = map[locx][locy+i]
            vals.append(valyup)
            loc.append([locx,locy+i])
        if locy-i>=0:
            valydown = map[locx][locy-i]
            vals.append(valydown)
            loc.append([locx,locy-i])
    best = 0
    best_index = -1
    for i in range(len(vals)):
        if vals[i]>best:
            best = vals[i]
            best_index = i
    return loc[best_index]

def has_kids(agent, max):
    if agent.preg or agent.is_fertile==False or agent.wealth<(agent.met*75+max/2):
        return False
    return True









