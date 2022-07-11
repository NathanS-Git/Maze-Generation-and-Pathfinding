import random

def generate_maze(size, seed=None):
    """ Random Depth-First Search Maze Generator 
    
    The maze is represented as a 2D matrix of values.
    0 - Empty space
    1 - Wall
    (Later we use 2 and 3 to represent the beginning and end in the A* algorithm)
    
    The maze starts out as a 2D matrix of pure 1's (walls), then two points are chosen and 
    the wall between them is removed to connect them visually.
    """

    random.seed(seed)

    assert size % 2 != 0, "Maze size must be odd"

    maze = [[1 for _ in range(size)] for _ in range(size)] # Representation of the maze, with walls in-between each node.
    x,y = random.randint(0,size//2),random.randint(0,size//2) # Choose a random starting point in half the defined space
    stack = [(x,y)]

    while stack:
        maze[x*2][y*2] = 0 # Mark current node as visited/active
        neighbours = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        unvisited_neighbours = []

        # Find all unvisited/unactive neighbours of current node
        for (nx,ny) in neighbours:
            try:
                if maze[nx*2][ny*2] == 1 and nx >= 0 and ny >= 0:
                    unvisited_neighbours.append((nx,ny))
            except IndexError: # Attempted to survey an out-of-bounds neighbour
                continue 
        
        if unvisited_neighbours: # If unvisited/unactivated neighbours exist, visit/activate a random one
            (i,j) = random.choice(unvisited_neighbours) # The neighbour we wish to connect to, from the current node
            maze[i*2][j*2] = 0 # Activate it
            maze[(x*2)+(i-x)][(y*2)+(j-y)] = 0 # Connect it visually (Remove the wall between the nodes)
            stack.append((i,j))
            x,y = i,j # Set as current node
        else: # Otherwise we've reached a dead end. Begin backtracking.
            x,y = stack.pop()

    return maze