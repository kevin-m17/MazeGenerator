# import pygame
# import numpy
# import random
# pygame.init()

# done = False
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# BLUE = (0, 0, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)

# cols = 20
# rows = 20

# width = 700
# height = 700
# wr = width/cols
# hr = height/rows

# screen = pygame.display.set_mode([width, height])
# pygame.display.set_caption("Python Maze")
# clock = pygame.time.Clock()


# class Spot:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         # self.f = 0
#         # self.g = 0
#         # self.h = 0
#         self.visited = False
#         self.walls = [True, True, True, True]
#         self.neighbors = []

#     def draw(self, color = BLACK):
#         if self.walls[0]:
#             pygame.draw.line(screen, color, [self.x*hr, self.y*wr],       [self.x*hr+hr, self.y*wr], 1)
#         if self.walls[1]:
#             pygame.draw.line(screen, color, [self.x*hr+hr, self.y*wr],    [self.x*hr+hr, self.y*wr + wr], 1)
#         if self.walls[2]:
#             pygame.draw.line(screen, color, [self.x*hr+hr, self.y*wr+wr], [self.x*hr, self.y*wr+wr], 1)
#         if self.walls[3]:
#             pygame.draw.line(screen, color, [self.x*hr, self.y*wr+wr],    [self.x*hr, self.y*wr], 1)

#     def show_block(self, color):
#         if self.visited:
#             pygame.draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-2, wr-2])

#     def add_neighbors(self):
#         if self.x > 0:
#             self.neighbors.append(grid[self.x - 1][self.y])
#         if self.y > 0:
#             self.neighbors.append(grid[self.x][self.y - 1])
#         if self.x < rows - 1:
#             self.neighbors.append(grid[self.x + 1][self.y])
#         if self.y < cols - 1:
#             self.neighbors.append(grid[self.x][self.y + 1])


# grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

# for i in range(rows):
#     for j in range(cols):
#         grid[i][j].add_neighbors()

# current = grid[0][0]
# visited = [current]
# completed = False


# def breakwalls(a, b):
#     if a.y == b.y and a.x > b.x:
#         grid[b.x][b.y].walls[1] = False
#         grid[a.x][a.y].walls[3] = False
#     if a.y == b.y and a.x < b.x:
#         grid[a.x][a.y].walls[1] = False
#         grid[b.x][b.y].walls[3] = False
#     if a.x == b.x and a.y < b.y:
#         grid[b.x][b.y].walls[0] = False
#         grid[a.x][a.y].walls[2] = False
#     if a.x == b.x and a.y > b.y:
#         grid[a.x][a.y].walls[0] = False
#         grid[b.x][b.y].walls[2] = False


# while not done:
#     clock.tick(15)
#     screen.fill(BLACK)
#     if not completed:
#         grid[current.x][current.y].visited = True
#         got_new = False
#         temp = 10

#         while not got_new and not completed:
#             r = random.randint(0, len(current.neighbors)-1)
#             Tempcurrent = current.neighbors[r]
#             if not Tempcurrent.visited:
#                 visited.append(current)
#                 current = Tempcurrent
#                 got_new = True
#             if temp == 0:
#                 temp = 10
#                 if len(visited) == 0:
#                     completed = True
#                     break
#                 else:
#                     current = visited.pop()
#             temp = temp - 1

#         if not completed:
#             breakwalls(current, visited[len(visited)-1])

#         for i in range(rows):
#             for j in range(cols):
#                 grid[i][j].draw(WHITE)

#         current.visited = True
#         current.show_block(GREEN)
#         pygame.display.flip()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True

import pygame
import time
import random

# set up pygame window
WIDTH = 500
HEIGHT = 600
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()

# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = 20                   # width of cell
grid = []
visited = []
stack = []
solution = {}


# build the grid
def build_grid(x, y, w):
    for i in range(1,21):
        x = 20                                                            # set x coordinate to start position
        y = y + 20                                                        # start a new row
        for j in range(1, 21):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])           # top of cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   # right of cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   # bottom of cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           # left of cell
            grid.append((x,y))                                            # add cell to grid list
            x = x + 20                                                    # move cell to new position


def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x +  1, y + 1, 19, 39), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - w +1, y +1, 39, 19), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, 39, 19), 0)
    pygame.display.update()


def single_cell( x, y):
    pygame.draw.rect(screen, GREEN, (x +1, y +1, 18, 18), 0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, 18, 18), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                        # has visited cell


def solution_cell(x,y):
    pygame.draw.rect(screen, YELLOW, (x+8, y+8, 5, 5), 0)             # used to show the solution
    pygame.display.update()                                        # has visited cell


def carve_out_maze(x,y):
    single_cell(x, y)                                              # starting positing of maze
    stack.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        time.sleep(.07)                                            # slow program now a bit
        cell = []                                                  # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
            cell.append("right")                                   # if yes add to cell list

        if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:     # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:      # up cell available?
            cell.append("up")

        if len(cell) > 0:                                          # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly

            if cell_chosen == "right":                             # if this cell has been chosen
                push_right(x, y)                                   # call push_right function
                solution[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + w                                          # make this cell the current cell
                visited.append((x, y))                              # add to visited list
                stack.append((x, y))                                # place current cell on to stack

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            time.sleep(.05)                                       # slow program down a bit
            backtracking_cell(x, y)                               # change colour to green to identify backtracking path


def plot_route_back(x,y):
    solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (20,20):                                     # loop until cell position == start position
        x, y = solution[x, y]                                    # "key value" now becomes the new key
        solution_cell(x, y)                                      # animate route back
        time.sleep(.1)


x, y = 20, 20                     # starting position of grid
build_grid(40, 0, 20)             # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
carve_out_maze(x,y)               # call build the maze  function
plot_route_back(400, 400)         # call the plot solution function


# ##### pygame loop #######
running = True
while running:
    # # keep running at the at the right speed
    # clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False