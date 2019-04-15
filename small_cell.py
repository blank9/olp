import pandas as pd
import numpy as np
import time

small_cell_count = 10
small_cell_capacity = 50
img_count = 100

small_cell_img_mat = np.random.choice([0, 1], size=(small_cell_count, img_count), p=[1/2, 1/2])
small_cell_occupied = []

small_cell_user_mat = np.random.choice([0, 1], size=(small_cell_count, img_count), p=[1/2, 1/2]) #tbd

img_sizes = []
img_last_used_times = []

def process_request_from_user(user, small_cell, img): #all 3 are indexes
    if small_cell_img_mat[small_cell][img]:
        #success code
        pass
    else:
        #send request to backhaul
        pass

def process_request_from_backhaul(user, small_cell, img): #all 3 are indexes
    if img_sizes[img] + small_cell_occupied[small_cell] <= small_cell_capacity:
        small_cell_img_mat[small_cell][img] = 1
        small_cell_occupied[small_cell] += img_sizes[img]
    else:
        while img_sizes[img] + small_cell_occupied[small_cell] > small_cell_capacity:
            #perform LRU
    
    #send the image to the users