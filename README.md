## User Guide
On the command line, type 'python pacmanSimulation.py' to run the program.
You will be prompted to input the number of ghosts, cherries, timesteps, choice of map, pacman eating cherry status and movement scheme.
After the input the program will begin to display the simulation as a plot every time interval.
Note: Simulation configured to run until end of timesteps/all cherries eaten regardless of Pacman being eaten by ghosts


## Synopsis
Coding a Maze Pathfinding Simulation using only matplotlib for visualising movement 

## Contents
README - readme file for Maze Pathfinding in the spirit of Pacman
pacmanSimulation.py - main file that contains code for reading in a map, plotting the characters/features and use of matplotlib to simulate pac-man like movement/interaction
characters.py - contains the super and sub class of characters
ghostGang.csv - csv file containing the attributes for the four ghosts
mazeLvl1Mini.csv - contains map size and coordinates that are obstacles
mazeLvl1Portals.csv - contains map size and coordinates that are obstacles

## Dependencies
matplotlib
random

## Version information
29/04/2022 - initial version with basic scripts for menu in main.py(now pacmanSimulation.py), classes and drafts of mazes
02/05/2022 - implemented basic movement for pacman under class attributes and tested against obstacles
03/05/2022 - tested cherry mechanic on pacman gaining invincibility and ghost response
04/05/2022 - added and tested the Moore neighbourhood scheme with base map. Added more mazes
07/05/2022 - initial testing of movement function using Breadth First Search Algorithm
09/05/2022 - BFS function works and is able to display shortest path during single timestep
10/05/2022 - implement a for loop to perform BFS function multiple times for both ghost gang and pacman as each timestep represents 1 move step
13/05/2022 - encountered many errors in looping bfs and used test.py to debug errors in isolation
16/05/2022 - created a list data structure to store path to cherry for pacman and a dynamic list data structure for ghost gang as pacman changes location every timestep
17/05/2022 - created more dynamic list structures to accomodate for ghosts running back to base whilst pacman is invincible and for pacman to chase ghosts
18/05/2022 - testing and identifying which ghosts to chase when pacman in invincible
19/05/2022 - added portals for both pacman and ghosts to demonstrate quickest pathfinding when you can exit and reenter the maze through the out of bounds portal
