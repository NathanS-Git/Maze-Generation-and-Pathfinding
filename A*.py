import numpy as np
import pygame as pg
from randdfs import generate_maze


def h_euclid(pos, goal): # Use euclidean distance as the heuristic
    return np.sqrt(np.power(pos[0]-goal[0],2)+np.power(pos[1]-goal[1],2))

def d_euclid(pos1, pos2):
    return np.sqrt(np.power(pos1[0]-pos2[0],2)+np.power(pos1[1]-pos2[1],2))


def h_manhattan(pos, goal): # Use manhattan distance as heuristic
    return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])

def d_manhattan(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])


def rebuild_path(came_from, goal, start):
    path = [goal] # Start on goal
    current = came_from[goal[0]][goal[1]]

    while current != start: # While we are not on the start, traverse backwards.
        path.append(current)
        current = came_from[current[0]][current[1]]
    
    path.append(start)

    return path


def Astar (maze: list, start: tuple = False, goal: tuple = False) -> list:
    
    if not (start and goal):
        for i in range(len(maze)): # Find start and goal positions, if not already given.
            for j in range(len(maze[i])):
                if maze[i][j] == 2:
                    start = (i,j)
                elif maze[i][j] == 3:
                    goal = (i,j)
                elif start and goal: # If we know where both are, we have all the info we need
                    break
            if start and goal:
                break
    
    if not (start and goal):
        print("No start and/or end goal found/given")

    f_scores = [row.copy() for row in maze] # Map of f_scores per position
    g_scores = [row.copy() for row in maze] # Map of g_scores per position 
    came_from = [row.copy() for row in maze] # Map of optimal neighbour per position

    for i in range(len(f_scores)): # Initialize f_scores and g_scores map
        for j in range(len(f_scores[i])):
            f_scores[i][j] = float('inf')
            g_scores[i][j] = float('inf')
            if (i,j) == start:
                g_scores[i][j] = 0
                f_scores[i][j] = h_manhattan(start, goal)

    evaluating = [start+(0,)] # Put the starting position as the first node to be evaluated

    print("Solving...")
    while evaluating:
        node = evaluating.pop(0)
        x,y = node[:2] # Position of node
 
        if (x,y) == goal: # If current node is the goal
            # Path found
            print("Solved!")
            return rebuild_path(came_from,goal,start)

        # Obtain (euclidean) neighbours of current node
        # neighbours = [(x+dx,y+dy) for dx in range(-1,2) for dy in range(-1,2) if (dx != 0 or dy != 0) and (x+dx >= 0) and (y+dy >= 0)]
        
        # Obtain (manhattan) neighbours of current node
        neighbours = [(x+dx,y+dy) for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)] if (x+dx >= 0) and (y+dy >= 0)]

        for (i,j) in neighbours:
            n = (i,j) # Neighbour position
            try:
                # If it is a wall don't attempt to evaluate it
                if (maze[i][j] == 1):
                    continue
                
                # Otherwise... evaluate
                # Combine g_score of current node and distance to neighbour
                tentative_score = g_scores[x][y] + d_euclid(n, node[:2])

                if tentative_score < g_scores[i][j]: # New best g_score for this neighbour
                    g_scores[i][j] = tentative_score 
                    f_scores[i][j] = tentative_score + h_euclid((i,j), goal)
                    came_from[i][j] = (x,y) # Set neighbours optimal neighbour to be the current node
                
                    if n not in (e[:2] for e in evaluating): # If this is a new unique node
                        evaluating.append((i,j,f_scores[i][j])) # Add node to evaluation list
                        evaluating.sort(key=lambda s: s[2]) # Put least-f_score node first in list

            except IndexError: # If we're examining a neighbour outside of bounds
                pass

    print("No path found")
    
    return -1


if (__name__=="__main__"):
    pg.init()
    screen_size = 1003
    screen = pg.display.set_mode((screen_size, screen_size))

    maze_size = 1001
    
    maze = generate_maze(maze_size,5)
    
    maze_display = pg.Surface((maze_size,maze_size))
    maze_display.fill((0,0,0))

    # Draw walls and empty space
    for i in range(maze_size):
        for j in range(maze_size):
            if maze[i][j] == 1:
                maze_display.set_at((j,i),(0,0,0))
            else:
                maze_display.set_at((j,i), (255,255,255))
    
    # Get solution
    solution = Astar(maze,(0,0),(maze_size-1,maze_size-1))

    # If solution failed
    if isinstance(solution, int):
        quit()

    # Draw solution to screen
    for location in solution:
        maze_display.set_at(location[::-1], (150,150,255))

    # Draw start and end points to screen
    maze_display.set_at(solution[-1][::-1], (255,0,0))
    maze_display.set_at(solution[0][::-1], (0,255,0))

    scale = screen_size//(maze_size+2)

    screen.fill((0,0,0))
    screen.blit(pg.transform.scale(maze_display, (screen_size-scale*2,screen_size-scale*2)), (scale,scale) )
    pg.display.update()
    #pg.image.save(pg.display.get_surface(), "Temp.png")