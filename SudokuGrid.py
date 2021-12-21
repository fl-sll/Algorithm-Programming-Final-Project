import pygame
import time
import numpy as np
from dokusan import generators
from solver import solve,valid
pygame.font.init()

class Grid:
    # Create board for the Sudoku
    grid = np.array(list(str(generators.random_sudoku(avg_rank = 150))))
    bo = grid.reshape(9,9)
    board = bo.astype(int)
    
    # Create the constructor for the object
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(9)] for i in range(9)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    # function to update the model
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

class Cube:
    rows = 9
    cols = 9