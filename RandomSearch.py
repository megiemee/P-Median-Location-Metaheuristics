import random
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
from IPython.display import clear_output
import time
import copy

###Random Search###

#Generate Data Inputs

# Select random seed
random.seed(1)

# Number of candidate locations
n=1000

#Number of locations to open
openfac=30

#Coordinate Range
rangelct=100000

#Generate random locations
coordlct_x = random.choices(range(0, rangelct), k=n)
coordlct_y = random.choices(range(0, rangelct), k=n)

#store best coords
best_x, best_y = None, None

#choose 15 random locations
def choose_locations(x_coords, y_coords):
    x_locations = []
    y_locations = []
    for i in range(openfac):
        added = False
        added_index = []
        while not added:
            random.seed()
            potential_loc = random.randint(0,len(x_coords) -1)
            if potential_loc not in added_index:
                x_locations.append(x_coords[potential_loc])
                y_locations.append(y_coords[potential_loc])
                added_index.append(potential_loc)
                added = True
    return x_locations, y_locations



#find closest facility for every demand point

import math
#function to plot grap
def plot_demand(coordlct_x, coordlct_y):
    plt.plot(coordlct_x, coordlct_y, 'o', color='black')
    
def plot_facils(tobuild_x, tobuild_y):
    plt.plot(tobuild_x, tobuild_y, 'o', color='red')
    

def closest_facility():
    
    #generate required random locations (openfac: no. locations to open)
    random.seed()
    tobuild_x, tobuild_y = choose_locations(coordlct_x, coordlct_y)

    closest_i_list = [] #index of closest facility for each demand loc
    total_distance = 0 #distance to nearest facil

    for i in range(len(coordlct_x)):

        curr_closest = math.sqrt((tobuild_x[0]-coordlct_x[i])**2 + (tobuild_y[0]-coordlct_y[i])**2)
        curr_closest_i = 0
        for n in range(1, len(tobuild_x)):
            distance = math.sqrt((tobuild_x[n]-coordlct_x[i])**2 + (tobuild_y[n]-coordlct_y[i])**2)
            if distance < curr_closest:
                
                curr_closest_i = n
                curr_closest = distance
                
                

        closest_i_list.append(curr_closest_i)
        total_distance += curr_closest

    return total_distance, closest_i_list, tobuild_x, tobuild_y

import time

shortest = 99999999999999999999999999999
shortest_distance = []
cputime_i = []
start = time.time()#timer
curr_time = time.time()
time_now = [0,0]

while int(curr_time-start) < 60:
    curr, curr_i_list, curr_tobuild_x, curr_tobuild_y = closest_facility()
    if curr < shortest:
        #store info of current best
        shortest = curr
        closest_i_list, tobuild_x, tobuild_y = curr_i_list, curr_tobuild_x, curr_tobuild_y
        
    shortest_distance.append(shortest)
    curr_time= time.time()
    time_now=np.append(time_now, curr_time-start)
    

plot_demand(coordlct_x, coordlct_y)
plot_facils(tobuild_x, tobuild_y)
for demand in range(len(coordlct_x)):  
        plt.plot([tobuild_x[closest_i_list[demand]], coordlct_x[demand]], [tobuild_y[closest_i_list[demand]], coordlct_y[demand]], color='black')

###Random Search Results###
plt.plot(time_now[range(len(shortest_distance))],shortest_distance,'k-')
print(shortest_distance[-1])
zipped_coords = list(map(lambda x, y: (x, y), tobuild_x, tobuild_y))
print(zipped_coords)
print(time_now)
