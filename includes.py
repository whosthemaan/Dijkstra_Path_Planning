import heapq
import cv2
import numpy as np
from math import dist

y_field = 250
x_field = 600

class Node:

    def __init__(self, x, y, theta, cost, parent_index, cost_to_go = 0):
        self.x = x
        self.y = y
        self.theta = theta
        self.cost = cost
        self.parent_index = parent_index
        self.cost_to_go = cost_to_go 
        
    def __lt__(self,other):
        return self.cost + self.cost_to_go < other.cost + other.cost_to_go

def move_cal(move,x,y,theta,step_size,cost):
    theta = theta + move
    x = x + (step_size*np.cos(np.radians(theta)))
    y = y + (step_size*np.sin(np.radians(theta)))
    x = round(x)
    y = round(y)
    cost = 1 + cost
    return x,y,theta,cost

def c_space(y, x):
    # wall
    # wall = y >= (1 + c) and y <= (y_field - c) and x >= (1 + c) and x <= (x_field - c)

    # check if the point lies inside the hexagon
    (x1, y1) = (300,50)
    (x2, y2) = (365,87)
    (x3, y3) = (365,162)
    (x4, y4) = (300,200)
    (x5, y5) = (235,162)
    (x6, y6) = (235,87)
    side1 = ((y - y1) * (x2 - x1)) - ((y2 - y1) * (x - x1))
    side2 = ((y - y2) * (x3 - x2)) - ((y3 - y2) * (x - x2))
    side3 = ((y - y3) * (x4 - x3)) - ((y4 - y3) * (x - x3))
    side4 = ((y - y4) * (x5 - x4)) - ((y5 - y4) * (x - x4))
    side5 = ((y - y5) * (x6 - x5)) - ((y6 - y5) * (x - x5))
    side6 = ((y - y6) * (x1 - x6)) - ((y1 - y6) * (x - x6))
    hex = 1
    if(side1 >= 0 and side2 >= 0 and side3 >= 0 and side4 >= 0 and side5 >= 0 and side6 >= 0):
        hex = 0

    # check if the point lies inside the triangle
    (x1, y1) = (460, 25)
    (x2, y2) = (510, 125)
    (x3, y3) = (460, 225)
    side1 = ((y - y1) * (x2 - x1)) - ((y2 - y1) * (x - x1))
    side2 = ((y - y2) * (x3 - x2)) - ((y3 - y2) * (x - x2))
    side3 = x - x3
    tri = 1
    if (side1 >= 0 and side2 >= 0 and side3 >= 0) or (side1 <= 0 and side2 <= 0 and side3 <= 0):
        tri = 0
        
    # check if the point lies inside the rectangle2
    (x1, y1) = (100, 150)
    (x2, y2) = (150, 150)
    (x3, y3) = (150, 250)
    (x4, y4) = (100, 250)
    side1 = y - y1
    side2 = x - x2
    side3 = y - y3
    side4 = x - x4
    rect2 = 1
    if(side1 >= 0 and side2 <= 0 and side3 <= 0 and side4 >= 0):
        rect2 = 0

    # check if the point lies inside the rectangle1
    (x1, y1) = (100,0)
    (x2, y2) = (150,0)
    (x3, y3) = (150, 100)
    (x4, y4) = (100, 100)
    side1 = y - y1
    side2 = x - x2
    side3 = y - y3
    side4 = x - x4
    rect1 = 1
    if(side1 >= 0 and side2 <= 0 and side3 <= 0 and side4 >= 0):
        rect1 = 0
    
    if(tri == 0 or rect2 == 0 or hex == 0 or rect1 == 0):
        return True
    return False

def clearance_space(y, x, c):
    # wall
    wall = y >= (1 + c) and y <= (y_field - c) and x >= (1 + c) and x <= (x_field - c)

    # check if the point lies inside the hexagon
    (x1, y1) = (300,50-c)
    (x2, y2) = (365+c,87)
    (x3, y3) = (365+c,162)
    (x4, y4) = (300,200+c)
    (x5, y5) = (235-c,162)
    (x6, y6) = (235-c,87)
    side1 = ((y - y1) * (x2 - x1)) - ((y2 - y1) * (x - x1))
    side2 = ((y - y2) * (x3 - x2)) - ((y3 - y2) * (x - x2))
    side3 = ((y - y3) * (x4 - x3)) - ((y4 - y3) * (x - x3))
    side4 = ((y - y4) * (x5 - x4)) - ((y5 - y4) * (x - x4))
    side5 = ((y - y5) * (x6 - x5)) - ((y6 - y5) * (x - x5))
    side6 = ((y - y6) * (x1 - x6)) - ((y1 - y6) * (x - x6))
    hex = 1
    if(side1 >= 0 and side2 >= 0 and side3 >= 0 and side4 >= 0 and side5 >= 0 and side6 >= 0):
        hex = 0

    # check if the point lies inside the triangle
    side1 = y - 2*x + 895 + 2*c
    side2 = 2*x + y - 1145 - 2*c
    side3 = x - (460 - c)
    tri = 1

    if (side1 >= 0 and side2 <= 0 and side3 >= 0):
        tri = 0
        
    # check if the point lies inside the rectangle2
    (x1, y1) = (100, 150)
    (x2, y2) = (150, 150)
    (x3, y3) = (150, 250)
    (x4, y4) = (100, 250)
    side1 = y - (y1-c)
    side2 = x - (x2+c)
    side3 = y - (y3+c)
    side4 = x - (x4-c)
    rect2 = 1
    if(side1 >= 0 and side2 <= 0 and side3 <= 0 and side4 >= 0):
        rect2 = 0

    # check if the point lies inside the rectangle1
    (x1, y1) = (100,0)
    (x2, y2) = (150,0)
    (x3, y3) = (150, 100)
    (x4, y4) = (100, 100)
    side1 = y - (y1-c)
    side2 = x - (x2+c)
    side3 = y - (y3+c)
    side4 = x - (x4-c)
    rect1 = 1
    if(side1 >= 0 and side2 <= 0 and side3 <= 0 and side4 >= 0):
        rect1 = 0
    
    if(tri == 0 or rect2 == 0 or hex == 0 or rect1 == 0 or wall==0):
        return True
    return False

def robot_radius_space(y, x, c, r):
    # wall
    c = c + r
    wall = y >= (1 + c) and y <= (y_field - c) and x >= (1 + c) and x <= (x_field - c)

    # check if the point lies inside the hexagon
    (x1, y1) = (300,50-c)
    (x2, y2) = (365+c,87)
    (x3, y3) = (365+c,162)
    (x4, y4) = (300,200+c)
    (x5, y5) = (235-c,162)
    (x6, y6) = (235-c,87)
    side1 = ((y - y1) * (x2 - x1)) - ((y2 - y1) * (x - x1))
    side2 = ((y - y2) * (x3 - x2)) - ((y3 - y2) * (x - x2))
    side3 = ((y - y3) * (x4 - x3)) - ((y4 - y3) * (x - x3))
    side4 = ((y - y4) * (x5 - x4)) - ((y5 - y4) * (x - x4))
    side5 = ((y - y5) * (x6 - x5)) - ((y6 - y5) * (x - x5))
    side6 = ((y - y6) * (x1 - x6)) - ((y1 - y6) * (x - x6))
    hex = 1
    if(side1 >= 0 and side2 >= 0 and side3 >= 0 and side4 >= 0 and side5 >= 0 and side6 >= 0):
        hex = 0

    # check if the point lies inside the triangle
    side1 = y - 2*x + 895 + 2*c
    side2 = 2*x + y - 1145 - 2*c
    side3 = x - (460 - c)
    tri = 1

    if (side1 >= 0 and side2 <= 0 and side3 >= 0):
        tri = 0
        
    # check if the point lies inside the rectangle2
    (x1, y1) = (100, 150)
    (x2, y2) = (150, 150)
    (x3, y3) = (150, 250)
    (x4, y4) = (100, 250)
    side1 = y - (y1-c)
    side2 = x - (x2+c)
    side3 = y - (y3+c)
    side4 = x - (x4-c)
    rect2 = 1
    if(side1 >= 0 and side2 <= 0 and side3 <= 0 and side4 >= 0):
        rect2 = 0

    # check if the point lies inside the rectangle1
    (x1, y1) = (100,0)
    (x2, y2) = (150,0)
    (x3, y3) = (150, 100)
    (x4, y4) = (100, 100)
    side1 = y - (y1-c)
    side2 = x - (x2+c)
    side3 = y - (y3+c)
    side4 = x - (x4-c)
    rect1 = 1
    if(side1 >= 0 and side2 <= 0 and side3 <= 0 and side4 >= 0):
        rect1 = 0
    
    if(tri == 0 or rect2 == 0 or hex == 0 or rect1 == 0 or wall==0):
        return True
    return False

def goal_reached(current, goal):
    if dist((current.x, current.y), (goal.x, goal.y))  < 1.5:
        return True
    else:
        return False

def generate_key(node):
    generate_key = 1021*node.x + 112*node.y 
    return generate_key

def a_star(start,goal,step_size, c, r):                       

    if goal_reached(start, goal):
        return None,1
    
    moves = [60, 30, 0, -30, -60]
    unvisited = {}  
    
    start_key = generate_key(start) 
    unvisited[(start_key)] = start
    
    visited = {}
    queue = [] 
    heapq.heappush(queue, [start.cost, start]) 
    all_nodes = [] 
    
    while (queue):
        current_node = (heapq.heappop(queue))[1]
        all_nodes.append([current_node.x, current_node.y, current_node.theta])          
        current_index = generate_key(current_node)
        if goal_reached(current_node, goal):
            goal.parent_index = current_node.parent_index
            goal.cost = current_node.cost
            print("Goal Node Reached!!!")
            return all_nodes,1

        if current_index in visited:  
            continue
        else:
            visited[current_index] = current_node
		
        del unvisited[current_index]

        for move in moves:
            x,y,theta,cost = move_cal(move,current_node.x,current_node.y,current_node.theta, step_size, current_node.cost)

            # Heuristic based on distance
            cost_to_go = dist((x, y), (goal.x, goal.y))  
   
            new_node = Node(x,y,theta, cost,current_node, cost_to_go)   
   
            new_node_id = generate_key(new_node) 
   
            if robot_radius_space(new_node.x, new_node.y, c, r):
                continue
            elif new_node_id in visited:
                continue
   
            if new_node_id in unvisited:
                if new_node.cost < unvisited[new_node_id].cost: 
                    unvisited[new_node_id].cost = new_node.cost
                    unvisited[new_node_id].parent_index = new_node.parent_index
            else:
                unvisited[new_node_id] = new_node
   			
            heapq.heappush(queue, [(new_node.cost + new_node.cost_to_go), new_node]) 
   
    return  all_nodes, 0

def backtrack(goal):  
    universal_path = []
    universal_path.append((goal.y, goal.x))

    parent = goal.parent_index
    while parent != -1:
        universal_path.append((parent.y, parent.x))
        parent = parent.parent_index
        
    universal_path.reverse()

    universal_path = np.asarray(universal_path)
    
    return universal_path
    
def animate(explored, back_track, c, r):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    path="./A_Star.avi"
    out = cv2.VideoWriter(path, fourcc, 60.0, (x_field, y_field))
    field = np.zeros((y_field, x_field, 3), dtype=np.uint8)
    count = 0

    for i in range(x_field):
        for k in range(y_field):
            if robot_radius_space(k, i, c, r):
                field[k, i] = (125, 125, 125)
            elif not (k >= (1 + (c+r)) and k <= (y_field - (c+r)) and i >= (1 + (c+r)) and i <= (x_field - (c+r))):
                field[k, i] = (125, 125, 125)

    for i in range(x_field):
        for k in range(y_field):
            if clearance_space(k, i, c):
                field[k, i] = (255,255,255)
            elif not (k >= (1 + c) and k <= (y_field - c) and i >= (1 + c) and i <= (x_field - c)):
                field[k, i] = (255,255,255)

    for i in range(x_field):
        for k in range(y_field):
            if c_space(k, i):
                field[k, i] = (0,0,255)               

    for state in explored:
        field[int(y_field - state[0]), int(state[1])] = (255, 0, 0)
        if(count%100 == 0):
            out.write(field)
        count = count + 1

    count = 0
    for y in range(1, y_field + 1):
        for x in range(1, x_field + 1):
            if(field[int(y_field - y), int(x - 1), 0] == 0 and field[int(y_field - y), int(x - 1), 1] == 0 and field[int(y_field - y), int(x - 1), 2] == 0):
                if(c_space(y, x) == False):
                    field[int(y_field - y), int(x - 1)] = (154, 250, 0)
                    if(count%100 == 0):
                        out.write(field)
                    count = count + 1

    if(len(back_track) > 0):
        for state in back_track:
            field[int(y_field - state[1]), int(state[0] - 1)] = (0, 0, 255)
            out.write(field)
            cv2.imshow('result', field)
            cv2.waitKey(5)
            
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    out.release()
