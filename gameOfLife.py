import sys
import pygame
import random

# Conways Game of Life!
#
# The game is a cellular automaton model:
#   A cellular automaton is a series of cells that follows basic rules to create 
# emergent behaviour.
# The rules are:
#   1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
#   2. Any live cell with two or three live neighbours lives on to the next generation.
#   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
#   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by
#   reproduction.
#
# Future improvements:
# 1. Make it interactable - Draw your own patterns before letting it run
# 2. Performance upgrade - Only check live cells and dead cells near live cells
#    - The dead cells only change state if they are near live cells, so dont ceck them
#      unless they are

pygame.init()
pygame.display.set_caption("Conways Game of Life")

# Frame rate
FPS = 12
clock = pygame.time.Clock()

# Window size
size = width, height = 1200, 800
res = 10
rows = int(height/res)
cols = int(width/res)

# Initialize screen
screen = pygame.display.set_mode(size)

# Colours
black = 0, 0, 0
white = 255, 255, 255


# Main code -----
def createArray():
     return [[0 for y in range(rows)] for y in range(cols)]

def populateBoard():
    board = createArray()
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j] = random.randint(0, 1)
    return board

def drawBoard(board):
    # Draw live cells
    for i in range(len(board)):
        for j in range(len(board[i])):
            x = i * res
            y = j * res
            if board[i][j] == 1:
                pygame.draw.rect(screen, black, (x+2, y+2, res-3, res-3))
    # Draw grid
    for x in range(cols):
        x *= res
        pygame.draw.line(screen, black, (x, 0), (x, height))
    for y in range(rows):
        y *= res
        pygame.draw.line(screen, black, (0, y), (width, y))

def sumNeighbours(array, x, y):
    sum = 0
    for i in -1, 0, 1:
        for j in -1, 0, 1:
            sum += array[(x+i)%cols][(y+j)%rows] # Wraps at board edges
    sum -= array[x][y]
    return sum

def update(current):
    next = createArray()
    for i in range(len(current)):
        for j in range(len(current[i])):
            state = current[i][j]
            sumN = sumNeighbours(current, i, j)
            if state == 1 and sumN < 2:         # Rule 1 - Underpopulation
                next[i][j] = 0
            if state == 1 and sumN in [2, 3]:   # Rule 2 - Lives on
                next[i][j] = 1
            if state == 1 and sumN > 3:         # Rule 3 - Overpopulation
                next[i][j] = 0
            if state == 0 and sumN == 3:        # Rule 4 - Reproduction
                next[i][j] = 1
    return next


# Run -----
current = populateBoard()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(white)
    drawBoard(current)

    next = update(current)
    current = next
    
    pygame.display.flip()
