import pandas as pd
import numpy as np
import time

#global vars--------------------------------------
user_count = 10

small_cell_count = 10
small_cell_capacity = 50

img_count = 100

day_count = 2

small_cell_img_mat = np.zeros((small_cell_count, img_count))
small_cell_occupied = np.zeros(small_cell_count)

small_cell_user_mat = np.random.choice([0, 1], size=(small_cell_count, img_count), p=[1/2, 1/2]) #tbd

img_sizes = np.random.randint(15, size=(img_count,))

small_cell_img_added_times = np.zeros((small_cell_count, img_count)) #for fifo
small_cell_img_last_used_times = np.zeros((small_cell_count, img_count)) # for lru
small_cell_img_frequency = np.zeros((small_cell_count, img_count)) # for lfu

img_request_per_day_count = np.zeros((img_count, day_count))
#request generators----------------------------------

def request_gen():
    request_count = np.random.randint(100, 200)
    request_list = []
    for i in range(request_count):
        user = np.random.randint(user_count)
        small_cell = np.random.randint(small_cell_count)
        img = np.random.randint(img_count)
        request_list.append([user, small_cell, img])
    print(request_list)
    return request_list

#small cells-----------------------------------------

def process_small_cell_from_user(user, small_cell, img): #all 3 are indexes
    if small_cell_img_mat[small_cell][img]:
        small_cell_img_last_used_times[small_cell][img] = time.time()
        return True
    else:
        return False

def process_small_cell_from_backhaul(user, small_cell, img): #all 3 are indexes
    if img_sizes[img] + small_cell_occupied[small_cell] <= small_cell_capacity:
        small_cell_img_mat[small_cell][img] = 1
        small_cell_occupied[small_cell] += img_sizes[img]
        small_cell_img_last_used_times[small_cell][img] = small_cell_img_added_times[small_cell][img] = time.time()
        
    else:
        pass
        #perform replacement strategy
    #send the image to the users

def fifo(small_cell, img): #both are indexes
    while img_sizes[img] + small_cell_occupied[small_cell] > small_cell_capacity:
        removed_img_idx = small_cell_img_added_times[small_cell].index(min(small_cell_img_added_times[small_cell]))
        small_cell_img_mat[small_cell][removed_img_idx] = 0
        small_cell_occupied[small_cell] -= img_sizes[removed_img_idx]
        small_cell_img_last_used_times[small_cell][removed_img_idx] = 0

    small_cell_img_mat[small_cell][img] = 1
    small_cell_occupied[small_cell] += img_sizes[img]
    small_cell_img_last_used_times[small_cell][img] = time.time()

def lifo(small_cell, img): #both are indexes
    while img_sizes[img] + small_cell_occupied[small_cell] > small_cell_capacity:
        removed_img_idx = small_cell_added_times[small_cell].index(max(small_cell_added_times[small_cell]))
        small_cell_img_mat[small_cell][removed_img_idx] = 0
        small_cell_occupied[small_cell] -= img_sizes[removed_img_idx]
        small_cell_img_last_used_times[small_cell][removed_img_idx] = 0

    small_cell_img_mat[small_cell][img] = 1
    small_cell_occupied[small_cell] += img_sizes[img]
    small_cell_img_last_used_times[small_cell][img] = time.time()

def lru(small_cell, img):
    while img_sizes[img] + small_cell_occupied[small_cell] > small_cell_capacity:
        removed_img_idx = small_cell_last_used_times[small_cell].index(min(small_cell_last_used_times[small_cell]))
        small_cell_img_mat[small_cell][removed_img_idx] = 0
        small_cell_occupied[small_cell] -= img_sizes[removed_img_idx]
        small_cell_img_last_used_times[small_cell][removed_img_idx] = 0

    small_cell_img_mat[small_cell][img] = 1
    small_cell_occupied[small_cell] += img_sizes[img]
    small_cell_img_last_used_times[small_cell][img] = time.time()

def lfu(small_cell, img):
    while img_sizes[img] + small_cell_occupied[small_cell] > small_cell_capacity:
        removed_img_idx = small_cell_last_used_times[small_cell].index(min(small_cell_last_used_times[small_cell]))
        small_cell_img_mat[small_cell][removed_img_idx] = 0
        small_cell_occupied[small_cell] -= img_sizes[removed_img_idx]
        small_cell_img_last_used_times[small_cell][removed_img_idx] = 0

    small_cell_img_mat[small_cell][img] = 1
    small_cell_occupied[small_cell] += img_sizes[img]
    small_cell_img_last_used_times[small_cell][img] = time.time()

#backhaul

def cawr():
    pass

#main simulation
cache_hits = 0
cache_misses = 0
request_count = 0

for day in range(day_count):
    requests = request_gen()
    request_count += len(requests)

    for req in requests:
        if process_small_cell_from_user(req[0], req[1], req[2]):
            cache_hits += 1
        else:
            cache_misses += 1
            cawr()
            process_small_cell_from_backhaul(req[0], req[1], req[2])

print("Number of requests: ", request_count)
print("hits: ", cache_hits)
print("misses: ", cache_misses)
