import math 
from queue import PriorityQueue
import time
import pygame as pyg

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

def check_obstacle_space(node, rad):
    robot_space = ((node[0],node[1]),(node[0]+rad,node[1]), (node[0]-rad,node[1]), (node[0],node[1]+rad), (node[0],node[1]-rad))
    for robot_pos in robot_space:
        if robot_pos in obstacle_points:
            return False
        
    return True

# get input and check if valid or not
def get_input():
    clearance = int(input("Enter the clearance of the mobile robot"))
    l = int(input("Enter the step size L of the mobile robot (between 1-10)"))
    rad = int(input("Enter the radius of the mobile robot"))
    accept_start_node, accept_goal_node = True, True
    while accept_start_node:
        start_x = int(input("Enter start x: "))
        start_y = int(input("Enter start y: "))
        start_node = (start_x, start_y)
        robot_status = check_obstacle_space(start_node, rad)
        if robot_status == True:
            accept_start_node = False
            start_theta = int(input("Enter orientation of the start node in degrees (between 0 to 360 degrees): "))
            start_node = (start_x, start_y, start_theta)
        else:
            print("Entered start node is in obstacle. Please enter a valid co-ordinate...")

    while accept_goal_node:    
        goal_x = int(input("Enter goal x: "))
        goal_y = int(input("Enter goal y: "))        
        goal_node = (goal_x, goal_y)
        if goal_node not in obstacle_points:
            accept_goal_node = False
            goal_theta = int(input("Enter orientation of the goal node in degrees (between 0 to 360 degrees): "))
            goal_node = (goal_x, goal_y, goal_theta)
        else:
            print("Entered goal node is in obstacle. Please enter a co-ordinate...")
    

    return start_node, goal_node, clearance, l

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
    next_point = (current_point[0] + l, current_point[1])  
    next_angle = current_point[2]
    # update angle for other moves

    if next_point not in visited_nodes and next_point not in obstacle_points:
        cost = l
        updated_cost = curr_node[1] + int(cost)        
        next_node = (updated_cost + eclidean_distance(next_point, goal_pt),updated_cost, next_point)
        for i in range(map_queue.qsize()):
            #if map_queue.queue[i][2] == next_point:
            if eclidean_distance(next_point,map_queue.queue[i][2]) < 0.5:
                if map_queue.queue[i][1] > updated_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = current_point
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = current_point

# function to track back from the goal node to the start node to get the shortest path
def back_tracking(path_info, initial, current):
    child = path_info.get(current)
    current_tuple = tuple(current)
    child_tuple = tuple(child)
    shortest_path.append(current_tuple)
    shortest_path.append(child_tuple)
    while child != initial:  
        child = path_info.get(child)
        child_tuple = tuple(child)
        shortest_path.append(child_tuple)
    return shortest_path

# to flip the coordinates because of the origin change in pygame
def flip_points(points, height):
    return (points[0], height - points[1])

def flip_object_points(points, height, object_height):
    return (points[0], height - points[1] - object_height)

def pygame_visualization(visited_nodes, shortest_path):
    pyg.init()
    window = pyg.display.set_mode((X_SIZE,Y_SIZE))

    obstacle_color = "red"
    clearance_color = "pink"
    condition = True
    clock = pyg.time.Clock()

    rect2_clearance = flip_object_points([95, 0], 250, 105)
    rect1_clearance = flip_object_points([95, 145], 250, 105)
    rect2_original = flip_object_points([100, 0], 250, 100)
    rect1_original = flip_object_points([100, 150], 250, 100)

    triangle1_clearance = flip_points([455, 20], 250)
    triangle2_clearance = flip_points([463, 20], 250)
    triangle3_clearance = flip_points([515.5, 125], 250)
    triangle4_clearance = flip_points([463, 230], 250)
    triangle5_clearance = flip_points([455, 230], 250)

    triangle1 = (460, 25)
    triangle2 = (460, 225)
    triangle3 = (510, 125)

    hexagon1_clearance = (300, 205.76)
    hexagon2_clearance = (230, 165.38)
    hexagon3_clearance = (230, 84.61)
    hexagon4_clearance = (300, 44.23)
    hexagon5_clearance = (370, 84.61)
    hexagon6_clearance = (370, 165.38)

    hexagon1_org = (235,87.5)
    hexagon2_org = (300,50)
    hexagon3_org = (365,87.5)
    hexagon4_org = (365,162.5)
    hexagon5_org = (300,200)
    hexagon6_org = (235,162.5)

    while condition:
        for loop in pyg.event.get():
            if loop.type == pyg.QUIT:
                condition = False

        pyg.draw.rect(window, clearance_color, pyg.Rect(rect2_clearance[0], rect2_clearance[1], 60, 105))
        pyg.draw.rect(window, clearance_color, pyg.Rect(rect1_clearance[0], rect1_clearance[1], 60, 105))
        pyg.draw.rect(window, obstacle_color, pyg.Rect(rect2_original[0], rect2_original[1], 50, 100))
        pyg.draw.rect(window, obstacle_color, pyg.Rect(rect1_original[0], rect1_original[1], 50, 100))

        pyg.draw.polygon(window, clearance_color, ((triangle1_clearance),(triangle2_clearance),(triangle3_clearance), (triangle4_clearance), (triangle5_clearance)))
        pyg.draw.polygon(window, obstacle_color, ((triangle1),(triangle2),(triangle3)))

        pyg.draw.polygon(window, clearance_color, ((hexagon1_clearance),(hexagon2_clearance),(hexagon3_clearance),(hexagon4_clearance),(hexagon5_clearance),(hexagon6_clearance)))
        pyg.draw.polygon(window, obstacle_color, ((hexagon1_org),(hexagon2_org),(hexagon3_org),(hexagon4_org),(hexagon5_org),(hexagon6_org)))

        pyg.draw.rect(window, clearance_color ,pyg.Rect(0, 0, 600, 5))
        pyg.draw.rect(window, clearance_color ,pyg.Rect(0, 245, 600, 5))
        pyg.draw.rect(window, clearance_color ,pyg.Rect(0, 0, 5, 250))
        pyg.draw.rect(window, clearance_color ,pyg.Rect(595, 0, 5, 250))

        for node in visited_nodes:
            pyg.draw.circle(window, "white", flip_points(node, 250), 1)
            pyg.display.flip()
            clock.tick(700)

        for node in shortest_path:
            pyg.draw.circle(window, "teal", flip_points(node, 250), 1)
            pyg.display.flip()
            clock.tick(10)

        pyg.display.flip()
        pyg.time.wait(3000)
        condition = False
    pyg.quit()

create_obstacle_map()
start_node, goal_node, clearance, l = get_input()
# print(eclidean_distance((0, 0), (1, 1)))
start = time.time()
map_queue = PriorityQueue()
start_pt = (start_node[0], start_node[1])
goal_pt = (goal_node[0], goal_node[1])
map_queue.put((eclidean_distance(start_pt, goal_pt), 0, start_pt))
#map_queue.put((eclidean_distance(start_pt, goal_pt), 0, start_node))
# print(map_queue.queue)

visited_nodes = []
parent_child_info = {}
shortest_path = []

while True:
    current_node = map_queue.get()
    #print(current_node)
    visited_nodes.append(current_node[2])
    x, y = current_node[2][0], current_node[2][1]
    #if current_node[2] != goal_pt:
    if eclidean_distance((x,y), goal_pt) > 1.5:
        # if y+1 < 600:
        #     move_up(current_node)
        # if y-1 >= 0:
        #     move_down(current_node)
        # if x+1 < 250:
        #     move_right(current_node)
        # if x-1 >= 0:
        #     move_left(current_node)
        # if x+1 < 600 and y+1 < 250:
        #     move_up_right(current_node)
        # if x-1 >=0 and y+1 < 250:
        #     move_up_left(current_node)
        # if x+1 < 600 and y-1 >= 0:
        #     move_down_right(current_node)
        # if x-1 >=0 and y-1 >= 0:
        #     move_down_left(current_node)
        if x+l < 600:
            move_right(current_node)

    else:
        print("Reached Goal")
        stop = time.time()
        print("Time: ",stop - start)   
        shortest = back_tracking(parent_child_info, start_pt, goal_pt)
        shortest.reverse()  
        print(shortest)
        break

pygame_visualization(visited_nodes, shortest_path)