# 40th Classic CCC Room Planner
# Solution for level 4, 5, 6 and 7

import os
import sys
import time

level = "level6"  # Set level between 4 and 7

logging = False
logging_memoize = False
logging_time = False

animation_speed = 25  # Time in milliseconds (0ms for no animation, 25ms for animation) - Start in Console (!)
emoji_desk = "🟦"    # "X"
emoji_split = "🟨"   # "~"
emoji_empty = "🟫"   # "."

memo = dict()


def solve(r1, c1, r2, c2, length):
    """
    Recursively solves for the maximum number of desks that can be placed in a given rectangular room

    Parameters:
    - r1, c1: Top-left corner coordinates of the room
    - r2, c2: Bottom-right corner coordinates (exclusive) of the room
    - length: The required length of each desk

    Returns:
    - A list of tuples representing the positions of desks placed within the room
    """

    width = c2 - c1
    height = r2 - r1

    if height <= 0 or width <= 0:
        # If the rectangle has no area, return empty list
        return []

    if level == "level7":
        # For Level 7, any row or column of length up to '7' can be filled
        if (height == 1 and width <= length) or (width == 1 and height <= length):
            return [(r, c, "desk") for r in range(r1, r2) for c in range(c1, c2)]
    else:
        # For Level 5 and 6, only exact matches of 'length' are filled
        if (height == 1 and width < length) or (width == 1 and height < length):
            return []

        if (height == 1 and width == length) or (width == 1 and height == length):
            return [(r, c, "desk") for r in range(r1, r2) for c in range(c1, c2)]

    key = (height, width, length)
    if key in memo:
        return [(r1 + row_offset, c1 + col_offset, typ) for row_offset, col_offset, typ in memo[key]]

    key_transposed = (width, height, length)
    if key_transposed in memo:
        return [(r1 + col_offset, c1 + row_offset, typ) for row_offset, col_offset, typ in memo[key_transposed]]

    best = []

    # Set a threshold to determine when to apply a greedy split for the room
    limit = length * 4 + 4

    if height > limit and width % 2 == 1:
        # If height is odd, split off the corresponding part
        best = [(r1 + length, c, "split") for c in range(c1, c2)]
        best += solve(r1, c1, r1 + length, c2, length) + solve(r1 + length + 1, c1, r2, c2, length)

    elif width > limit and height % 2 == 1:
        # If width is odd, split off the corresponding part
        best = [(r, c1 + length, "split") for r in range(r1, r2)]
        best += solve(r1, c1, r2, c1 + length, length) + solve(r1, c1 + length + 1, r2, c2, length)

    elif height > limit and width > limit:
        # If both the width and height are even, split spiral
        rl = r1 + length
        cu = c2 - length - 1
        rr = r2 - length - 1
        cd = c1 + length

        best = (
                [(rl, c, "split") for c in range(c1, cu + 1)] +
                [(rr, c, "split") for c in range(cd, c2)] +
                [(r, cu, "split") for r in range(r1, rr + 1)] +
                [(r, cd, "split") for r in range(rl, r2)])
        best += solve(r1, c1, rl, cu, length)
        best += solve(r1, cu + 1, rr, c2, length)
        best += solve(rr + 1, cd + 1, r2, c2, length)
        best += solve(rl + 1, c1, r2, cd, length)
        best += solve(rl + 1, cd + 1, rr, cu, length)
    else:
        # Splitting horizontally at every possible row

        # ........... 2 Horizontal Split
        # ...........
        # ..upper....
        # ....section.
        # ...........
        # ...........
        # @@@@@@@@@@@ split_row
        # ...........
        # ...........
        # ..lower....
        # ...section.
        # ...........
        # ...........

        for split_row in range(r1 + 1, r2):
            upper_section = solve(r1, c1, split_row, c2, length)
            lower_section = solve(split_row + 1, c1, r2, c2, length)
            candidate = upper_section + lower_section
            if count_desks(candidate) > count_desks(best):
                best = [(split_row, c, "split") for c in range(c1, c2)] + candidate

        # Splitting vertically at every possible column

        #    split_col
        # ......@........... 2 Vertical Split
        # ......@...........
        # ......@...........
        # ......@...........
        # ......@...........
        # .left.@...right...
        # .sec-.@...section.
        # ..tion@...........
        # ......@...........
        # ......@...........
        # ......@...........
        # ......@...........
        # ......@...........

        for split_col in range(c1 + 1, c2):
            left_section = solve(r1, c1, r2, split_col, length)
            right_section = solve(r1, split_col + 1, r2, c2, length)
            candidate = left_section + right_section
            if count_desks(candidate) > count_desks(best):
                best = [(r, split_col, "split") for r in range(r1, r2)] + candidate

        # Try splitting spiral at every possible position

        #     r1/c1      r1/cu r1/c2
        #       ...........@...... 5 Spiral Split
        #       ...........@......
        #       ...(1).....@..(2).
        #       ...........@......
        #       ...........@......
        # left  ...........@......
        # rl/c1 @@@@@@@@@@@@......
        #       ......@....@......
        #       ......@....@......
        #       ......@....@......
        #       ......@....@......
        #       ......@(5).@......
        #       ......@....@......
        #       ..(4).@....@......
        #       ......@....@...... right
        #       ......@@@@@@@@@@@@ rr/c2
        #       ......@...........
        #       ......@...........
        #       ......@.....(3)...
        #       ......@...........
        #       ......@...........
        #       ......@...........
        #     r2/c1 r2/cd      r2/c2

        limit = 21  # Attempt spiral split only for small rectangles
        if width < limit and height < limit:
            for rl in range(r1, r2):
                for cu in range(c1, c2):
                    for rr in range(rl + 1, r2):
                        for cd in range(c1, cu):

                            # Divide the room into 5 sections in a spiral pattern
                            section1 = solve(r1, c1, rl, cu, length)
                            section2 = solve(r1, cu + 1, rr, c2, length)
                            section3 = solve(rr + 1, cd + 1, r2, c2, length)
                            section4 = solve(rl + 1, c1, r2, cd, length)
                            section5 = solve(rl + 1, cd + 1, rr, cu, length)
                            candidate = section1 + section2 + section3 + section4 + section5

                            if count_desks(candidate) > count_desks(best):
                                best = (
                                        [(rl, c, "split") for c in range(c1, cu + 1)] +
                                        [(rr, c, "split") for c in range(cd, c2)] +
                                        [(r, cu, "split") for r in range(r1, rr + 1)] +
                                        [(r, cd, "split") for r in range(rl, r2)])
                                best += candidate

    # Memoize the result
    memo[key] = [(row - r1, col - c1, typ) for row, col, typ in best]
    if logging_memoize:
        print(f"## Memoize {height}x{width}-{length}")
        print_grid(construct_grid(width, height, memo[key]))

    return best


def count_desks(candidate):
    return sum(1 for _, _, typ in candidate if typ == 'desk')


def solve_file(my_input, level):
    result = ""
    rooms = my_input.splitlines()
    N = rooms.pop(0)

    for room in rooms:
        room = list(map(int, room.split()))
        if level == "level4":
            length = 3
            columns, rows, goal = room
        if level == "level5":
            length = 2
            columns, rows, goal = room
        if level == "level6":
            columns, rows, goal, length = room
        if level == "level7":
            length = 7
            columns, rows, goal = room

        occupied_positions = solve(0, 0, rows, columns, length)

        grid = construct_grid(columns, rows, occupied_positions)
        result += '\n'.join(''.join("X" if cell == "desk" else "." for cell in row) for row in grid) + '\n\n'

        if logging:
            print(f"Solve {level} room size: {columns}x{rows} desk length: {length}")
            print_grid(grid)

        if animation_speed > 0 and rows <= 40 and columns <= 40:
            os.system('cls' if os.name == 'nt' else 'clear')
            for pos in range(len(occupied_positions)):
                r, c, typ = occupied_positions[pos]
                if typ == "desk":
                    print(f"Solve {level} room size: {columns}x{rows} desk length: {length}\n", flush=False)
                    grid = construct_grid(columns, rows, occupied_positions[:pos + 1])
                    print_grid(grid)
                    if level == "level7":
                        print(f"placed {count_desks(occupied_positions[:pos + 1])} cells")
                    else:
                        print(f"placed {count_desks(occupied_positions[:pos + 1]) // length} desks")
                    sys.stdout.write(f"\033[{rows + 4}A")  # Move cursor up
                    sys.stdout.flush()
                    time.sleep(animation_speed / 1_000)
            sys.stdout.flush()
            time.sleep(animation_speed / 50)

            if level == "level7":
                assert count_desks(occupied_positions) == goal
            else:
                assert count_desks(occupied_positions) // length == goal

    return result[:-1]


def print_grid(grid):
    for row in grid:
        line = ""
        for typ in row:
            line += emoji_desk if typ == "desk" else emoji_split if typ == "split" else emoji_empty
        print(line, flush=False)
    print()


def construct_grid(C, R, occupied_positions):
    grid = [['' for _ in range(C)] for _ in range(R)]
    for r, c, typ in occupied_positions:
        grid[r][c] = typ
    return grid


if __name__ == '__main__':

    start_time = time.time()

    leveldir = os.path.join(os.path.dirname(__file__), level + '\\')
    if not (os.path.exists(leveldir) and os.path.isdir(leveldir)):
        print(f"Input folder {leveldir} does not exist!")
        exit(-1)

    os.system('cls' if os.name == 'nt' else 'clear')
    print('-' * 80)
    print(f"{'Roomplaner ' + level:^80}")
    print('-' * 80)
    print()

    for file in os.listdir(leveldir):
        infile = leveldir + file

        if infile.endswith('.in'):

            with open(infile) as f:
                content = f.read()

            outfile = infile[:-3] + '.out'

            result = solve_file(content, level)

            if result and len(result) > 0 and "example" not in outfile:
                with open(outfile, 'w') as f:
                    f.write(result)

    if logging_time:
        print(f"Elapsed time: {time.time() - start_time:.1f} seconds")
    time.sleep(5)
