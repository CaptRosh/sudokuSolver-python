import pygame
from boards import getBoard
import time

pygame.font.init()

class Cube:
    rows = 9
    cols = 9

    def __init__(self,value,row,col,width,height):
        self.value = value
        self.pencil = 0
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.select = False

    def draw(self,win):
        font = pygame.font.SysFont("Arial", 35)

        dist = self.width/9
        x = self.col * dist
        y = self.row * dist

        if self.pencil != 0 and self.value == 0:
            win.blit(font.render(str(self.pencil),1,(130,130,130)),(x+5,y+5))
        elif self.value != 0:
            text = font.render(str(self.value),1,(0,0,0))
            win.blit(text,(x + (dist/2 - text.get_width()/2), y + (dist/2 - text.get_height()/2)))
        
        if self.select:
            pygame.draw.rect(win,(255,0,0),(x,y,dist,dist),3)
    
    def change(self,win,correct=True):
        font = pygame.font.SysFont("Arial", 35)

        dist = self.width/9
        x = self.col * dist
        y = self.row * dist

        pygame.draw.rect(win,(255,255,255),(x,y,dist,dist),0)
        
        text = font.render(str(self.value),1,(0,0,0))
        win.blit(text,(x + (dist / 2 - text.get_width() / 2), y + (dist / 2 - text.get_height() / 2)))

        if correct:
            pygame.draw.rect(win,(0,255,0),(x,y,dist,dist),3)
        else:
            pygame.draw.rect(win,(255,0,0),(x,y,dist,dist),3)

    def set_val(self, val):
        self.value = val
    
    def set_temp(self, val):
        self.pencil = val

class Grid:

    board = getBoard()

    def __init__(self,rows,cols,width,height,win):
        self.rows = rows
        self.cols = cols
        self.height = height
        self.width = width
        self.cubes = [[Cube(self.board[i][j],i,j,width,height) for j in range(cols)] for i in range(rows)]
        self.model = None 
        self.update()
        self.selected = None
        self.win = win

    def update(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def pos(self,val):
        row,col = self.selected

        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_val(val)
            self.update()
        
        if plausible(self.model,val,(row,col)) and self.solved():
            return True
        else:
            self.cubes[row][col].set_val(0)
            self.cubes[row][col].set_temp(0)
            self.update()
            return False
    
    def sketch(self,val):
        self.cubes[self.selected[0]][self.selected[1]].set_temp(val)
    
    def draw(self):

        dist = self.width/9

        for i in range(self.rows + 1):
            if i%3 == 0 and i != 0:
                w = 4
            else: 
                w = 1

            pygame.draw.line(self.win,(0, 0, 0),(0,i*dist),(self.width,i*dist), w)
            pygame.draw.line(self.win, (0, 0, 0), (i * dist, 0), (i * dist, self.height), w)

        
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)
    
    def select(self,row,col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].select = False
        
        self.cubes[row][col].select = True
        self.selected = (row,col)
    
    def clear(self):
        row,col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            dist = self.width/9
            x = pos[0]//dist
            y = pos[1]//dist

            return (int(y),int(x))
        else:
            return None
    
    def finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
    def solved(self):
        find = findEmp(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if plausible(self.model,i,(row,col)):
                self.model[row][col] = i
            
                if self.solved():
                    return True
            
                self.model[row][col] = 0
        
        return False
    
    def solved_gui(self):
        find = findEmp(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if plausible(self.model,i,(row,col)):
                self.model[row][col] = i
                self.cubes[row][col].set_val(i)
                self.cubes[row][col].change(self.win,True)
                self.update()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solved_gui():
                    return True
                
                self.model[row][col] = 0
                self.cubes[row][col].set_val(0)
                self.update()
                self.cubes[row][col].change(self.win,False)
                pygame.display.update()
                pygame.time.delay(100)
        
        return False

def findEmp(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return (i,j)

    return None

def plausible(b,num,pos):
    for i in range(len(b[0])):
        if b[pos[0]][i] == num and pos[1] != i:
            return False
        
    for i in range(len(b)):
        if b[i][pos[1]] == num and pos[0] != i:
            return False

    x_coord = pos[1]//3
    y_coord = pos[0]//3

    for i in range(y_coord*3,y_coord*3 + 3):
        for j in range(x_coord*3,x_coord*3 + 3):
            if b[i][j] == num and (i,j) != pos:
                return False
    
    return True 

def redraw(win,b,time,strikes):
    win.fill((255,255,255))

    font = pygame.font.SysFont('Arial',35)
    win.blit(font.render("Time: " + format_time(time),1,(0,0,0)),(540-160,560))

    win.blit(font.render(("X " * strikes),1,(255,0,0)),(20,560))
    
    b.draw()

def format_time(t):
    sec = t%60
    min = t//60
    hour = min//60

    if sec//10 == 0:
        return " " + str(min) + ":0" + str(sec)
    else:
        return " " + str(min) + ":" + str(sec)


win = pygame.display.set_mode((540,600))
pygame.display.set_caption("Sudoku Solver")

board = Grid(9,9,540,540,win)
key = None
run = True
start = time.time()
strikes = 0

while run:
    play = round(time.time() - start)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_1:
                key =  1
            if e.key == pygame.K_2:
                key =  2
            if e.key == pygame.K_3:
                key =  3
            if e.key == pygame.K_4:
                key =  4
            if e.key == pygame.K_5:
                key =  5
            if e.key == pygame.K_6:
                key =  6
            if e.key == pygame.K_7:
                key =  7
            if e.key == pygame.K_8:
                key =  8
            if e.key == pygame.K_9:
                key =  9
            if e.key == pygame.K_DELETE:
                board.clear()
                key = None
            
            if e.key == pygame.K_SPACE:
                board.solved_gui()

            if e.key == pygame.K_RETURN:
                r,c = board.selected
                if board.cubes[r][c].pencil != 0:
                    if not board.pos(board.cubes[r][c].pencil):
                        strikes += 1
                    key = None

                if board.finished():
                    print("Game over")
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            click = board.click(pos)

            if click:
                board.select(click[0],click[1])
                key = None
    
    if board.selected and key != None:
        board.sketch(key)
    
    redraw(win,board,play,strikes)
    pygame.display.update()

pygame.quit()