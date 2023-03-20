from includes import *

if __name__ == '__main__':
    
    #### Clearance of the Obstacle ####
    # c = input("Assign Clearance to the Obstacles: ")
    # c = int(c)
    c = 2
    #### Radius of the Robot ####
    # r = input("Enter the Radius of the Robot: ") 
    # r = int(r)
    r = 2
    
    #### Step Size of the Robot ####
    # robot_step_size = input("Enter Step size of the Robot: ")
    # robot_step_size = int(robot_step_size)
    robot_step_size = 1

    #### Taking start node coordinates as input from user #####
    # start_coordinates = input("Enter coordinates for Start Node: ")
    # start_x, start_y = start_coordinates.split()
    # start_x = int(start_x)
    # start_y = int(start_y)
    start_x = 11
    start_y = 11
    
    #### Taking Orientation for the robot ####
    # s_theta = input("Enter Orientation of the robot at start node: ")
    # start_theta = int(s_theta)

    start_theta = 30
    
    ### Checking if the user input is valid #####
    if robot_radius_space(start_x, start_y, c, r):
        print("Start node is out of bounds")
        exit(-1)
        
    if not (start_theta%30)==0:
        print("Orientation has to be a multiple of 30")
        exit(-1)
		    
	##### Taking Goal node coordinates as input from user ##### 
    # goal_coordinates = input("Enter coordinates for Goal Node: ")
    # goal_x, goal_y = goal_coordinates.split()
    # goal_x = int(goal_x)
    # goal_y = int(goal_y)
    goal_x = 125
    goal_y = 580
    
    #### Taking Orientation for the robot ####
    # g_theta = input("Enter Orientation of the robot at goal node: ")
    # goal_theta = int(g_theta)
    goal_theta = 60
    
    if robot_radius_space(goal_x, goal_y, c, r):
        print("Goal node is out of bounds")
        exit(-1)
        
    if not (goal_theta%30)==0:
        print("Orientation has to be a multiple of 30")
        exit(-1)
    
    start_node = Node(start_x, start_y,start_theta, 0.0, -1,0)
    goal_node = Node(goal_x, goal_y,goal_theta, 0.0, -1, 0)
    all_nodes,flag = a_star(start_node, goal_node, robot_step_size, c, r)
    
    if (flag)==1:
        universal_path = backtrack(goal_node)
    else:
        print("Robot cannot explore with current robot radius and clearance, please try again!")
        exit(-1)

    animate(all_nodes, universal_path, c, r)


	



	











