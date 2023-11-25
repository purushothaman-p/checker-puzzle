---

### Script Functionality: Domino Placement Puzzle Solver

#### Overview:
This script tries to solve the [domino placement puzzle](https://www.linkedin.com/posts/kenneth-roe-7ba4303_while-im-looking-for-work-ive-decided-activity-7131384927689838592-TJYi?utm_source=share&utm_medium=member_desktop) by using Z3-python solver to find valid configurations of dominoes. The puzzle involves placing a set of dominoes (rectangular tiles) on a grid with specified constraints.

#### Details:
- The grid size (`n x n`) and the number of dominoes (`num_dominoes`) are defined initially.
- Two boxes on the grid are specified to be removed, whose co-ordinates are represented by `removed_boxes`.
- The script creates dominoes represented as dictionaries, each containing coordinates `x1, y1, x2, y2` for the two ends of the domino.
- Constraints are imposed on each domino placement:
    - Each domino must have valid coordinates within the grid (`0 <= x < n`, `0 <= y < n`).
    - Each domino's length should be 2 units (Manhattan distance between its ends should be 1).
    - No two dominoes should overlap:
        - Distinct endpoints for each pair of dominoes should have a minimum Manhattan distance of 1.
    - Boxes to be removed cannot contain dominoes.

#### Execution:
- The Z3 solver checks for a solution satisfying all imposed constraints.
- If a solution exists (`solver.check() == sat`), it prints the coordinates of the placed dominoes on the grid.
- Each domino is represented by a letter ('a', 'b', 'c', etc.) and its endpoints are displayed.
- The solved grid with placed dominoes is printed with their respective identifiers.

### Observations:
- The script is able to prove that a solution exists for trivial examples with grid sizes of 2x2, 4x4 - i.e. when the removed boxes are adjacent. 
- It struggles to prove the existence/non-existence of a solution either if, 
    - the grid size is larger than 4x4, or
    - the removed boxes are non-adjacent (even for a 4x4 grid)

Suggestions/modifications to improve the performance of the code is highly welcome. 
---
