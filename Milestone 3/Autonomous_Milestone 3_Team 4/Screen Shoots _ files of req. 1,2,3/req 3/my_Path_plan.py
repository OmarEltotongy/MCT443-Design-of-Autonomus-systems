#!/usr/bin/env python

import numpy as np #Imports Numpy package full of functions and methods that can be used.
import rospy
Iterations=0

def Draw_Horizontal(Array,Index1,Index2):   #Draws A horizontal Line from index1 to index2
    Local_Counter = Index1[1]
    while(Local_Counter <= Index2[1]):
        Array[Index1[0],Local_Counter]= 0
        Local_Counter+=1
        
def Draw_Vertical(Array,Index1,Index2):    #Draws A Vertical Line from index1 to index2
    Local_Counter = Index1[0]
    while(Local_Counter <= Index2[0]):
        Array[Local_Counter,Index1[1]]= 0
        Local_Counter+=1

def Draw(Map):    #Draws a Map

    Draw_Horizontal(Map,[0,0],[0,9])
    Draw_Horizontal(Map,[9,0],[9,9])
    Draw_Vertical(Map,[0,0],[9,0])        # EDGES
    Draw_Vertical(Map,[0,9],[9,9])


def BFS(Map,Start,Goal,Direction):  # Direction for CCW -1  for CW 1

    Flag = False # Flag indicating if goal node is found
    
    # Initializing a queue 
    queue = []
    queue.append(Start)

    # Visited Nodes
    Visited = []

    # Parent Node Mapping
    Parents = np.zeros([10,10,2],dtype = int)


    while queue:   # If queue is not empty 

        Node = queue.pop(0)  # Pop first element in the queue
        global Iterations
        Iterations=Iterations+1
        if Node==Goal:   # Did we reach the goal?
            Flag = True
            break

        Neighbours = get_Neighbours(Node,Direction) # Get neighbours of this node

        for N in Neighbours: # For each neighbour of this node
            if not N in Visited and Map[N[0],N[1]]!=0:   # if this neighbour wasnt visited before and doesnt equal 0 (ie not an obstacle)
                queue.append(N)      # add to the queue
                Visited.append(N)     # add it to the visited
                Parents[N[0],N[1]] = Node  # add its parent node 

    if Flag == False:
        print('Mafesh path :(')

    if Flag == True:
        path = get_Path(Parents,Goal,Start) # this function returns the path to the goal 
        return path


def DFS(Map,Start,Goal,Direction):  # Direction for CCW -1  for CW 1

    Flag = False # Flag indicating if goal node is found
    
    # Initializing a q
    stack = []
    stack.append(Start)

    # Visited Nodes
    Visited = []
    Visited.append(Start)
    # Parent Node Mapping
    Parents = np.zeros([10,10,2],dtype = int)

    while stack:   # If queue is not empty 
        Node = stack.pop()  # Pop first element in the queue
        global Iterations
        Iterations=Iterations+1
        if Node==Goal:   # Did we reach the goal?
            Flag = True
            break

        Neighbours = get_Neighbours(Node,Direction) # Get neighbours of this node

        for N in Neighbours: # For each neighbour of this node
            if not N in Visited and Map[N[0],N[1]]!=0:   # if this neighbour wasnt visited before and doesnt equal 0 (ie not an obstacle)
                stack.append(N)       # add to the queue
                Visited.append(N)     # add it to the visited
                Parents[N[0],N[1]] = Node  # add its parent node 

    if Flag == False:
        print('Mafesh path :(')

    if Flag == True:
        path = get_Path(Parents,Goal,Start) # this function returns the path to the goal 
        return path
    

def get_Path(Parents,Goal,Start):

    path = []
    Node = Goal  # start backward 
    path.append(Goal)
   
    while not np.array_equal(Node, Start):

       path.append(Parents[Node[0],Node[1]])  # add the parent node 
       Node = Parents[Node[0],Node[1]]        # search for the parent of that node 
     
    path.reverse()
    return path

    

def get_Neighbours(Node,Direction):    # Returns neighbours of the parent node   Direction = 1 for Clockwise/ Direction = -1 for CCW 

    Neighbours = []
    
    if Direction==1:
        Neighbours.append([Node[0],Node[1]+1])
        Neighbours.append([Node[0]+1,Node[1]+1])
        Neighbours.append([Node[0]+1,Node[1]])
        Neighbours.append([Node[0]+1,Node[1]-1])
        Neighbours.append([Node[0],Node[1]-1])
        Neighbours.append([Node[0]-1,Node[1]-1])
        Neighbours.append([Node[0]-1,Node[1]])
        Neighbours.append([Node[0]-1,Node[1]+1])
                        
    if Direction==-1:
        Neighbours.append([Node[0],Node[1]+1])
        Neighbours.append([Node[0]-1,Node[1]+1])
        Neighbours.append([Node[0]-1,Node[1]])
        Neighbours.append([Node[0]-1,Node[1]-1])
        Neighbours.append([Node[0],Node[1]-1])
        Neighbours.append([Node[0]+1,Node[1]-1])
        Neighbours.append([Node[0]+1,Node[1]])
        Neighbours.append([Node[0]+1,Node[1]+1])

    return Neighbours

if __name__ == '__main__':     # Main function that is executed 

    Map = np.ones([10,10],dtype = int)    # Uses Numpy package to create a 7x7 map of ones 
    Draw(Map)   # Calls Drawing ID function
    for i in range(3):
        Map[i+1][4]=0
    for i in range(4):
        Map[i+5][2]=0
    for i in range(4):
        Map[5][i+5]=0
    start=[8,8]
    goal=[8,1]    
    print("Starting node is ",start,"goal is ",goal," with CW exploration starting East")
    print(Map)
    print("------------------")
    print("For BFS:")
    path = BFS(Map,start,goal,1) 
    print(path)
    print("the path generated is from ",len(path),"and after ",Iterations)
    Iterations=0    
    print("------------------")
    print("For DFS:")
    path = DFS(Map,start,goal,1) 
    print(path)
    print("the path generated is from ",len(path),"and after ",Iterations)
    print("------------------")
