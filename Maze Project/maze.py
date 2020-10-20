import pygame
import random

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
height = 400
width = 400
block = 20
stack = []
current = None


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.walls = [True, True, True, True] # north east south west
        self.visited = False

    def reveal(self):
        if self.walls[0]:
            pygame.draw.line(screen, white, [self.x, self.y]
                             , [self.x + block, self.y], 1)
        if self.walls[1]:
            pygame.draw.line(screen, white, [self.x + block, self.y]
                             , [self.x + block, self.y + block], 1)
        if self.walls[2]:
            pygame.draw.line(screen, white, [self.x + block, self.y + block]
                             , [self.x, self.y + block], 1)
        if self.walls[3]:
            pygame.draw.line(screen, white, [self.x, self.y + block]
                             , [self.x, self.y], 1)
        if self.visited:
            rect = pygame.Rect(self.x, self.y, block, block + block)
            pygame.draw.rect(screen, green, rect)


    def get_neighbor(self):
        xval = self.x
        yval = self.y

        if not Tile(xval, yval - block).visited and yval - block >= 0:
            self.neighbors.append(Tile(xval, yval - block))
        if not Tile(xval, yval + block).visited and yval + block <= width:
            self.neighbors.append(Tile(xval, yval + block))
        if not Tile(xval + block, yval).visited and xval + block <= height:
            self.neighbors.append(Tile(xval + block, yval))
        if not Tile(xval - block, yval).visited and xval - block >= 0:
            self.neighbors.append(Tile(xval + block, yval))

        print(current.neighbors)

        if not self.neighbors:
            return None

        return random.choice(self.neighbors)


    # remove wall and update visited
    def remove_wall(row, col, chosen):
        current = Tile(row, col)

        if len(current.neighbors) > 0:
            xvalue = current.x
            yvalue = current.y

            # which direction will the tracker go?
            if chosen == Tile(row, col-block):
                Tile(xvalue, yvalue).walls[0] = False
                Tile(xvalue, yvalue - block).walls[2] = False
            elif chosen == Tile(row, col+block):
                Tile(xvalue, yvalue).walls[2] = False
                Tile(xvalue, yvalue + block).walls[0] = False
            elif chosen == Tile(row + block, col):
                Tile(xvalue, yvalue).walls[1] = False
                Tile(xvalue + block, yvalue).walls[3] = False
            else:
                Tile(xvalue, yvalue).walls[3] = False
                Tile(xvalue - block, yvalue).walls[1] = False
        else:
            current = stack.pop()

def index(x, y):
    return y + x * block

def main():
    global screen
    global grid
    grid = []
    pygame.init()
    screen = pygame.display.set_mode((height, width))
    screen.fill(black)
    quit = False

    for y_value in range(0, height, block):
        for x_value in range(0, width, block):
            grid.append(Tile(x_value, y_value))


    # first step - left corner is first tile
    current = grid[0]

    while not quit:
        # draw out the whole grid again
        for i in range(len(grid)):
            grid[i].reveal()

        # step 1: the current tile should be marked visited and pushed in stack
        current.visited = True
        stack.append(current)

        next = get_neighbor(current.x, current.y)

        if next is not None:
            # wall is removed
            remove_wall(current.x, current.y, next)

            # mark next as visited and make current cell the next
            next.visited = True
            current = next

        elif len(stack) > 0:
            current = stack.pop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
        pygame.display.update()

    pygame.quit()

main()






