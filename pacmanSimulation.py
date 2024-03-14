#
# Author : Gabe S
# 
#
# Revisions: 
#
# 29/04/2022 – Base version for assignment, creation of classes for characters
# 30/04/2022 - added function to read map layout, ghost attributes from csv file
# 01/05/2022 - added a method to lure ghosts towards pacman
# 03/05/2022 - added method for ghosts to runaway from pacman, method for pacman to move towards newly spawned cherry locations
## Refer to README for more revision updates

import random
import matplotlib.pyplot as plt
from characters import *

def read_map(choice):
    if choice == 1:
        fileobj = open('smallMap.csv', 'r')     # read coordinates from csv file
    elif choice == 2:
        fileobj = open('mazeLvl1Mini.csv', 'r')     # read coordinates from csv file
    elif choice == 3:
        fileobj = open('mazeLvl1Portals.csv', 'r')     # read coordinates from csv file    
    
    data = fileobj.readlines()
    fileobj.close()
    
    coordinatesList = []
    boundaries = data[0].split(',')         # first line in csv file is map size
    for line in data[1:]:                   # append x and y coordinates as tuple into a coordinates List
        # print(line)
        splitline = line.split(',')
        temp = (int(splitline[0]),int(splitline[1]))
        coordinatesList.append(temp)
        # xlist.append(int(splitline[0]))
        # ylist.append(int(splitline[1]))
    # print(coordinatesList)     
    
    return int(boundaries[0]), int(boundaries[1]), coordinatesList

def convert_to_xylist(tupleList):           # split tuple to separate variables
    xlist = []
    ylist = []
    for coordinates in tupleList:
        xlist.append(coordinates[0])
        ylist.append(coordinates[1])

    return xlist, ylist

def addPortalsVon(graph):                  # removing and replacing certain cell's neighbours to allow movement through portals
    graph[(9,14)].remove((9,15))
    graph[(9,14)].add((9,1))
    graph[(9,1)].remove((9,0))
    graph[(9,1)].add((9,14))
    graph[(1,7)].remove((0,7))
    graph[(1,7)].add((17,7))
    graph[(17,7)].remove((18,7))
    graph[(17,7)].add((1,7))
    return graph

def addPortalsMoore(graph):                  # removing and replacing certain cell's neighbours to allow movement through portals
    graph[(9,14)].remove((8,15))
    graph[(9,14)].remove((9,15))
    graph[(9,14)].remove((10,15))
    graph[(9,14)].add((9,1))
    graph[(9,1)].remove((8,0))
    graph[(9,1)].remove((9,0))
    graph[(9,1)].remove((10,0))
    graph[(9,1)].add((9,14))
    graph[(1,7)].remove((0,6))
    graph[(1,7)].remove((0,7))
    graph[(1,7)].remove((0,8))
    graph[(1,7)].add((17,7))
    graph[(17,7)].remove((18,6))
    graph[(17,7)].remove((18,7))
    graph[(17,7)].remove((18,8))
    graph[(17,7)].add((1,7))
    return graph

def read_ghosts(numGhosts):
    fileobj = open('ghostGang.csv', 'r')
    data = fileobj.readlines()
    fileobj.close()

    listOfGhosts = [] 
    for line in data[:numGhosts]:               # read in ghost details from csv and append them to list
        splitline = line.split(',')
        listOfGhosts.append(Ghost(splitline[0], splitline[1], int(splitline[2]), int(splitline[3])))
        # print(splitline[0], splitline[1], int(splitline[2]), int(splitline[3]))
    return listOfGhosts

def cherry_spawn_location(col, row, list, num):
    listOfCherries = []
    for _ in range(num):
        x = int(random.randint(2,col-1))
        y = int(random.randint(2,row-1))
        while (x,y) in list or (x,y) in listOfCherries:
            print('Cherry ', _, ' spawned on obstacle: ', (x,y))
            x = int(random.randint(2,col-1))
            y = int(random.randint(2,row-1))
        listOfCherries.append((x,y))
    print('cherry list: ', listOfCherries)     # print coordinates of all cherries
    return listOfCherries

def plot_ghost_scatter(ghosts):
    xlist = []
    ylist = []
    size = []
    colour = []
    for ghost in ghosts:
        if not ghost.eaten:
            xlist.append(ghost.getCol()) 
            ylist.append(ghost.getRow())
            size.append(500)
            colour.append(ghost.getColour())
    # print(len(ghost))
    plt.scatter(xlist,ylist,s=size,c=colour, marker='^')

def plot_maze_scatter(mazeList):
    xlist, ylist = convert_to_xylist(mazeList)              # break tuple to separate variables
    plt.scatter(xlist, ylist, s=300, marker='s', c="black")

def plot_cherry_scatter(cherry):
    plt.scatter(cherry[0], cherry[1], s=250, c="red", marker='*')

def get_coord(object):      # returns objects col and row as tuple
    return (object.getCol(), object.getRow())

def ghostMove(chaser, target):       # ghost movement indicated by pacman status
    status = target.invincible
    coord = get_coord(target)
    if status:
        chaser.runaway_moore(coord) # chaser away coordinates are updated
        print('RUN AWAY')
    else:
        chaser.lure_moore(coord)    # chaser closer coordinates are updated
        print('CHASE')

def ghostsInPlay(ghosts):
    for ghost in ghosts:
        if not ghost.eaten:
            return ghost

def status_check(target):
    if target.invincible:
        target.invincibility_duration -=1
        # print('Invincible: ', target.invincible, target.invincibility_duration)
        
    if target.invincibility_duration == 0:
        target.invincible = False
     

def create_graph_moore(cols, rows, list):
    graph = {}
    for col in range(1, cols+1):       # double for loop to access all coordinates within the map
        for row in range(1, rows+1):
            if (col,row) not in list:
                # print('col, row: ', (col,row)) 
                tempList=[(col-1,row+1),(col,row+1),(col+1,row+1),(col+1,row),(col+1,row-1),(col,row-1),(col-1,row-1),(col-1,row)]
                neighbourList = []
                for coord in tempList:      # checks if the adjacent coordinates are in the list
                    # print(tempList)
                    if coord not in list:
                        neighbourList.append(coord)
                # print(neighbourList)
                # print(set(neighbourList))
                graph[(col,row)] = set(neighbourList)
    return graph

def create_graph_von(cols, rows, list):
    graph = {}
    for col in range(1, cols+1):       # double for loop to access all coordinates within the map
        for row in range(1, rows+1):        
            if (col,row) not in list:
                tempList = [(col, row+1),(col+1,row),(col,row-1),(col-1,row)]
                neighborList = []
                for coord in tempList:      # checks if the adjacent coordinates are in the list
                    if coord not in list:
                        neighborList.append(coord) 
                graph[(col,row)] = set(neighborList)
    return graph

def bfs(graph, start_vertex, target_value):         # Bread First Search Function (learned to code this function from www.codecademy.com)
    path = [start_vertex]               # initial start of path is the first vertex
    vertex_and_path = [start_vertex, path]          # this list contains the start vertex and the path list 
    bfs_queue = [vertex_and_path]           # using a list to operate as a queue data structure
    visited = set()         # stores a set of vertices that have already been visited
    # count = 1
    while bfs_queue:        # while the queue is not empty loop through it
        current_vertex, path = bfs_queue.pop(0) # current vertex we are visiting and its' associated path is taken from the first position in the queue
        visited.add(current_vertex)     # add the current vertex to the visited set
        for neighbour in graph[current_vertex]:     # loop through each adjacent vertex of the current vertex
            if neighbour not in visited:        # clause to check if neighbor has not already been visited as we do not revisit past vertices
                if neighbour == target_value:       # comparison if adjacent vertex is our target vertex
                    return path + [neighbour]       # return the current path and the adjacent vertex which is our target
                else:
                    bfs_queue.append([neighbour, path + [neighbour]])       # continue searching by adding this adjacent vertex to the queue along with the path list with neighbour appended to it

def main():
    numGhosts = int
    while numGhosts not in [1,2,3,4]:
        numGhosts = int(input('Please input the number of ghosts to spawn in simulation from 1-4: '))        # number of ghost beings to chase pacman

    numCherries = int
    while numCherries not in [1,2,3,4]:
        numCherries = int(input('Please input the number of cherries to spawn on map from 1-4: '))     # number of cherries to spawn on map
    
    cherryIndex = 0     # initial assignment of index in the list of cherries
    
    timesteps = int(input('Please input how many timesteps you would like this simulation to run for: '))        # number of timesteps to run simulation

    mapChoice = int
    while mapChoice not in [1,2,3]:
        mapChoice = int(input('Select a map:\n1)No Obstacles\n2)Maze map\n3)Maze map with portals\n'))
    MAXCOLS, MAXROWS, obstacleList = read_map(mapChoice)      # read in map from csv file and store the coordinates of walls and boundaries
    
    eatChoice = int
    while eatChoice not in [1,2]:
        eatChoice = int(input('What does Pac-man do while he is invincible\n1)Eat Cherries\n2)Eat Ghosts\n'))

    ghostList = read_ghosts(numGhosts)
    cherryList = cherry_spawn_location(MAXCOLS, MAXROWS, obstacleList, numCherries)

    puckman = PacPerson("Pac-man", "yellow", random.randint(2, MAXCOLS-1), random.randint(2, MAXROWS-1))        # create pacman
    while (get_coord(puckman)) in obstacleList or get_coord(puckman) == cherryList[0] :     # if pacman initial spawn coords are an obstacle
        print('Pacman spawned on obstacle: ', get_coord(puckman))
        puckman.col = random.randint(2, MAXCOLS-1)                    # re-randomise his spawn coords
        puckman.row = random.randint(2, MAXROWS-1)                    # parameters 1 and MAX are the boundaries

    graphChoice = int
    while graphChoice not in [1,2]:
        graphChoice = int(input('Select a neighbourhood scheme:\n1)Von Neumann\n2)Moore\n'))
    if graphChoice == 1:
        theGraph = create_graph_von(MAXCOLS, MAXROWS, obstacleList)
    elif graphChoice == 2:
        theGraph = create_graph_moore(MAXCOLS, MAXROWS, obstacleList)
    
    if mapChoice == 3:
        if graphChoice == 1:
            theGraph = addPortalsVon(theGraph)
        elif graphChoice == 2:
            theGraph = addPortalsMoore(theGraph)
    
    for t in range(1, timesteps+1):     # every timestep the locations of all features are plotted       
        print("### Timestep ", t, "###")

        if get_coord(puckman) == cherryList[cherryIndex]:   # when pacman eats cherry
            print('Pacman ate cherry ', cherryIndex+1, ' at ', cherryList[cherryIndex])
            puckman.invincible = True                                     # becomes invincible
            puckman.invincibility_duration = 5                            # duration counter starts at constant number
            cherryIndex += 1                                              # next cherry index is selected
            if cherryIndex>=4:
                print('Pac-man has eaten all the cherries')
                break
            # bfsCherryPath = bfs(theGraph, cherryList[cherryIndex], get_coord(puckman)) # new path is created for new cherry
            # print('Pacman is invincible for ', puckman.invincibility_duration, 'timesteps')
            # if bfsCherryPath:
            #     puckman.move(bfsCherryPath.pop())                                                     
        elif puckman.invincible and ghostsInPlay(ghostList) != None and eatChoice == 2:
            bfsEatGhostPath = bfs(theGraph, get_coord(ghostsInPlay(ghostList)), get_coord(puckman))
            if bfsEatGhostPath:
                puckman.move(bfsEatGhostPath[:-1].pop())
            print('Pacman chasing ghosts')
        else:
            bfsCherryPath = bfs(theGraph, cherryList[cherryIndex], get_coord(puckman)) # new path is created for new cherry
            # print('The Path: ', bfsCherryPath)
            puckman.move(bfsCherryPath[:-1].pop())      # pacman coordinates are updated to the last element in the path list
            # puckman.lure_moore(currentCherry)
            print('Pacman chasing cherry')                                           
        # print('Pacman is at: ', get_coord(puckman))

        for ghost in ghostList:
            if puckman.invincible and not ghost.eaten:
                bfsGhostRunPath = bfs(theGraph, (9,6), get_coord(ghost))
                if bfsGhostRunPath:
                    ghost.move(bfsGhostRunPath[:-1].pop())
            elif not puckman.invincible and not ghost.eaten:
                bfsGhostChasePath = bfs(theGraph, get_coord(puckman), get_coord(ghost))
                if bfsGhostChasePath:
                    ghost.move(bfsGhostChasePath[:-1].pop())

            if get_coord(ghost) == get_coord(puckman):
                if not puckman.invincible:
                    puckman.eaten = True
                    print('Ghost has eaten ',puckman.getName())
                elif puckman.invincible:
                    ghost.eaten = True
                    print('Pac-man has eaten ghost ', ghost.getName())

            # print('Ghost Chase Path: ', bfsGhostChasePath)
            # print('Ghost is at: ', get_coord(ghost))

        status_check(puckman)       # currently checking pacman invincibility status

        plot_maze_scatter(obstacleList)         # plot the static maze
        plot_ghost_scatter(ghostList)       # plot dynamic location of ghosts
        plot_cherry_scatter(cherryList[cherryIndex])     # plot cherry location, new one appears after previous one gets eaten
        plt.scatter(puckman.getCol(), puckman.getRow(), s=500, c = puckman.getColour())     # plot dynamic location of pacman
        plt.xlim(0,MAXCOLS+1)    # display the grid
        plt.ylim(0,MAXROWS+1)    # in its actual size
        plt.pause(0.5)
        plt.clf()

        # if puckman.eaten:
        #     break

def test():
    # MAXCOLS, MAXROWS, obstacleList = read_map()      # read in map from csv file and store the coordinates of walls and boundaries
    # print(type(MAXCOLS), type(MAXROWS), type(obstacleList[0]))
    # testGraph = create_graph_von(MAXCOLS, MAXROWS, obstacleList)
    # testGraph = create_graph_moore(MAXCOLS, MAXROWS, obstacleList)
    # print(testGraph) # print the graph of all coordinates and adjacent ones that are not obstacles
    # # print(bfs(testGraph, (2,2), (4,4))) # print the path from start to target
    
    # some_hazardous_graph = {
    # 'lava': set(['sharks', 'piranhas']), 'sharks': set(['piranhas', 'bees']),
    # 'piranhas': set(['bees']), 'bees': set(['lasers']), 'lasers': set([])}
    # print(bfs(some_hazardous_graph, 'lava', 'lasers'))
    # print(dfs(some_hazardous_graph, 'lava', 'lasers'))
    
    # puckman = PacPerson("Pac-man", "yellow", random.randint(1, MAXCOLS), random.randint(1, MAXROWS))        # create pacman
    # puckmanCoords = (puckman.getCol(), puckman.getRow())
    # while (puckman.getCol(), puckman.getRow()) in obstacleList:     # if pacman initial spawn coords are an obstacle
    #     print('Spawned on obstacle: ', (puckman.getCol(), puckman.getRow()))
    #     puckman.col = random.randint(1, MAXCOLS)                    # re-randomise his spawn coords
    #     puckman.row = random.randint(1, MAXROWS)
    # print('Spawned: ', (puckman.getCol(), puckman.getRow()))

    # numCherries = 4    
    # cherryList = cherry_spawn_location(MAXROWS, MAXCOLS, obstacleList, numCherries)     # check if cherry spawn location is valid
    # print('cherryList: ', cherryList)

    ghostList = read_ghosts()
    for ghost in ghostList:
        ghost.eaten = True
    
    if (ghostsInPlay(ghostList)) == None:
        print('All ghosts have been eaten')

if __name__ == "__main__":
    main()
    # test()