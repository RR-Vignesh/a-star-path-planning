import math 
from queue import PriorityQueue
import time
import pygame as pyg
import numpy as np

obstacle_points = []

# size of the map
X_SIZE = 600
Y_SIZE = 250

def find_intersection_pt(slope1, slope2, intercept1, intercept2, a, b):
    A = np.array([[slope1, a], [slope2, b]])
    B = np.array([intercept1, intercept2])
    X = np.linalg.solve(A, B)
    print("X: ",X)
    return X

# create map with obstacle
def create_obstacle_map(clearance):
    points = []
    x_range = np.arange(0, X_SIZE+1, 0.5)
    y_range1 = np.arange(0, clearance+1, 0.5)
    y_range2 = np.arange(Y_SIZE - clearance, Y_SIZE + 1, 0.5)
    for xp in x_range:
        for yp in y_range1:
            points.append((xp,yp))
        for yp in y_range2:
            points.append((xp,yp))

    y_range = np.arange(0, Y_SIZE + 1, 0.5)
    x_range1 = np.arange(0, clearance+1, 0.5)
    x_range2 = np.arange(X_SIZE - clearance, X_SIZE + 1, 0.5)
    for yp in y_range:
        for xp in x_range1:
            points.append((xp,yp))
        for xp in x_range2:
            points.append((xp,yp))

    # Rectangles and clearance
    x_range = np.arange(100 - clearance, 150 + clearance + 1, 0.5)
    y_range = np.arange(0, Y_SIZE+1, 0.5)
    for xp in x_range:
        for yp in y_range:
            if yp <= (100 + clearance) or yp >= (150 - clearance):
                points.append((xp,yp))

    # triangle 
    x_range = np.arange(460-clearance, 510+2*clearance, 0.5)
    y_range = np.arange(0, Y_SIZE, 0.5)

    m1, m2 = 2, 2
    b1, b2 = 895, 1145
    
    c1 = b1 + clearance * (math.sqrt(pow(m2,2) + 1))
    c2 = b1 - clearance * (math.sqrt(pow(m2,2) + 1))
    c3 = b2 + clearance * (math.sqrt(pow(m1,2) + 1))
    c4 = b2 - clearance * (math.sqrt(pow(m1,2) + 1))
    
    for xp in x_range:
        for yp in y_range:            
            if (m1*xp - yp <= b1) and (m2*xp+yp <= b2):
                    points.append((xp,yp))

            if (m1*xp-yp <= min(c1, c2)) and (m2*xp+yp <= min(c3, c4)):
                    points.append((xp,yp)) 

    # Hexagon
    x_range = np.arange(300 - int(64.95) - clearance, 300 + int(64.95) + clearance, 0.5)
    y_range = np.arange(125 - 75 - clearance, 125 + 75 + clearance, 0.5)

    m = 15/26
    b1, b2, b3, b4 = 32.692, 378.846, 217.307, 128.846
    
    c1 = b1 + clearance * (math.sqrt(pow(m,2) + 1))
    c2 = b1 - clearance * (math.sqrt(pow(m,2) + 1))
    c3 = b2 + clearance * (math.sqrt(pow(m,2) + 1))
    c4 = b2 - clearance * (math.sqrt(pow(m,2) + 1))
    c5 = b3 + clearance * (math.sqrt(pow(m,2) + 1))
    c6 = b3 - clearance * (math.sqrt(pow(m,2) + 1))
    c7 = b4 + clearance * (math.sqrt(pow(m,2) + 1))
    c8 = b4 - clearance * (math.sqrt(pow(m,2) + 1))
    
    print(max(c1, c2))
    print(max(c3, c4))
    print(min(c5, c6))
    print(min(c7, c8))

    for xp in x_range:
        for yp in y_range:            
            if  (yp - m*xp - b1) < 0 and (yp + m*xp - b2) < 0 and (yp + m*xp - b3) > 0 and (yp - m*xp + b4) > 0:
                points.append((xp,yp))      
            
            if  (yp - m*xp - max(c1, c2)) < 0 and (yp + m*xp - max(c3, c4)) < 0 and (yp - m*xp - min(c5, c6)) > 0 and (yp + m*xp + min(c7, c8)) > 0:
                points.append((xp,yp))    
    
    hexagon_p1 = find_intersection_pt(-m, m, max(c1, c2), max(c3, c4), 1, 1)
    hexagon_p2 = find_intersection_pt(m, 1, max(c3, c4), 300 + 64.95 + clearance, 1, 0)
    hexagon_p3 = find_intersection_pt(1, -m, 300 + 64.95 + clearance, min(c5, c6), 0, 1)
    hexagon_p4 = find_intersection_pt(-m, m, min(c5, c6), -min(c7, c8), 1, 1)
    hexagon_p5 = find_intersection_pt(m, 1, -min(c7, c8), 300 - 64.95 -clearance, 1, 0)
    hexagon_p6 = find_intersection_pt(1, -m, 300 - 64.95-clearance, max(c1, c2), 0, 1)

    hexagon_pts = [hexagon_p1, hexagon_p2, hexagon_p3, hexagon_p4, hexagon_p5, hexagon_p6]
    return points, hexagon_pts

# Validating input values
def get_input():
    clearance = int(input("Enter the clearance of the mobile robot: "))
    rad = int(input("Enter the radius of the mobile robot: "))

    # Create Obstacle based on the clearance and radius of the robot
    obstacle_points = create_obstacle_map(clearance + rad)
    while True:
        l = int(input("Enter the step size L of the mobile robot (between 1-10): "))
        if l>=1 and l<=10:
            break
        else:
            print("Incorrect step size. Please enter positive step size between 1 and 10")

    accept_start_node, accept_goal_node = True, True
    while accept_start_node:
        start_x = int(input("Enter start x: "))
        start_y = int(input("Enter start y: "))
        start_node = (start_x, start_y)

        if start_node not in obstacle_points:
            accept_start_node = False
            while True:
                start_theta = int(input("Enter orientation of the start node in degrees (between 0 to 360 degrees): "))
                if start_theta % 30 == 0:
                    break
                else:
                    print("Incorrect theta value. Please enter positive theta in multiple of 30")
            start_node = (start_x, start_y, start_theta)
        else:
            print("Entered start node is in obstacle. Please enter a valid co-ordinate...")

    while accept_goal_node:    
        goal_x = int(input("Enter goal x: "))
        goal_y = int(input("Enter goal y: "))        
        goal_node = (goal_x, goal_y)
        if goal_node not in obstacle_points:
            accept_goal_node = False
            while True:
                goal_theta = int(input("Enter orientation of the goal node in degrees (between 0 to 360 degrees): "))
                if goal_theta % 30 == 0:
                    break
                else:
                    print("Incorrect theta value. Please enter positive theta in multiple of 30")

            goal_node = (goal_x, goal_y, goal_theta)
        else:
            print("Entered goal node is in obstacle. Please enter a co-ordinate...")
    

    return start_node, goal_node, clearance, l, rad, obstacle_points

def euclidean_distance(pt1, pt2):
    distance = math.sqrt(pow((pt1[0] - pt2[0]), 2) + pow((pt1[1] - pt2[1]),2))
    return round(distance, 2)

def round_nearest(val):
    if val-int(val)<0.5:
        val=int(val)
    elif val-int(val) == 0.5:
        val=val
    else:
        val = int(val)+1
    
    return val
    
def move_right(curr_node):
    global goal_reached
    current_point = (curr_node[3][0], curr_node[3][1])
    next_point = (current_point[0] + l, current_point[1])  
    next_angle = curr_node[3][2]
    if next_angle >= 360:
        next_angle-=360
    if next_angle < 0:
        next_angle+=360

    # round off next point to nearest 0.5
    next_point = (round_nearest(next_point[0]), round_nearest(next_point[1]), next_angle)
    """ print("The next point after rounding off is :")
    print(next_point) """
    
    ## Obstacle with clearance
    if visited_nodes[int(next_point[0]*2)][int(next_point[1]*2)][int(next_point[2]/30)] != 1 and (next_point[0],next_point[1]) not in obstacle_points:
        cost_to_come = curr_node[2] + l 
        cost_to_go = euclidean_distance(next_point, goal_pt)    
        total_cost =  cost_to_come + cost_to_go
        next_node = (total_cost ,cost_to_go, cost_to_come, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][3] == next_point:
                if map_queue.queue[i][0] > total_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = curr_node[3]
                    return
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = curr_node[3]
        if cost_to_go < 1.5:
            goal_reached = True

def move_plus_30(curr_node):
    global goal_reached
    current_point = (curr_node[3][0], curr_node[3][1])
    next_point = (current_point[0] + l*math.cos(np.deg2rad(curr_node[3][2]) + math.pi/6)), current_point[1] + l*math.sin(np.deg2rad(curr_node[3][2]) + math.pi/6) 
    next_angle = curr_node[3][2] + 30
    if next_angle >= 360:
        next_angle-=360
    if next_angle < 0:
        next_angle+=360
    # round off next point to nearest 0.5
    next_point = (round_nearest(next_point[0]), round_nearest(next_point[1]), next_angle)
    
    ## Obstacle with clearance
    if visited_nodes[int(next_point[0]*2)][int(next_point[1]*2)][int(next_point[2]/30)] != 1 and (next_point[0],next_point[1]) not in obstacle_points:
        cost_to_come = curr_node[2] + l 
        cost_to_go = euclidean_distance(next_point, goal_pt)
        total_cost = cost_to_come + cost_to_go     
        next_node = (total_cost, cost_to_go, cost_to_come, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][3] == next_point:
            #if euclidean_distance(next_point,map_queue.queue[i][2]) <= 0.5 and (next_angle - map_queue.queue[i][2][2]) <= 30:
                if map_queue.queue[i][0] > total_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = curr_node[3]
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = curr_node[3]
        if cost_to_go < 1.5:
            goal_reached = True

def move_plus_60(curr_node):
    global goal_reached
    current_point = (curr_node[3][0], curr_node[3][1])
    next_point = ((current_point[0] + l*math.cos(np.deg2rad(curr_node[3][2]) + math.pi/3)), current_point[1] + l*math.sin(np.deg2rad(curr_node[3][2]) + math.pi/3))  
    next_angle = curr_node[3][2] + 60
    if next_angle >= 360:
        next_angle-=360
    if next_angle < 0:
        next_angle+=360
    # round off next point to nearest 0.5
    next_point = (round_nearest(next_point[0]), round_nearest(next_point[1]), next_angle)
    
    ## Obstacle with clearance
    if visited_nodes[int(next_point[0]*2)][int(next_point[1]*2)][int(next_point[2]/30)] != 1 and (next_point[0],next_point[1]) not in obstacle_points:
        cost_to_come = curr_node[2] + l 
        cost_to_go = euclidean_distance(next_point, goal_pt) 
        total_cost = cost_to_come + cost_to_go   
        next_node = (total_cost, cost_to_go, cost_to_come, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][3] == next_point:
            #if euclidean_distance(next_point,map_queue.queue[i][2]) <= 0.5 and (next_angle - map_queue.queue[i][2][2]) <= 30:
                if map_queue.queue[i][0] > total_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = curr_node[3]
                    return 
                else:
                    return 
        map_queue.put(next_node)
        parent_child_info[next_point] = curr_node[3]
        if cost_to_go < 1.5:
            goal_reached = True

def move_minus_30(curr_node):
    global goal_reached
    current_point = (curr_node[3][0], curr_node[3][1])
    next_point = ((current_point[0] + l*math.cos(np.deg2rad(curr_node[3][2])-math.pi/6)), current_point[1] + l*math.sin(np.deg2rad(curr_node[3][2])-math.pi/6))  
    next_angle = curr_node[3][2] - 30
    if next_angle >= 360:
        next_angle-=360
    if next_angle < 0:
        next_angle+=360
    # round off next point to nearest 0.5
    next_point = (round_nearest(next_point[0]), round_nearest(next_point[1]), next_angle)
    
    ## Obstacle with clearance
    if visited_nodes[int(next_point[0]*2)][int(next_point[1]*2)][int(next_point[2]/30)] != 1 and (next_point[0],next_point[1]) not in obstacle_points:
        cost_to_come = curr_node[2] + l 
        cost_to_go = euclidean_distance(next_point, goal_pt)  
        total_cost = cost_to_come + cost_to_go  
        next_node = (total_cost, cost_to_go, cost_to_come, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][3] == next_point:
            #if euclidean_distance(next_point,map_queue.queue[i][2]) <= 0.5 and (next_angle - map_queue.queue[i][2][2]) <= 30:
                if map_queue.queue[i][0] > total_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = curr_node[3]
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = curr_node[3]
        if cost_to_go < 1.5:
            goal_reached = True

def move_minus_60(curr_node):
    global goal_reached
    current_point = (curr_node[3][0], curr_node[3][1])
    next_point = ((current_point[0] + l*math.cos(np.deg2rad(curr_node[3][2])-math.pi/3)), current_point[1] + l*math.sin(np.deg2rad(curr_node[3][2])-math.pi/3))  
    next_angle = curr_node[3][2] - 60
    if next_angle >= 360:
        next_angle-=360
    if next_angle < 0:
        next_angle+=360
    # round off next point to nearest 0.5
    next_point = (round_nearest(next_point[0]), round_nearest(next_point[1]), next_angle)
    
    ## Obstacle with clearance
    if visited_nodes[int(next_point[0]*2)][int(next_point[1]*2)][int(next_point[2]/30)] != 1 and (next_point[0],next_point[1]) not in obstacle_points:
        cost_to_come = curr_node[2] + l 
        cost_to_go = euclidean_distance(next_point, goal_pt) 
        total_cost =  cost_to_come + cost_to_go   
        next_node = (total_cost , cost_to_go, cost_to_come, next_point)
        for i in range(map_queue.qsize()):
            if map_queue.queue[i][3] == next_point:
            #if euclidean_distance(next_point,map_queue.queue[i][2]) <= 0.5 and (next_angle - map_queue.queue[i][2][2]) <= 30:
                if map_queue.queue[i][0] > total_cost:
                    map_queue.queue[i] = next_node 
                    parent_child_info[next_point] = curr_node[3]
                    return 
                else:
                    return
        map_queue.put(next_node)
        parent_child_info[next_point] = curr_node[3]
        if cost_to_go < 1.5:
            goal_reached = True


# function to track back from the goal node to the start node to get the shortest path

def back_tracking(path, initial_state, curr_val):
    optimal_path = []
    optimal_path.append(curr_val)
    parent_path = (curr_val)
    while parent_path != initial_state:  
        parent_path = path[parent_path]
        optimal_path.append(parent_path)
    
    optimal_path.reverse()
    return optimal_path

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

# Obtaining and validating the input from the user
start_node, goal_node, clearance, l, radius, obstacle_points = get_input()

start = time.time()
map_queue = PriorityQueue()
start_pt = (start_node[0], start_node[1])
goal_pt = (goal_node[0], goal_node[1])
map_queue.put((euclidean_distance(start_pt, goal_pt), euclidean_distance(start_pt, goal_pt), 0, start_node))

visited_nodes = np.zeros((1200,500,12), dtype=int)
parent_child_info = {}
shortest_path = []

visualization_points = create_obstacle_map(clearance)
goal_reached = False
while map_queue.qsize() != 0:
    current_node = map_queue.get()
    x, y = current_node[3][0], current_node[3][1]
    #print("The current node inside the while True is : ")
    #print(current_node)
    if visited_nodes[int(x*2)][int(y*2)][int(current_node[3][2]/30)] != 1:
        visited_nodes[int(x*2)][int(y*2)][int(current_node[3][2]/30)]=1
        if euclidean_distance((x,y), goal_pt) > 1.5:
        # if check_obstacle_space((x+radius+l,y)) < 600:
        ### change the limits to max x and y size
            if x >0  and x+l < X_SIZE and y>0 and y<Y_SIZE:
                move_right(current_node)
            if goal_reached == False and x>0 and y>0 and x+(l*math.cos(np.deg2rad(current_node[3][2]) + math.pi/6)) < X_SIZE and y+(l*math.sin(math.pi/6)) < Y_SIZE:
                move_plus_30(current_node)
            if goal_reached == False and x>0 and y>0 and x+(l*math.cos(np.deg2rad(current_node[3][2]) + math.pi/3)) < X_SIZE and y+(l*math.sin(np.deg2rad(current_node[3][2]) + math.pi/3)) < Y_SIZE:
                move_plus_60(current_node)
            if goal_reached == False and x>0 and y>0 and x+(l*math.cos(np.deg2rad(current_node[3][2]) - math.pi/6)) < X_SIZE and y+(l*math.sin(np.deg2rad(current_node[3][2]) - math.pi/6)) < Y_SIZE:
                move_minus_30(current_node)
            if goal_reached == False and x>0 and y>0 and x+(l*math.cos(np.deg2rad(current_node[3][2]) - math.pi/3)) < X_SIZE and y+(l*math.sin(np.deg2rad(current_node[3][2]) - math.pi/3)) < Y_SIZE:
                move_minus_60(current_node)

        else:
            print("Reached Goal")
            stop = time.time()
            print("Time: ",stop - start)   
            #shortest = back_tracking(parent_child_info, start_pt, goal_pt)
            shortest = back_tracking(parent_child_info, start_node, current_node[3])
            #shortest.reverse()  
            print(shortest)
            break

#pygame_visualization(visited_nodes, shortest_path)