# Dijkstra_Path_Planning

Libraries used:
1. numpy
2. matplotlib.pyplot
3. matplotlib.animations
4. matplotlib.patches
5. queue

## Assumptions for the Dijkstra Algorithm used:

1. Robot is a point robot(radius = 0)
2. Robot has a clearance of 5mm (I have added this as a boundary to the obstacles itself)
3. Workspace of algorithm is an 8-connected space. 
4. Upward, Downward, Right and Left cost is 1.0
5. Cost of moving diagonally between Up-left, Up-right, Down-left and Down-right is 1.4

<p align="center">
<img src="https://user-images.githubusercontent.com/40595475/226610198-59d4b1ac-3c18-4875-b51a-4caad5e34592.png" alt= “” width="400" height="300">
</p>
<p align="center"> Fig1. Cost function definition </p>

<p align="center">
<img src="https://user-images.githubusercontent.com/40595475/226610891-f5fa8f53-f09c-4273-9f91-ad29ce2cead3.png" alt= “” width="600" height="300">
</p>
<p align="center"> Fig2. Field Dimensions </p>


We can run the code using the following command:

    python3 dijkstra_Rohan_Maan.py

Enter the source and destination in the following format:

    0,0
  
    10,10
  
<p align="center">
<img src="https://user-images.githubusercontent.com/40595475/224509485-52936d3a-9ba7-4836-a3db-4a1437708bac.png" alt= “” width="650" height="300">
</p>
<p align="center"> Fig3. Dijkstra Path Planning </p>
 
