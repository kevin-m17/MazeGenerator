
import pygame
import numpy
import random

# color and misc variables
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)

rows = 20
cols = 20
interval = 20
width = 400
height = 400


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.walls = [True, True, True, True] # north east south west
        self.visited = False

    def gridBuild(self, window):
        # assume x and y to be one unit intervals
        if self.walls[0]:
            pygame.draw.line(window, white, [self.x * interval, self.y * interval],[self.x * interval + interval, self.y * interval], 1)
        if self.walls[1]:
            pygame.draw.line(window, white, [self.x * interval + interval, self.y * interval],    [self.x * interval + interval, self.y * interval + interval], 1)
        if self.walls[2]:
            pygame.draw.line(window, white, [self.x * interval + interval, self.y * interval + interval], [self.x * interval, self.y * interval + interval], 1)
        if self.walls[3]:
            pygame.draw.line(window, white, [self.x * interval, self.y * interval + interval],    [self.x * interval, self.y * interval], 1)

    def addNeighbors(self, grid):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x <= rows - 2:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y <= cols - 2:
            self.neighbors.append(grid[self.x][self.y + 1])

def removewall(first, second, grid):
    # draw out
    if first.x == second.x and first.y < second.y:
        grid[first.x][first.y].walls[2] = False
        grid[second.x][second.y].walls[0] = False
    elif first.x == second.x and first.y > second.y:
        grid[first.x][first.y].walls[0] = False
        grid[second.x][second.y].walls[2] = False
    elif first.y == second.y and first.x > second.x:
        grid[first.x][first.y].walls[3] = False
        grid[second.x][second.y].walls[1] = False
    else:
        grid[first.x][first.y].walls[1] = False
        grid[second.x][second.y].walls[3] = False

def main(): 
    # define variables
    pygame.init()
    window = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Maze Generator with Recursive Backtracking")
    end = False
    grid = []

    grid = [[Square(i, j) for j in range(cols)] for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            grid[i][j].addNeighbors(grid)

    current = grid[0][0]
    visited = []
    visited.append(current)
    finished = False

    mazeSpeed = pygame.time.Clock() # need a clock variable
    pygame.time.wait(20000)

    # start of the backtracking
    while not end:
        mazeSpeed.tick(20)
        window.fill(black)
        if not finished:
            grid[current.x][current.y].visited = True
            notVisited = False
            num = 5

            while not notVisited and not finished:
                # random neighbor is chosen as the next square
                randomNeighbor = random.randint(0, len(current.neighbors)-1)
                currentSquare = current.neighbors[randomNeighbor]
                if not currentSquare.visited:
                    visited.append(current)
                    current = currentSquare
                    notVisited = True

                # ensures stack doesn't prematurely empty
                if num == 0:
                    num = 5
                    if len(visited) == 0:
                        finished = True
                        break
                    else:
                        current = visited.pop()
                num -= 1

            # remove the wall to make maze
            if not finished:
                removewall(current, visited[len(visited)-1], grid)

            # creates whole maze again
            for i in range(rows):
                for j in range(cols):
                    grid[i][j].gridBuild(window)

            # updated visited squares accordingly
            current.visited = True
            if current.visited:
                pygame.draw.rect(window, green, [current.x*interval, current.y*interval, interval, interval])
            pygame.display.update()

        # quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                completed = True

main()
    