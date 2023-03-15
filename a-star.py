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

create_obstacle_map()
