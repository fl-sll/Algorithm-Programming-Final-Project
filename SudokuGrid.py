import pygame
import time
from solver import solve,valid
pygame.font.init()

class Grid:
    board = [
        [9, 2, 0, 0, 0, 0, 5, 8, 4],
        [0, 0, 0, 5, 0, 0, 0, 0, 3],
        [0, 8, 3, 0, 9, 2, 0, 0, 0],
        [2, 6, 0, 8, 5, 4, 0, 0, 1],
        [0, 0, 5, 3, 6, 1, 0, 9, 0],
        [1, 0, 0, 0, 0, 9, 0, 0, 0],
        [8, 5, 0, 2, 0, 3, 0, 1, 0],
        [4, 1, 2, 9, 8, 0, 0, 3, 0],
        [3, 9, 0, 0, 0, 6, 8, 0, 0]
    ]