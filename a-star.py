import math 
from queue import PriorityQueue
import time

obstacle_points = []

# size of the map
X_SIZE = 600
Y_SIZE = 250

# create map with obstacle
def create_obstacle_map():
    # Wall clearance
    for xp in range(0,601):
        for yp in range(0,6):
            obstacle_points.append((xp,yp))
        for yp in range(245,251):
            obstacle_points.append((xp,yp))
    
    for yp in range(0,251):
        for xp in range(0,6):
            obstacle_points.append((xp,yp))
        for xp in range(595,601):
            obstacle_points.append((xp,yp))

    # Rectangle and clearance
    for xp in range(100,151):
        for yp in range(101,106):
            obstacle_points.append((xp,yp))
        for yp in range(145, 151):
            obstacle_points.append((xp,yp))
        for yp in range(0,101):
            obstacle_points.append((xp,yp))
    
    for xp in range(151,156):
        for yp in range(0,106):
            obstacle_points.append((xp,yp))
        for yp in range(145,250):
            obstacle_points.append((xp,yp))
    
    for xp in range(100,151):
        for yp in range(150,251):
            obstacle_points.append((xp,yp))
        for yp in range(101,105):
            obstacle_points.append((xp,yp))
            
    for xp in range(95,100):
        for yp in range(150,251):
            obstacle_points.append((xp,yp))
        for yp in range(100,105):
            obstacle_points.append((xp,yp))  
        for yp in range(0,101):
            obstacle_points.append((xp,yp))     
        for yp in range(145,151):
            obstacle_points.append((xp,yp)) 

    # triangle 
    for xp in range(450, 601):
        for yp in range(0,251):
            if (2*xp - yp <= 895) and (2*xp+yp <= 1145):
                obstacle_points.append((xp,yp))

            if (2*xp+yp <= 1156.18) and (2*xp - yp <= 906.18):
                obstacle_points.append((xp,yp))

    # Hexagon
    for xp in range(220,380):
        for yp in range(40,230):
            if  (yp - (0.577)*xp - (32.692)) < 0 and (yp + (0.577)*xp - (378.846)) < 0 and (yp - (0.577)*xp + (128.846)) > 0 and (yp + (0.577)*xp - (217.307)) > 0 and (230 <= xp <= 370):
                obstacle_points.append((xp,yp))

# get input and check if valid or not
def get_input():
    accept_start_node, accept_goal_node = True, True
    while accept_start_node:
        start_x = int(input("Enter start x: "))
        start_y = int(input("Enter start y: "))
        start_node = (start_x, start_y)
        if start_node not in obstacle_points:
            accept_start_node = False
            start_theta = int(input("Enter start theta: "))
            start_node = (start_x, start_y, start_theta)
        else:
            print("Entered start node is in obstacle. Please enter a valid note...")

    while accept_goal_node:    
        goal_x = int(input("Enter goal x: "))
        goal_y = int(input("Enter goal y: "))        
        goal_node = (goal_x, goal_y)
        if goal_node not in obstacle_points:
            accept_goal_node = False
            goal_theta = int(input("Enter goal theta: "))
            goal_node = (goal_x, goal_y, goal_theta)
        else:
            print("Entered goal node is in obstacle. Please enter a valid note...")
    return start_node, goal_node

def eclidean_distance(pt1, pt2):
    distance = math.sqrt(pow((pt1[0] - pt2[0]), 2) + pow((pt1[1] - pt2[1]),2))
    return round(distance, 2)

def move_up_right(curr_node):
    current_point = curr_node[2]
    next_point = (current_point[0] + 1, current_point[1] + 1)     

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = 1.4
        updated_cost = curr_node[1] + cost         
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][2] == next_point:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

def move_up_left(curr_node):
    current_point = curr_node[2]
    next_point = (current_point[0] - 1, current_point[1] + 1)     

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = 1.4
        updated_cost = curr_node[1] + cost         
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][2] == next_point:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

def move_down_right(curr_node):
    current_point = curr_node[2]
    next_point = (current_point[0] + 1, current_point[1] - 1)     

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = 1.4
        updated_cost = curr_node[1] + cost         
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][2] == next_point:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

def move_down_left(curr_node):
    current_point = curr_node[2]
    next_point = (current_point[0] - 1, current_point[1] - 1)     

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = 1.4
        updated_cost = curr_node[1] + cost         
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][2] == next_point:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

def move_up(curr_node):
    current_point = curr_node[2]
    next_point = (current_point[0], current_point[1] + 1)     

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = 1
        updated_cost = curr_node[1] + cost         
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][2] == next_point:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

def move_down(curr_node):
    current_point = curr_node[2]
    next_point = (current_point[0], current_point[1] - 1)     

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = 1
        updated_cost = curr_node[1] + cost         
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][2] == next_point:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

def move_left(curr_node):
    current_point = curr_node[2]
    next_point = (current_point[0] - 1, current_point[1])     

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = 1
        updated_cost = curr_node[1] + cost         
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][2] == next_point:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

def move_right(curr_node):
    current_point = curr_node[2]
    next_point = (current_point[0] + 1, current_point[1])     

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = 1
        updated_cost = curr_node[1] + int(cost)        
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][2] == next_point:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

create_obstacle_map()
start_node, goal_node = get_input()
# print(eclidean_distance((0, 0), (1, 1)))
start = time.time()
map_queue = PriorityQueue()
start_pt = (start_node[0], start_node[1])
goal_pt = (goal_node[0], goal_node[1])
map_queue.put((eclidean_distance(start_pt, goal_pt), 0, start_pt))
# print(map_queue.queue)

visited_nodes = []
parent_child_info = {}

while True:
    current_node = map_queue.get()
    print(current_node)
    visited_nodes.append(current_node[2])
    x, y = current_node[2][0], current_node[2][1]
    if current_node[2] != goal_pt:
        if y+1 < 600:
            move_up(current_node)
        if y-1 >= 0:
            move_down(current_node)
        if x+1 < 250:
            move_right(current_node)
        if x-1 >= 0:
            move_left(current_node)
        if x+1 < 600 and y+1 < 250:
            move_up_right(current_node)
        if x-1 >=0 and y+1 < 250:
            move_up_left(current_node)
        if x+1 < 600 and y-1 >= 0:
            move_down_right(current_node)
        if x-1 >=0 and y-1 >= 0:
            move_down_left(current_node)
    else:
        print("Reached Goal")
        stop = time.time()
        print("Time: ",stop - start)   
        break
