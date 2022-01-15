import pygame
import time
import numpy as np
from dokusan import generators
from solver import *
pygame.font.init()

class Grid:
    # Create board for the Sudoku
    # random board generator
    grid = np.array(list(str(generators.random_sudoku(avg_rank = 3))))
    # reshaping the list into a 9x9 array
    bo = grid.reshape(9,9)
    # change the list from strings to integers
    board = bo.astype(int)
    
    # Create the constructor for the Grid
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        # Make cube with value of board with row i and column j
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(9)] for i in range(9)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    # function to update the model
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    # set a sketch of a number clicked by the user but not entered yet (preview)
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    # Function to validate if the value sketched by the user can be entered
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()
            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    # draw the board
    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            # separates the board with thicker lines by 3x3
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw boxes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    # function to show selection of box clicked by the user
    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # clears the box selected
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # Show box that is clicked by the user
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    # checks if the board is done or not
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    # draw window
    def draw(self, win):
        font = pygame.font.SysFont("timesnewroman", 30)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        # Creates a blue outline around the box when it is clicked
        if self.selected:
            pygame.draw.rect(win, (0,0,255), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

# redraw window
def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    font = pygame.font.SysFont("timesnewroman", 30)
    textfont = pygame.font.SysFont("comicsans", 30)
    text = font.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 555))
    # Draw Strikes
    text = textfont.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 550))
    # Draw grid and board
    board.draw(win)

# show time running the program
def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hours = secs // 3600

    time = " " + str(hours) + ":" + str(minute) + ":" + str(sec)
    return time

def main():
    # Set window 
    win = pygame.display.set_mode((540,600))
    # Set caption
    pygame.display.set_caption("Sudoku")
    # Set board
    board = Grid(9, 9, 540, 540)
    # set default key value to none
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:

        play_time = round(time.time() - start)

        # Allocation of keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    # if cube of row i and col j is not empty
                    if board.cubes[i][j].temp != 0:
                        # if correct print(success) else print(wrong)
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            # add 1 strike if wrong
                            strikes += 1
                        # erase the sketched value
                        key = None

                        # if the board is done print(gameover) and stop the program from running
                        if board.is_finished():
                            print("Game over")
                            print("Thank you for playing")
                            # draw "Game Over after done"
                            win.fill((255,255,255))
                            font = pygame.font.SysFont("timesnewroman",30)
                            text = font.render("Game Over", True, (0,0,0))
                            text_rect = text.get_rect()
                            text_rect.center = (540/2, 600/2)
                            win.blit(text, text_rect)
                            pygame.display.update()
                            # add time after "Game Over" is displayed and the window closes
                            pygame.time.wait(2000)
                            run = False
                
                # same as the above function but with numpad
                if event.key == pygame.K_KP_ENTER:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            print("Thank you for playing")
                            win.fill((255,255,255))
                            font = pygame.font.SysFont("timesnewroman",30)
                            text = font.render("Game Over", True, (0,0,0))
                            text_rect = text.get_rect()
                            text_rect.center = (540/2, 600/2)
                            win.blit(text, text_rect)
                            pygame.display.update()
                            pygame.time.wait(2000)
                            run = False

            # Allocation of mouse's use
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        
        # Sketch the value clicked by the user but not enter it yet
        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

main()
pygame.quit()