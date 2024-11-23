# Room Planner - solution for level 4, 5, 6 and 7

### What's the Challenge?
Imagine you have a big, empty rectangular room and a bunch of different-sized desks. These desks can be long, ranging from 1×2 to 1×7 blocks. Your mission is to place as many desks as you can in the room, but there’s a rule: no two desks can be next to each other, not even at the corners. The Room Planner puzzle is a great way to boost your problem-solving skills.

### Curious about how the algorithm works? Watch this video!
[See how the algorithm works – watch now!](https://www.youtube.com/watch?v=_699KQQofv8)


### I) Breaking It Down - Recursive Thinking using divide and conquer

Learn how to tackle big problems by splitting them into smaller, easier pieces.

> The key idea is to focus not on placing desks directly but on splitting the room into smaller sections until each is small enough to accommodate a desk. Splitting is performed horizontally (2-way split), vertically (2-way split), and spirally (5-way split).


```python
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

```

Base Case for Level 4,5 and 6

```python
    # Resolving the Base Case for Level 4,5 and 6
if (height == 1 and width < length) or (width == 1 and height < length):
    # The room is too small, no desk can be placed
    return []

if (height == 1 and width == length) or (width == 1 and height == length):
    return [(r, c) for r in range(r1, r2) for c in range(c1, c2)]
```

Base Case for Level 7

```python

# Resolving the Base Case for Level 7
if (height == 1 and width <= length) or (width == 1 and height <= length):
    return [(r, c) for r in range(r1, r2) for c in range(c1, c2)]

```

```python

best = []

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
    if len(candidate) > len(best):
        best = candidate

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
    if len(candidate) > len(best):
        best = candidate

# Split spiral at every possible position

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

return best
```

That's it! Realy, the algorithm is complete. Now it's all about improving the runtime to make it faster. Right now, it’s far too slow, and we need to push its performance to the next level! Let’s get started. Look, it’s easy!


### II) Smart Memory - Dynamic Programming using memoization

Find out how to remember the answers to little problems so you don’t have to solve them again. Memoization improves performance by storing and reusing results of expensive calculations, avoiding redundant work. It’s ideal for problems with overlapping subproblems, speeding up recursive algorithms and optimizing efficiency in tasks requiring fast results. Let’s dive in and see how to implement memoization!

```python

memo = dict()

def solve(r1, c1, r2, c2, length):

    width = c2 - c1
    height = r2 - r1

    key = (height, width, length)
    if key in memo:
        return [(r1 + row_offset, c1 + col_offset) for row_offset, col_offset in memo[key]]

    <...>

    # Memoize the result
    memo[key] = [(row - r1, col - c1) for row, col in best]

    return best
```

### III) Knowing When to Switch Gears - How to deal with big rooms using Thresholds

We fixed the problem for small rooms, but big rooms are still a challenge. We need a new idea here. Let’s think and make it happen! Before placing desks, make the area smaller and easier to handle. No need for exact splits—just use the longest length.

If either the width or length is odd, split off the corresponding side

```python
    # Set a threshold to determine when to apply a greedy split for the room
limit = length * 4 + 4

if height > limit and width % 2 == 1:
    best = solve(r1, c1, r1 + length, c2, length) + solve(r1 + length + 1, c1, r2, c2, length)
elif width > limit and height % 2 == 1:
    best = solve(r1, c1, r2, c1 + length, length) + solve(r1, c1 + length + 1, r2, c2, length)
```

If both the width and length are even, extract one spiral. Why does it matter if it's even or odd? Think about it—you’ll figure it out!

```python
    elif height > limit and width > limit:
rl = r1 + length
cu = c2 - length - 1
rr = r2 - length - 1
cd = c1 + length

best = solve(r1, c1, rl, cu, length)
best += solve(r1, cu + 1, rr, c2, length)
best += solve(rr + 1, cd + 1, r2, c2, length)
best += solve(rl + 1, c1, r2, cd, length)
best += solve(rl + 1, cd + 1, rr, cu, length)
```

> The total runtime for all five input files across Levels 4 to 7 is under one minute in Python

By mastering these techniques, you'll be equipped to tackle a wide range of programming challenges more effectively.


### Examples of scenarios where the Spiral approach outperforms the Horizontal or Vertical approach

#### Memo Spiral 4x4-2
```python
XX.X
...X
X...
X.XX
```

#### Memo Spiral 6x6-2
```python
X.X.XX
X.X...
....XX
XX....
...X.X
XX.X.X
```

#### Memo Spiral 8x8-4
```python
XXXX.X.X
.....X.X
XXXX.X.X
.....X.X
X.X.....
X.X.XXXX
X.X.....
X.X.XXXX
```

#### Memo Spiral 13x12-4
```python
XXXX.X.X.X.X
.....X.X.X.X
XXXX.X.X.X.X
.....X.X.X.X
X.X.........
X.X.XXXX.X.X
X.X......X.X
X.X.XXXX.X.X
.........X.X
X.X.X.X.....
X.X.X.X.XXXX
X.X.X.X.....
X.X.X.X.XXXX
```

#### Memo Spiral 12x8-6
```python
XXXXXX.X
.......X
XXXXXX.X
.......X
XXXXXX.X
.......X
X.......
X.XXXXXX
X.......
X.XXXXXX
X.......
X.XXXXXX
```

#### Memo Spiral 18x17-6
```python
XXXXXX.XXXXXX.X.X
..............X.X
XXXXXX.XXXXXX.X.X
..............X.X
XXXXXX.XXXXXX.X.X
..............X.X
XXXXXX.X.X.......
.......X.X.XXXXXX
XXXXXX.X.X.......
.......X.X.XXXXXX
XXXXXX.X.X.......
.......X.X.XXXXXX
X.X..............
X.X.XXXXXX.XXXXXX
X.X..............
X.X.XXXXXX.XXXXXX
X.X..............
X.X.XXXXXX.XXXXXX
```
