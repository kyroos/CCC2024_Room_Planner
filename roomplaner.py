# 40th Classic CCC Room Planner
# Solution for level 4, 5, 6 and 7

import os
import time

level = "level6"  # Set level between 4 and 7

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
            return [(r, c) for r in range(r1, r2) for c in range(c1, c2)]
    else:
        # For Level 5 and 6, only exact matches of 'length' are filled
        if (height == 1 and width < length) or (width == 1 and height < length):
            return []

        if (height == 1 and width == length) or (width == 1 and height == length):
            return [(r, c) for r in range(r1, r2) for c in range(c1, c2)]

    key = (height, width, length)
    if key in memo:
        return [(r1 + row_offset, c1 + col_offset) for row_offset, col_offset in memo[key]]

    key_transposed = (width, height, length)
    if key_transposed in memo:
        return [(r1 + col_offset, c1 + row_offset) for row_offset, col_offset in memo[key_transposed]]

    best = []

    # Set a threshold to determine when to apply a greedy split for the room
    limit = length * 4 + 4

    if height > limit and width % 2 == 1:
        # If height is odd, split off the corresponding part
        best = solve(r1, c1, r1 + length, c2, length) + solve(r1 + length + 1, c1, r2, c2, length)

    elif width > limit and height % 2 == 1:
        # If width is odd, split off the corresponding part
        best = solve(r1, c1, r2, c1 + length, length) + solve(r1, c1 + length + 1, r2, c2, length)

    elif height > limit and width > limit:
        # If both the width and height are even, split spiral
        rl = r1 + length
        cu = c2 - length - 1
        rr = r2 - length - 1
        cd = c1 + length

        best = solve(r1, c1, rl, cu, length)
        best += solve(r1, cu + 1, rr, c2, length)
        best += solve(rr + 1, cd + 1, r2, c2, length)
        best += solve(rl + 1, c1, r2, cd, length)
        best += solve(rl + 1, cd + 1, rr, cu, length)
    else:
        # Try splitting horizontally at every possible row
        for split_row in range(r1 + 1, r2):
            upper_section = solve(r1, c1, split_row, c2, length)
            lower_section = solve(split_row + 1, c1, r2, c2, length)
            candidate = upper_section + lower_section
            if len(candidate) > len(best):
                best = candidate

        # Try splitting vertically at every possible column
        for split_col in range(c1 + 1, c2):
            left_section = solve(r1, c1, r2, split_col, length)
            right_section = solve(r1, split_col + 1, r2, c2, length)
            candidate = left_section + right_section
            if len(candidate) > len(best):
                best = candidate

        # Try splitting spiral at every possible position
        if width < 21 and height < 21:
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

                            if len(candidate) > len(best):
                                best = candidate

    # Memoize the result
    memo[key] = [(row - r1, col - c1) for row, col in best]
    return best


if __name__ == '__main__':

    start_time = time.time()

    leveldir = os.path.join(os.path.dirname(__file__), level + '\\')
    if not (os.path.exists(leveldir) and os.path.isdir(leveldir)):
        print(f"Input folder {leveldir} does not exist!")
        exit(-1)

    for file in os.listdir(leveldir):
        infile = leveldir + file

        if infile.endswith('.in'):
            with open(infile) as f:
                rooms = f.read().splitlines()

            outfile = infile[:-3] + '.out'
            print(f"run {file} ...")

            result = ""
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

                grid = [[(r, c) in occupied_positions for c in range(columns)] for r in range(rows)]
                result += '\n'.join(''.join("X" if cell else "." for cell in row) for row in grid) + '\n\n'

                if level == "level7":
                    assert len(occupied_positions) == goal
                else:
                    assert len(occupied_positions) // length == goal

            if result and len(result) > 0 and "example" not in outfile:
                with open(outfile, 'w') as f:
                    f.write(result)

    print(f"Elapsed time: {time.time() - start_time:.1f} seconds")
