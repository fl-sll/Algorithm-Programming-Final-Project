import pygame
import time
import numpy as np
from dokusan import generators
from solver import solve,valid
pygame.font.init()

class Grid:
    grid = np.array(list(str(generators.random_sudoku(avg_rank = 150))))
    bo = grid.reshape(9,9)
    board = bo.astype(int)