"""

A* Path Finding Algorithm

"""
import copy
import math
import time
from collections import OrderedDict

def add(loc1, loc2):
    return [loc1[0] + loc2[0], loc1[1] + loc2[1]]


class Block:
    def __init__(self, loc):
        self.g = -1
        self.h = -1
        self.f = self.g + self.h
        self.loc = loc
        self.parent = -1
        self.visited = False
    def __str__(self):
        return str(str(self.loc) + " : " + str(self.g))


def dist(loc1, loc2):
    y2 = loc2[1]
    y1 = loc1[1]

    x2 = loc2[0]
    x1 = loc1[0]
    return (abs(y2-y1) + abs(x2-x1))
    # return math.sqrt(   (abs(y2 - y1)*abs(y2-y1) + abs(x2 - x1)*abs(x2-x1) ) )



def moves_list(current,head):
    i = current
    moves = []
    while i.loc != head:
        i.visited = True
        x_mov = i.loc[0] - i.parent.loc[0]
        y_mov = i.loc[1] - i.parent.loc[1]
        moves.append([x_mov, y_mov])
        i = i.parent
    moves.reverse()
    return moves

def move(head, goal, snake_blocks, boundaries, rows, cols, possible):

    grid = []
    print(len(snake_blocks))
    for i in range(cols + 4):
        c = []
        for j in range(rows + 4):
            c.append(Block([i, j]))
        grid.append(c)

    grid[head[0]][head[1]].g = 0
    grid[head[0]][head[1]].h = dist(head, goal)
    grid[head[0]][head[1]].f = 0 + dist(head, goal)
    grid[goal[0]][goal[1]].g = dist(head, goal)
    grid[goal[0]][goal[1]].h = 0
    grid[goal[0]][goal[1]].f = dist(head, goal) + 0

    open = [grid[head[0]][head[1]]]
    closed = []
    start = time.time()
    flag = True
    current = open[0]
    iterations = 0
    while True:
        if current.loc == goal:
            i = current
            moves = moves_list(current,head)
            return moves, True

        if len(open) == 0:
            #There is no path that leads to goal
            moves = []
            for i in closed:
                if not i.visited:
                    moves.append( moves_list(i,head) )

            sorted_list = list(sorted(moves, key=len))
            print("here")
            print( len(sorted_list[-1]) )
            return sorted_list[-1], False

        current = open[0]
        for i in open:
            f = i.g + i.h
            if f < current.f:
                current = i
            elif f == current.f:
                if i.h <= current.h:
                    current = i

        open.remove(current)
        closed.append(current)

        n1 = [current.loc[0] + 1, current.loc[1]]
        n2 = [current.loc[0] - 1, current.loc[1]]
        n3 = [current.loc[0], current.loc[1] + 1]
        n4 = [current.loc[0], current.loc[1] - 1]

        if n1[0] > cols or n1[1] > rows:
            n1 = -1
        if n2[0] > cols or n2[1] > rows:
            n2 = -1
        if n3[0] > cols or n3[1] > rows:
            n3 = -1
        if n4[0] > cols or n4[1] > rows:
            n4 = -1

        for i in boundaries:
            if i == n1:
                n1 = -1
            elif i == n2:
                n2 = -1
            elif i == n3:
                n3 = -1
            elif i == n4:
                n4 = -1

        ind = 0

        for i in snake_blocks:
            comp = current.g
            if i == n1:
                if len(snake_blocks) - ind > comp:
                    n1 = -1
            elif i == n2:
                if len(snake_blocks) - ind > comp:
                    n2 = -1
            elif i == n3:
                if len(snake_blocks) - ind > comp:
                    n3 = -1
            elif i == n4:
                if len(snake_blocks) - ind > comp:
                    n4 = -1
            ind += 1

        neighbors = []
        for i in [n1, n2, n3, n4]:
            if i != -1:
                b = grid[i[0]][i[1]]
                neighbors.append(b)

        for i in neighbors:
            if i in closed:
                continue

            if current.g + 1 < i.g or i not in open:
                i.g = current.g + 1
                i.h = dist(i.loc, goal)
                i.f = i.g + i.h
                i.parent = current
                if i not in open:
                    open.append(i)


def top_check(point1, point2, point3, point4, blocks, possible):
    # POINT1 has to be head
    # POINT2 has to be goal
    top = False
    for i in blocks:
        if i[0] >= point1[0] and i[0] <= point4[0]:
            if i[1] == point1[1]:
                top = True
                break
    if top:
        v1 = False
        v2 = False
        bottom = False
        for i in blocks:
            if i[0] >= point3[0] and i[0] <= point2[0]:
                if i[1] == point3[1]:
                    bottom = True
                    break
        if bottom:
            v1 = True

        left = False
        for i in blocks:
            if i[1] >= point1[1] and i[0] <= point3[1]:
                if i[0] == point1[0]:
                    left = True
                    break
        if left:
            v2 = True
        return v1, v2
    else:
        return False, False


def bottom_check(point1, point2, point3, point4, blocks, possible):
    bottom = False
    for i in blocks:
        if i[0] >= point3[0] and i[0] <= point2[0]:
            if i[1] == point3[1]:
                bottom = True
                break
    if bottom:
        v1 = False
        v2 = False
        top = False
        for i in blocks:
            if i[0] >= point1[0] and i[0] <= point4[0]:
                if i[1] == point1[1]:
                    top = True
                    break
        if top:
            v1 = True

        right = False
        for i in blocks:
            if i[1] >= point4[1] and i[0] <= point2[1]:
                if i[0] == point4[0]:
                    right = True
                    break
        if right:
            v2 = True
        return v1, v2
    else:
        return False, False


def top_left_blocked(snake, head, goal, blocks, possible):
    point1 = [head[0], head[1]]
    point2 = [goal[0], goal[1]]
    point3 = [head[0], goal[1]]
    point4 = [goal[0], head[1]]
    v1, v2 = top_check(point1, point2, point3, point4, blocks, possible)
    v3, v4 = bottom_check(point1, point2, point3, point4, blocks, possible)
    if v1 == True:
        try:
            possible.remove([1, 0])
        except:
            pass
    if v2 == True:
        try:
            possible.remove([1, 0])
            possible.remove([0, 1])
        except:
            pass
    return v1 or v2 or v3 or v4


def top_right_blocked(snake, head, goal, blocks, possible):
    point1 = [head[0], head[1]]
    point2 = [goal[0], goal[1]]
    point3 = [head[0], goal[1]]
    point4 = [goal[0], head[1]]
    v1, v2 = top_check(point4, point3, point2, point1, blocks, possible)
    v3, v4 = bottom_check(point4, point3, point2, point1, blocks, possible)
    if v1 == True:
        try:
            possible.remove([-1, 0])
        except:
            pass
    if v2 == True:
        try:
            possible.remove([-1, 0])
            possible.remove([0, 1])
        except:
            pass
    return v1 or v2 or v3 or v4


def bottom_left_blocked(snake, head, goal, blocks, possible):
    point1 = [head[0], head[1]]
    point2 = [goal[0], goal[1]]
    point3 = [head[0], goal[1]]
    point4 = [goal[0], head[1]]
    v1, v2 = top_check(point4, point3, point2, point1, blocks, possible)
    v3, v4 = bottom_check(point4, point3, point2, point1, blocks, possible)
    if v3 == True:
        try:
            possible.remove([1, 0])
        except:
            pass
    if v4 == True:
        try:
            possible.remove([1, 0])
            possible.remove([0, -1])
        except:
            pass
    return v1 or v2 or v3 or v4


def bottom_right_blocked(snake, head, goal, blocks, possible):
    point1 = [head[0], head[1]]
    point2 = [goal[0], goal[1]]
    point3 = [head[0], goal[1]]
    point4 = [goal[0], head[1]]
    v1, v2 = top_check(point1, point2, point3, point4, blocks, possible)
    v3, v4 = bottom_check(point1, point2, point3, point4, blocks, possible)
    if v3 == True:
        try:
            possible.remove([-1, 0])
        except:
            pass
    if v4 == True:
        try:
            possible.remove([-1, 0])
            possible.remove([0, -1])
        except:
            pass
    return v1 or v2 or v3 or v4


def safe_algo(snake, head, goal, blocks, possible):
    if head[0] >= goal[0]:
        # right
        if head[1] >= goal[1]:
            # bottom
            if bottom_right_blocked(snake, head, goal, blocks, possible):
                # pass
                try:
                    possible.remove([0, -1])
                    possible.remove([-1, 0])
                except:
                    pass
        else:
            # top
            if top_right_blocked(snake, head, goal, blocks, possible):
                # pass
                try:
                    possible.remove([0, 1])
                    possible.remove([-1, 0])
                except:
                    pass
    else:
        # left
        if head[1] >= goal[1]:
            # bottom
            if bottom_left_blocked(snake, head, goal, blocks, possible):
                # pass
                try:
                    possible.remove([0, -1])
                    possible.remove([1, 0])
                except:
                    pass
        else:
            # top
            if top_left_blocked(snake, head, goal, blocks, possible):
                # pass
                try:
                    possible.remove([0, 1])
                    possible.remove([1, 0])
                except:
                    pass
    print("possible: ")
    print(possible)
    return possible



def isInsideBox(loc, minx, maxx, miny, maxy):
    if minx <= loc[0] <= maxx:
        if miny <= loc[1] <= maxy:
            return True
        else:
            return False
    return False

def safe_algo_1(snake, head, goal, blocks, possible):
    last_possi = []
    for delta in possible:
        if not is_blockage(snake, head, goal, blocks, delta):
            return [delta]
        last_possi = delta

    return [last_possi]



def is_blockage(snake,head,goal,blocks, delta):
    curr = add(head,delta)
    corners = [[head[0], goal[1]],
               [goal[0], curr[1]],
               [curr[0], curr[1]],
               [goal[0], goal[1]]
              ]

    maxx = max([c[0] for c in corners])
    minx = min([c[0] for c in corners])
    maxy = max([c[1] for c in corners])
    miny = min([c[1] for c in corners])

    if maxx - minx == 0 or maxy - miny == 0:
        if maxx - minx == 0:
            for i in range(miny, maxy + 1):
                if snake.is_in_loc([minx, i]):
                    return True
        else:
            for i in range(minx, maxx + 1):
                if snake.is_in_loc([i, miny]):
                    return True
        return False

    min_reachedx = False
    max_reachedx = False

    min_reachedy = False
    max_reachedy = False

    for block in blocks:
        if isInsideBox(block, minx, maxx, miny, maxy):
            if block[0] == minx:
                min_reachedx = True

            if block[0] == maxx:
                max_reachedx = True

            if block[1] == miny:
                min_reachedy = True

            if block[1] == maxy:
                max_reachedy = True

    verdict = (min_reachedx and max_reachedx) or (min_reachedy and max_reachedy)
    # print(minx, miny, maxx, maxy, verdict)
    return verdict


def move_1(snake,head, goal, blocks, rows, cols, possible):

    sorted_p = sorted(possible, key= lambda x: dist(add(head,x),goal))
    last_possi = []
    for delta in sorted_p:
        if not is_blockage(snake,head,goal,blocks, delta):
            return [delta]
        last_possi = delta

    return [last_possi]
