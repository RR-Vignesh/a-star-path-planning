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

create_obstacle_map()
start_node, goal_node = get_input()
