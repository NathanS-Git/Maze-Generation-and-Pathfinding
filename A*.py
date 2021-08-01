import numpy as np

def h(pos, goal): # Use euclidian distance as the heuristic
    return np.sqrt(np.power(pos[0]-goal[0],2)+np.power(pos[1]-goal[1],2))*10

def g(pos, start):
    return np.sqrt(np.power(pos[0]-start[0],2)+np.power(pos[1]-start[1],2))*10

def rebuild_path(cameFrom, goal):
    path = [goal]
    current = cameFrom[goal[0]][goal[1]]

    while current != 2:
        path.append(current)
        current = cameFrom[current[0]][current[1]]

    return path 

def Astar (maze, start=False, goal=False):
    for i in range(len(maze)): # Find start and goal positions, if not already given.
        for j in range(len(maze[i])):
            if maze[i][j] == 2:
                start = (i,j)
            elif maze[i][j] == 3:
                goal = (i,j)
            elif start and goal: # If we know where both are, we have all the info we need
                break
    
    if not (start and goal):
        print("No start and/or end goal found/given")
        return -1

    fScores = [row.copy() for row in maze]
    cameFrom = [row.copy() for row in maze]
    for i in range(len(fScores)):
        for j in range(len(fScores[i])):
            fScores[i][j] = float('inf') # Each pos 
    
    evaluating = [(start[0],start[1],0)]
    evaluated = []
    while evaluating:
        node = evaluating.pop(0)
        evaluated.append(node)
        
        if node[:2] == goal:
            return rebuild_path(cameFrom,goal)

        # Obtain neighbours of current node
        neighbours = [(node[0]+x,node[1]+y) for x in range(-1,2) for y in range(-1,2) if (x != 0 or y != 0) and (node[0]+x >= 0) and (node[1]+y >= 0)]

        try:
            for (i,j) in neighbours:
                n = (i,j)

                if (maze[i][j] == 1) or n in (e[:2] for e in evaluated):
                    continue
                
                if n not in (e[:2] for e in evaluating) or fScores[i][j]:
                    fCost = g(n,start)+h(n,goal)
                    if fCost < fScores[i][j]:
                        fScores[i][j] = fCost
                        cameFrom[i][j] = (node[0],node[1])
                    if n not in (e[:2] for e in evaluating):
                        evaluating.append((i,j,fCost))
                        evaluating.sort(key=lambda x: x[2])
        except IndexError:
            pass

    print("No path found")
    return -1 # No path to goal found

# 0 is air, 1 is wall, 2 is start, 3 is goal
if __name__=="__main__":
    temp = [[2,0,0,1,0,0],
            [0,0,0,1,0,0],
            [0,0,0,1,0,3],
            [0,0,0,1,0,0],
            [0,0,0,1,0,0],
            [0,0,0,0,0,0]] 

    print(Astar(temp))