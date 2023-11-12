import time
from collections import deque
from queue import PriorityQueue
import heapq
import numpy as np
import pygame

from src.utils import can_move, get_state, is_deadlock, is_solved, print_state







def dfs(matrix, player_pos, widget=None, visualizer=False):
    print('Depth-First Search')
    initial_state = get_state(matrix)
    shape = matrix.shape
    print_state(initial_state, shape)
    seen = {None}
    stack = [(initial_state, player_pos, 0, '')]
    moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    curr_depth = 0
    direction = {
        (1, 0): 'D',
        (-1, 0): 'U',
        (0, -1): 'L',
        (0, 1): 'R',
    }
    while stack:
        if widget:
            pygame.event.pump()
        state, pos, depth, path = stack.pop()
        # if depth != curr_depth:
        #     print(f'Depth: {depth}')
        #     curr_depth = depth
        seen.add(state)
        for move in moves:
            new_state, _ = can_move(state, shape, pos, move)
            deadlock = is_deadlock(new_state, shape)
            if new_state in seen or deadlock:
                continue
            stack.append((
                new_state,
                (pos[0] + move[0], pos[1] + move[1]),
                depth + 1,
                path + direction[move],
            ))
            if is_solved(new_state):
                print(f'[DFS] Solution found!\n\n{path + direction[move]}\nDepth {depth + 1}\n')
                if widget and visualizer:
                    widget.solved = True
                    widget.set_text(f'[DFS] Solution Found!\n{path + direction[move]}', 20)
                    pygame.display.update()
                return (path + direction[move], depth + 1)
            if widget and visualizer:
                widget.set_text(f'[DFS] Solution Depth: {depth + 1}\n{path + direction[move]}', 20)
                pygame.display.update()
    print(f'[DFS] Solution not found!\n')
    if widget and visualizer:
        widget.set_text(f'[DFS] Solution Not Found!\nDepth {depth + 1}', 20)
        pygame.display.update()
    return (None, -1 if not stack else depth + 1)




def ucs(matrix, player_pos, widget=None, visualizer=False):
    print('Uniform Cost Search')
    initial_state = get_state(matrix)
    shape = matrix.shape
    print_state(initial_state, shape)
    seen = {None}
    pq = [(0, (initial_state, player_pos, 0, ''))]
    moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    curr_depth = 0
    direction = {
        (1, 0): 'D',
        (-1, 0): 'U',
        (0, -1): 'L',
        (0, 1): 'R',
    }
    while pq:
        if widget:
            pygame.event.pump()
        cost, (state, pos, depth, path) = heapq.heappop(pq)
        if state in seen:
            continue
        seen.add(state)
        for move in moves:
            new_state, _ = can_move(state, shape, pos, move)
            deadlock = is_deadlock(new_state, shape)
            if new_state in seen or deadlock:
                continue
            new_cost = cost + 1  # Uniform cost
            heapq.heappush(pq, (new_cost, (
                new_state,
                (pos[0] + move[0], pos[1] + move[1]),
                depth + 1,
                path + direction[move],
            )))
            if is_solved(new_state):
                print(f'[UCS] Solution found!\n\n{path + direction[move]}\nDepth {depth + 1}\n')
                if widget and visualizer:
                    widget.solved = True
                    widget.set_text(f'[UCS] Solution Found!\n{path + direction[move]}', 20)
                    pygame.display.update()
                return (path + direction[move], depth + 1)
            if widget and visualizer:
                widget.set_text(f'[UCS] Solution Depth: {depth + 1}\n{path + direction[move]}', 20)
                pygame.display.update()
    print(f'[UCS] Solution not found!\n')
    if widget and visualizer:
        widget.set_text(f'[UCS] Solution Not Found!\nDepth {depth + 1}', 20)
        pygame.display.update()
    return (None, -1 if not pq else depth + 1)







def solve_dfs(puzzle, widget=None, visualizer=False):
	matrix = puzzle
	where = np.where((matrix == '*') | (matrix == '%'))
	player_pos = where[0][0], where[1][0]
	return dfs(matrix, player_pos, widget, visualizer)

def solve_ucs(puzzle, widget=None, visualizer=False):
	matrix = puzzle
	where = np.where((matrix == '*') | (matrix == '%'))
	player_pos = where[0][0], where[1][0]
	return ucs(matrix, player_pos, widget, visualizer)

	
if __name__ == '__main__':
	start = time.time()
	root = solve_dfs(np.loadtxt('levels/lvl7.dat', dtype='<U1'))
	print(f'Runtime: {time.time() - start} seconds')


# matrix = np.array([
#     ['+', '+', '+', '+', '+', '+', '+'],
#     ['+', '*', '-', '@', '-', 'X', '+'],
#     ['+', '+', '-', '@', '-', '+', '+'],
#     ['+', 'X', '-', '-', '-', '$', '+'],
#     ['+', '+', '+', '+', '+', '+', '+']
# ])


# print('da solve: ',solve_bfs(matrix))
# print('da solve: ',solve_dfs(matrix))
# print('da solve: ',solve_ucs(matrix))