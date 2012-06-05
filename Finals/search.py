"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8

def getGoalCoordinate(N = N):  
   if N%2 == 0:  
      return N-1 + (N/2 -1)*N  
   else:  
      return N-1 + (N-1)/2 *N

def execute_action(state,action):
    new_state = []
    acted_object = action[0]
    acted_place = action[1]
    for element in state:
        obj = element[0]
        locations = element[1]
        if obj == acted_object:
            new_state.append((obj,tuple((a+acted_place for a in locations))))
        else:
            new_state.append(element)
    return tuple(new_state)


def successors(state, N = N):
    result = {}
    actions = []
    all_ocupied = []
    for element in state:
        all_ocupied = all_ocupied + list(element[1])
    all_ocupied.sort()
    # para cada elemento
    for element in state:
        # se nao for o goal ou parede:
        if element[0] != '@' and element[0] != '|':
            car = element[0]
            locations = element[1]
            location_list = list(locations)
            location_list.sort()
            start = location_list[0]
            size = len(locations)
            # idetificar se esta na horizontal
            if location_list[0] + 1 == location_list[1]:
                # horizontal
                leftmost_obstacle = all_ocupied[all_ocupied.index(start)-1]
                rightmost_obstacle = all_ocupied[all_ocupied.index(start+size-1)+1]
                if leftmost_obstacle == getGoalCoordinate():
                    left = leftmost_obstacle + 1 - start - 1
                else:
                    left = leftmost_obstacle + 1 - start
                if rightmost_obstacle == getGoalCoordinate():
                    right = rightmost_obstacle - (start+size-1)
                else:
                    right = rightmost_obstacle - (start+size)
                if left != 0:
                    new_state = execute_action(state,(car,left))
                    result[new_state] = (car,left)
                if right != 0:
                    new_state = execute_action(state,(car,right))
                    result[new_state] = (car,right)
                #if car == '*':
                #    print left,right, leftmost_obstacle, rightmost_obstacle
                #    print 'ACHOU!'
            else:
                # vertical
                up = 0
                down = 0
                a = start
                add = True
                while add:
                    if a != start:
                        if a not in all_ocupied or a == getGoalCoordinate():
                            up += 1
                        else:
                            add = False
                    a = a - N
                b = start + (size-1)*N
                add = True
                while add:
                    if b != start + (size-1) * N:
                        if b not in all_ocupied or b == getGoalCoordinate():
                            down += 1
                        else:
                            add = False
                    b = b + N
                if up != 0:
                    new_state = execute_action(state,(car,-up*N))
                    result[new_state] = (car,-up*N)
                if down != 0:
                    new_state = execute_action(state,(car,down*N))
                    result[new_state] = (car,down*N)
    return result

def is_goal(state, N = N):
    for element in state:
        obj = element[0]
        if obj == '*':
            locations = element[1]
            if getGoalCoordinate(N) in locations: return True
            else: return False
    return False

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(start,successors,is_goal)
    
# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    locations = []
    for i in range(n):
        locations.append(start+i*incr)
    return tuple(locations)


def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    the_grid = []
    the_grid.append(('@',(getGoalCoordinate(N),)))
    for car in cars:
        the_grid.append(car)
    wall_locations = range(1,N-1) + range(N,N*N,N) + range(N-1,N*N,N) + range(N*(N-1)+1,N*N-1)
    wall_locations.remove(getGoalCoordinate(N))
    wall_locations = tuple(wall_locations)
    the_grid.append(('|',wall_locations))
    return tuple(the_grid)


def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))


puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))


print puzzle1
print puzzle2
print puzzle3


# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                #print path2
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

path = solve_parking_puzzle(puzzle1,N)
print path_actions(path)
path = solve_parking_puzzle(puzzle2,N)
print path_actions(path)
path = solve_parking_puzzle(puzzle3,N)
print path_actions(path)
