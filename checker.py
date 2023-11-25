from z3 import *
from pprint import pprint as pp

n = 8
assert(n % 2 == 0)
# Removing one domino
num_dominoes = (n * n) // 2 - 1
# co-coordinates of the boxes to be removed
removed_boxes = [(0,0),(0,1)]

# List to hold the dominoes as dictionaries of coordinate pairs
dominoes = []

def manhattan_distance(x1, y1, x2, y2):
    return If(x1 > x2, x1 - x2, x2 - x1) + If(y1 > y2, y1 - y2, y2 - y1)

solver = Solver()
constraints = []

# Adding constraints for each domino
for _ in range(num_dominoes):
    # Define coordinates for each domino
    x1, y1, x2, y2 = Ints(f'{_}x1 {_}y1 {_}x2 {_}y2')

    # Constraint for the first box (x1, y1)
    box1 = And(0 <= x1, x1 < n, 0 <= y1, y1 < n)

    # Constraint for the second box (x2, y2)
    box2 = And(0 <= x2, x2 < n, 0 <= y2, y2 < n)

    # Constraint: length of the domino is 2 unit
    length = (manhattan_distance(x1, y1, x2, y2) == 1)

    # Adding domino coordinates to the list
    dominoes.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
    constraints += [box1, box2, length]
    # Adding constraints to the Z3 solver
    solver.add(box1, box2, length)


# Constraints to ensure distinct endpoints for each pair of dominoes
for i in range(num_dominoes):
    for j in range(i + 1, num_dominoes):
        overlap = And(
            manhattan_distance(dominoes[i]['x1'], dominoes[i]['y1'], dominoes[j]['x1'], dominoes[j]['y1']) >=1,
            manhattan_distance(dominoes[i]['x1'], dominoes[i]['y1'], dominoes[j]['x2'], dominoes[j]['y2']) >=1,
            manhattan_distance(dominoes[i]['x2'], dominoes[i]['y2'], dominoes[j]['x1'], dominoes[j]['y1']) >=1,
            manhattan_distance(dominoes[i]['x2'], dominoes[i]['y2'], dominoes[j]['x2'], dominoes[j]['y2']) >=1,
        )
        constraints += [overlap]
        solver.add(overlap)
    # Adding constraints to remove first horizontal two boxes
    box_removed = And(
        manhattan_distance(dominoes[i]['x1'], dominoes[i]['y1'], removed_boxes[0][0], removed_boxes[0][1]) >=1, # x1,y1 - 0 0
        manhattan_distance(dominoes[i]['x2'], dominoes[i]['y2'], removed_boxes[0][0], removed_boxes[0][1]) >=1, # x2,y2 - 0 0
        manhattan_distance(dominoes[i]['x1'], dominoes[i]['y1'], removed_boxes[1][0], removed_boxes[1][1]) >=1, # x1,y1 - 0 1
        manhattan_distance(dominoes[i]['x2'], dominoes[i]['y2'], removed_boxes[1][0], removed_boxes[1][1]) >=1, # x2,y2 - 0 1
    )
    constraints += [box_removed]
    solver.add(box_removed)

# pp(solver)
# pp(dominoes)

# Check satisfiability
grid = [['-' for i in range(n)] for j in range(n)]
# pp(grid)

# cannot_be_solved = Solver()
# cannot_be_solved.add(And(constraints) == False)

# print(f"Can be solved? : {cannot_be_solved.check()}")

if solver.check() == sat:
    model = solver.model()
    print("Solution found:")
    print(model.evaluate(And(constraints)))
    for (_, d) in enumerate(dominoes):
        (x1, y1, x2, y2) = (model[d['x1']].as_long(), model[d['y1']].as_long(), model[d['x2']].as_long(), model[d['y2']].as_long())
        print(f"{_}: {x1, y1}, {x2, y2}")
        grid[x1][y1] = chr(ord('a') + _)
        grid[x2][y2] = chr(ord('a') + _)
    for i in grid:
        print(''.join(i))
else:
    print("No solution found.")
