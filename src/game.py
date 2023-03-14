import numpy as np
import pygame

from src.utils import get_state

from .box import Box, Obstacle
from .floor import Floor, Goal
from .player import Player, ReversePlayer


class PuzzleElement:
    def __init__(self, char, obj=None, ground=None):
        self.char = char
        self.ground = ground
        self.obj = obj

    def __str__(self):
        return self.char

class Game:
    def __init__(self, window=None, width=1216, height=640, level=None, seed=None, path=None):
        self.seed = seed
        self.window = window
        self.level = level
        self.width = width
        self.height = height
        self.puzzle = np.empty((height // 64, width // 64), dtype=PuzzleElement)
        self.floor_group = pygame.sprite.Group()
        self.object_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.goal_group = pygame.sprite.Group()
        self.player = None
        self.puzzle_size = None
        self.pad_x = 0
        self.pad_y = 0
        self.path = path or f'levels/lvl{level}.dat'
        self.load_floor()
        if type(self) == Game:
            self.load_puzzle()

    def __del__(self):
        self.clear_objects()

    def get_matrix(self):
        slice_x = slice(self.pad_x, self.pad_x + self.puzzle_size[1])
        slice_y = slice(self.pad_y, self.pad_y + self.puzzle_size[0])
        sliced = self.puzzle[slice_y, slice_x]
        matrix = np.empty((self.puzzle_size), dtype='<U1')
        for h in range(len(sliced)):
            for w in range(len(sliced[0])):
                matrix[h, w] = sliced[h, w].char
        return matrix
    
    def get_curr_state(self):
        return get_state(self.get_matrix())

    def print_puzzle(self):
        for h in range(self.height // 64):
            for w in range(self.width // 64):
                if self.puzzle[h, w]:
                    print(self.puzzle[h, w].char, end=' ')
                else:
                    print(' ', end=' ')
            print(' ')

    def is_level_complete(self):
        boxes_left = 0
        for h in range(self.height // 64):
            for w in range(self.width // 64):
                if self.puzzle[h, w] and self.puzzle[h, w].char == '@':
                    boxes_left += 1
        return boxes_left == 0

    def clear_objects(self):
        for sprite in self.object_group:
            del sprite
        for sprite in self.floor_group:
            del sprite

    def load_floor(self):
        for i in range(self.width // 64):
            for j in range(self.height // 64):
                Floor(self.floor_group, x=i, y=j)

    def load_puzzle(self):
        try:
            with open(self.path) as f:
                lines = f.readlines()
                self.puzzle_size = (len(lines), len(lines[0].strip().split()))
                pad_x = (self.width // 64 - self.puzzle_size[1] - 2) // 2
                pad_y = (self.height // 64 - self.puzzle_size[0]) // 2
                self.pad_x, self.pad_y = pad_x, pad_y
            with open(self.path) as f:
                for i, line in enumerate(f):
                    for j, c in enumerate(line.strip().split()):
                        new_elem = PuzzleElement(c)
                        self.puzzle[i + pad_y, j + pad_x] = new_elem
                        if c == '+':  # wall
                            new_elem.obj = Obstacle(self.object_group, x=j + pad_x, y=i + pad_y)
                        elif c == '@':  # box
                            new_elem.obj = Box(self.object_group, x=j + pad_x, y=i + pad_y, game=self)
                        elif c == '*':  # player
                            new_elem.obj = Player(
                                self.object_group, self.player_group, 
                                x=j + pad_x, y=i + pad_y, game=self
                            )
                            self.player = new_elem.obj
                        elif c == 'X':  # goal
                            new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                        elif c == '$':  # box on goal
                            new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                            new_elem.obj = Box(self.object_group,  x=j + pad_x, y=i + pad_y, game=self)
                        elif c == '%':  # player on goal
                            new_elem.obj = Player(
                                self.object_group, self.player_group, 
                                x=j + pad_x, y=i + pad_y, game=self
                            )
                            new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                            self.player = new_elem.obj
                        elif c not in ' -':
                            raise ValueError(
                                f'Invalid character on file lvl{self.level}.dat: {c}'
                            )
        except (OSError, ValueError) as e:
            print(f'{e}')
            self.clear_objects()
            return


class ReverseGame(Game):
    def __init__(self, window=None, width=1216, height=640, level=None, seed=None):
        super().__init__(window, width, height, level, seed)
        self.pad_x = 0
        self.pad_y = 0

    def load_puzzle(self, puzzle):
        pad_x = (self.width // 64 - len(puzzle[0]) - 2) // 2
        pad_y = (self.height // 64 - len(puzzle)) // 2
        self.pad_x, self.pad_y = pad_x, pad_y
        for i, row in enumerate(puzzle):
            for j, c in enumerate(row):
                new_elem = PuzzleElement(c)
                self.puzzle[i + pad_y, j + pad_x] = new_elem
                if c == '+':  # wall
                    new_elem.obj = Obstacle(self.object_group, x=j + pad_x, y=i + pad_y)
                elif c == '@':  # box
                    new_elem.obj = Box(self.object_group, x=j + pad_x, y=i + pad_y, game=self)
                elif c == '*':  # player
                    new_elem.obj = ReversePlayer(
                        self.object_group, self.player_group, 
                        x=j + pad_x, y=i + pad_y, game=self
                    )
                    self.player = new_elem.obj
                elif c == 'X':  # goal
                    new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                elif c == '$':  # box on goal
                    new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                    new_elem.obj = Box(self.object_group,  x=j + pad_x, y=i + pad_y, game=self)
                elif c == '%':  # player on goal
                    new_elem.obj = ReversePlayer(
                        self.object_group, self.player_group, 
                        x=j + pad_x, y=i + pad_y, game=self
                    )
                    new_elem.ground = Goal(self.goal_group, x=j + pad_x, y=i + pad_y)
                    self.player = new_elem.obj

    
    