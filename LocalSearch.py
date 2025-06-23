import random
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
from IPython.display import clear_output
import time
import copy

###Local Search###

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

#start with a list of 1 (open) and 0 (nothing) with length as number of candidate locations
#Binary encoding
to_open = []

for candidate in range(n):
    if candidate < openfac:#choose first index(no. locations) as the location to open at
        to_open.append(1)
    else: 
        to_open.append(0)

#choose list of locations based on binary list given 
def choose_locations(to_open, coordlct_x, coordlct_y):
    x_locations = []
    y_locations = []
    
    for open_here in range(len(to_open)):
        if to_open[open_here] == 1:
            x_locations.append(coordlct_x[open_here])
            y_locations.append(coordlct_y[open_here])
            
        if len(x_locations) == openfac:
            break #exit early if all locations to open added
    
    return x_locations, y_locations


#find closest facility for every demand point

import math
#function to plot grap
def plot_demand(coordlct_x, coordlct_y):
    plt.plot(coordlct_x, coordlct_y, 'o', color='black')
    
def plot_facils(tobuild_x, tobuild_y):
    plt.plot(tobuild_x, tobuild_y, 'o', color='red')
    


def closest_facility(to_open, coordlct_x, coordlct_y):
    
    tobuild_x, tobuild_y = choose_locations(to_open, coordlct_x, coordlct_y) #list of each coordinate to build at
    
    #plot 
    #plot_demand(coordlct_x, coordlct_y)
    #plot_facils(tobuild_x, tobuild_y)
    

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

#assign current indexes to flip from
current_1 = 0
current_0 = openfac


while int(curr_time-start) < 60:
    
    
    #Keep looping and flipping 
    
    curr, curr_i_list, curr_tobuild_x, curr_tobuild_y = closest_facility(to_open, coordlct_x, coordlct_y)
    
    if curr < shortest:
        shortest = curr
        closest_i_list, tobuild_x, tobuild_y = curr_i_list, curr_tobuild_x, curr_tobuild_y
        
        #keep and perm next to swap if shorter
        
        #Find next 0
        random.seed()
        
        found = False
        while found == False:
            current_0 += random.randint(1,5)
            if current_0 >= n:
                current_0 = 0
            if to_open[current_0] == 0:
                found = True
            
        #Find next 1
        found = False
        while found == False:
            current_1 += random.randint(1,5)
            if current_1 >= n:
                current_1 = 0
            if to_open[current_1] == 1:
                found = True
        
        #swap both
        to_open[current_1], to_open[current_0] = to_open[current_0], to_open[current_1]
    
    else:
        
        #don't keep and perm next to swap
        
        #swap back
        to_open[current_1], to_open[current_0] = to_open[current_0], to_open[current_1]
        
        #Find next 0
        found = False
        while found == False:
            current_0 += random.randint(1,5)
            if current_0 >= n:
                current_0 = 0
            if to_open[current_0] == 0:
                found = True
            
        #Find next 1
        found = False
        while found == False:
            current_1 += random.randint(1,5)
            if current_1 >= n:
                current_1 = 0
            if to_open[current_1] == 1:
                found = True
        
        #swap both
        to_open[current_1], to_open[current_0] = to_open[current_0], to_open[current_1]
        
        
        
        
    shortest_distance.append(shortest)
    curr_time= time.time()
    time_now=np.append(time_now, curr_time-start)
    

#plot best result
plot_demand(coordlct_x, coordlct_y)
plot_facils(tobuild_x, tobuild_y)
for demand in range(len(coordlct_x)):  
    plt.plot([tobuild_x[closest_i_list[demand]], coordlct_x[demand]], [tobuild_y[closest_i_list[demand]], coordlct_y[demand]], color='black')

###Local Search Results###
plt.plot(time_now[range(len(shortest_distance))],shortest_distance,'k-')
print(shortest_distance[-1])
zipped_coords2 = list(map(lambda x, y: (x, y), tobuild_x, tobuild_y))
print(zipped_coords2)
