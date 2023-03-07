# Youtube Video link - https://youtu.be/q70aM7p1eg4
# Github link - https://github.com/whosthemaan/Dijkstra_Path_Planning

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Polygon
from Func import  check_obstacle, dijkstra, get_shapes
import os

def init():
    scatter_plot.set_offsets([])
    return scatter_plot

def animation_func(index, last_visited):
    if(index<=last_visited):
        line.set_data(path_x[0], path_y[0])
        data = np.hstack((visited_x[:index,np.newaxis], visited_y[:index, np.newaxis]))
        scatter_plot.set_offsets(data)
    else:
        line.set_data(path_x[:(index-last_visited)*30], path_y[:(index-last_visited)*30])
    return scatter_plot, line

if __name__ == "__main__":
    source_x, source_y, destination_x, destination_y = 0, 0, 0, 0

    while True:
        print("Enter source points as X,Y :")
        source = input()
        source_x = int(source.split(",")[0])
        source_y = int(source.split(",")[1])

        print("Enter destination points as X,Y :")
        destination = input()
        destination_x = int(destination.split(",")[0])
        destination_y = int(destination.split(",")[1])
    
        if(check_obstacle([source_x, source_y]) and check_obstacle([destination_x, destination_y])):
            break
        else:
            print("Please enter valid input :")
            continue

    source = (source_x, source_y)
    destination = (destination_x, destination_y)
    print("Source is : ", source)
    print("Destination is : ", destination)

    fig = plt.figure()
    axis = plt.axes(xlim=(0, 600), ylim=(0, 250))
    axis.set_facecolor('k')

    path, visited = dijkstra(source, destination)
    path.append(source)
    path.insert(0, destination)

    visited_x, visited_y = (np.array(visited)[:,0], np.array(visited)[:,1])

    path_x, path_y = (np.array(path)[:,0], np.array(path)[:,1])

    line, = axis.plot(path_x, path_y, color = 'g')
    scatter_plot = axis.scatter([], [], s=2, color='w')

    shapes = get_shapes()
    for index in shapes:
        axis.add_patch(index)

    animator = FuncAnimation(fig, animation_func, frames = (len(visited)+len(path)) ,fargs=[len(visited)], interval=0.01, repeat=False, blit=True)
    print("Saving animation, Please wait for sometime. Thanks. :)")
    gif_writer = PillowWriter(fps=60)
    animator.save('video.gif', writer=gif_writer)
    plt.show()

    
    
