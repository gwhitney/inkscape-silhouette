# (c) 2017 Johann Gail
#
# StrategyMinTraveling.py -- cut strategy algorithms for a Graphtec Silhouette Cameo plotter

import math

# Strategy is:
# At each end of a cut search the nearest starting point for the next cut.
# This will probably not find find the global optimum, but works well enough.


# Calculates the distance between two given points.
# The result does not calculate the root for performance reasons,
# because it is only compared to others, the actual value does not matter.
def dist_sq(a,b):
  dx = a[0]-b[0]
  dy = a[1]-b[1]
  return dx*dx+dy*dy

# Define the distance from a position to a path to be minimized greedily
def dist_to_path(p,pth):
  return 2*math.sqrt(dist_sq(p,pth[0])) + math.sqrt(dist_sq(p,pth[-1]))

# Finds the nearest path in a list from a given position
def findnearestpath(paths, pos, entrycircular, reversible):
    nearestindex=0
    nearestdist=float("inf")
    for index,path in enumerate(paths):
        distance = dist_to_path(pos,path) # original direction
        if (nearestdist > distance):
            nearestdist = distance
            nearestindex = index
            selected = path
        if reversible:
            reversed = path[::-1]
            distance = dist_to_path(pos,reversed) # reverse direction
            if (nearestdist > distance):
                nearestdist = distance
                nearestindex = index
                selected = reversed
        if (entrycircular & (path[0] == path[-1])):  # break up circular path. Not sure, if this saves real much time
           for i,p in enumerate(path):   # test each point in closed path
                 distance = dist_to_path(pos,[p])
                 if (nearestdist > distance):
                     nearestdist = distance
                     nearestindex = index
                     selected = path[i:] + path[1:i+1]
    return nearestindex,selected


# Sort paths to approximate minimal traveling times
# (greedy algorithm not necessarily optimal)
def sort(paths, entrycircular=False, reversible=True):
    pos=(0,0)
    sortedpaths=[]
    while (len(paths) > 0):
        i,path = findnearestpath(paths,pos,entrycircular,reversible)
        paths.pop(i)             # delete found index
        pos = path[-1]           # endpoint is next start point for search
        sortedpaths.append(path) # append to output list
    return sortedpaths
