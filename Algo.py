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