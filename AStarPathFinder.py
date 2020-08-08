import pygame as pg
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pg.display.set_mode((WIDTH,WIDTH))
pg.display.set_caption("A* Path Finding Algorithm")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Spot:
    def __init__(self,row,col,width,allrows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.allrows = allrows

    def get_pos(self):
        return self.row, self.col
    def isclosed(self):
        return self.color == RED
    def isopen(self):
        return self.color == GREEN
    def isbarrier(self):
        return self.color == BLACK
    def isstart(self):
        return self.color == ORANGE
    def isend(self):
        return self.color == TURQUOISE
    def reset(self):
        self.color = WHITE
    def makestart(self):
        self.color = ORANGE
    def makecolsed(self):
        self.color = RED
    def makebarrier(self):
        self.color = BLACK
    def makeopen(self):
        self.color = GREEN
    def makeend(self):
        self.color = TURQUOISE
    def makepath(self):
        self.color = PURPLE
    def draw(self, win):
        pg.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    def updateneighbors(self, grid):
        self.neighbors = []
        if self.row < self.allrows - 1 and not grid[self.row +1][self.col].isbarrier():
            self.neighbors.append(grid[self.row +1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].isbarrier():
            self.neighbors.append(grid[self.row - 1][self.col])
            
        if self.col < self.allrows - 1 and not grid[self.row ][self.col + 1].isbarrier():
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self.row > 0 and not grid[self.row][self.col - 1].isbarrier():
            self.neighbors.append(grid[self.row][self.col - 1])
            
    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def path(comefrom,current, draw):
    while current in comefrom:
        current = comefrom[current]
        current.makepath()
        draw()
def algorithm(draw,grid,start,end):
    count = 0
    openset = PriorityQueue()
    openset.put((0, count, start))
    camefrom = {}
    gscore = {spot: float("inf") for row in grid for spot in row}
    gscore[start] = 0
    fscore = {spot: float("inf") for row in grid for spot in row}
    fscore[start] = h(start.get_pos(), end.get_pos())

    opensethash = {start}

    while not openset.empty():
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()

        current = openset.get()[2]
        opensethash.remove(current)

        if current == end:
            path(camefrom,end,draw)
            end.makeend()
            return True

        for neighbor in current.neighbors:
            tmpgscore = gscore[current] + 1

            if tmpgscore < gscore[neighbor]:
                camefrom[neighbor] = current
                gscore[neighbor] = tmpgscore
                fscore[neighbor] = tmpgscore + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in opensethash:
                    count += 1
                    openset.put((fscore[neighbor], count, neighbor))
                    opensethash.add(neighbor)
                    neighbor.makeopen()

        draw()

        if current != start:
            current.makecolsed()
    return False
def makegrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid

def drawgrid(win, rows, width):
    gap = width //rows
    for i in range(rows):
        pg.draw.line(win, GREY,(0, i*gap),(width,i*gap))
        for j in range(rows):
            pg.draw.line(win, GREY, (j*gap,0),(j*gap,width))
    
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    drawgrid(win,rows,width)
    pg.display.update()

def getpos(pos,rows,width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = makegrid(ROWS, width)
    start = None
    end = None
    run = True
    while run:
        draw(win,grid,ROWS,width)
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                run = False
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                row, col = getpos(pos,ROWS,width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.makestart()
                elif not end and spot != start:
                    end = spot
                    end.makeend()
                elif spot != end and spot != start:
                    spot.makebarrier()
            elif pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos()
                row, col = getpos(pos,ROWS,width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.updateneighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width),grid, start, end)
                if ev.key == pg.K_c:
                    start = None
                    end = None
                    grid = makegrid(ROWS, width)

    pg.quit()
main(WIN,WIDTH)
