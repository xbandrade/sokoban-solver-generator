from collections import deque

import numpy as np
import pygame


def print_state(state, shape):
	m, n = shape
	matrix = np.array(list(state)).reshape(m, n)
	print(matrix)

def find_boxes(s):
	indices = []
	i = s.find('@')
	while i != -1:
		indices.append(i)
		i = s.find('@', i + 1)
	return indices


def is_deadlock(state, shape):
	if not state:
		return False
	height, width = shape
	boxes = find_boxes(state)
	for box in boxes:
		if ((state[box - 1] == '+' and state[box - width] == '+') or
			(state[box + 1] == '+' and state[box + width] == '+')):
			return True
	box = goal = 0
	for i in range(width + 1, 2 * width - 1):
		if state[i] == '@':
			box += 1
		elif state[i] in 'X%':
			goal += 1
	if box > goal:
		return True
	box = goal = 0
	for i in range(width * (height - 2) + 1, width * (height - 2) + width - 1):
		if state[i] == '@':
			box += 1
		elif state[i] in 'X%':
			goal += 1
	if box > goal:
		return True
	box = goal = 0
	for i in range(width + 1, width * (height - 1) + 1, width):
		if state[i] == '@':
			box += 1
		elif state[i] in 'X%':
			goal += 1
	if box > goal:
		return True
	box = goal = 0
	for i in range(2 * width - 2, width * height - 2, width):
		if state[i] == '@':
			box += 1
		elif state[i] in 'X%':
			goal += 1
	if box > goal:
		return True
	return False


def get_state(matrix):
	return matrix.tobytes().decode('utf-8').replace('\x00', '')

def is_solved(state):
	return '@' not in state

def can_move(state, shape, player_pos, move):
	new_state = list(state)
	x, y = player_pos
	_, width = shape
	target = x + move[0], y + move[1]
	boxtarget = x + move[0] * 2, y + move[1] * 2
	curr1d = x * width + y
	target1d = target[0] * width + target[1]
	boxtarget1d = boxtarget[0] * width + boxtarget[1]
	if state[target1d] == '+':
		return None
	elif state[target1d] in '-X':
		new_state[curr1d] = '-' if new_state[curr1d] == '*' else 'X'
		new_state[target1d] = '*' if new_state[target1d] == '-' else '%'
	elif state[target1d] in '@$':
		if state[boxtarget1d] in '+@$':
			return None
		elif state[boxtarget1d] in '-X':
			new_state[boxtarget1d] = '@' if new_state[boxtarget1d] == '-' else '$'
			new_state[target1d] = '*' if new_state[target1d] == '@' else '%'
			new_state[curr1d] = '-' if new_state[curr1d] == '*' else 'X'
	return ''.join(new_state)


def bfs(matrix, player_pos, widget=None, visualizer=False):
	initial_state = get_state(matrix)
	shape = matrix.shape
	print_state(initial_state, shape)
	seen = {None}
	q = deque([(initial_state, player_pos, 0, '')])
	moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
	curr_depth = 0
	direction = {
		(1, 0): 'D',
		(-1, 0): 'U', 
		(0, -1): 'L',
		(0, 1): 'R',
	}
	with open('bfs.dat', 'w') as f:
		while q:
			pygame.event.pump()
			state, pos, depth, path = q.popleft()
			if depth != curr_depth:
				print(f'Depth: {depth}')
				curr_depth = depth
			seen.add(state)
			for move in moves:
				new_state = can_move(state, shape, pos, move)
				deadlock = is_deadlock(new_state, shape)
				if new_state in seen or deadlock:
					continue
				q.append((
					new_state, 
					(pos[0] + move[0], pos[1] + move[1]),
					depth + 1,
					path + direction[move],
				))
				if is_solved(new_state):
					print(f'Solution found!\n\n{path + direction[move]}\nDepth {depth + 1}\n')
					if widget and visualizer:
						widget.solved = True
						widget.set_multiline(f'Solution Found!\n{path + direction[move]}', 14, True)
						pygame.display.update()
					return (path + direction[move], depth + 1)
				# print(root.children)
				if widget and visualizer:
					widget.set_multiline(f'Solution Depth: {depth + 1}\n{path + direction[move]}', 14, True)
					pygame.display.update()
		print(f'Solution not found!\n')
		if widget and visualizer:
			widget.set_multiline(f'Solution Not Found!\nDepth {depth + 1}', 14, True)
			pygame.display.update()
		return (None, -1 if not q else depth + 1)

def solve(puzzle, widget=None, visualizer=False):
	# matrix = np.loadtxt('levels/lvl1.dat', dtype='<U1')
	matrix = puzzle
	where = np.where((matrix == '*') | (matrix == '%'))
	player_pos = where[0][0], where[1][0]
	return bfs(matrix, player_pos, widget, visualizer)

	
if __name__ == '__main__':
	root = solve(np.loadtxt('levels/lvl1.dat', dtype='<U1'))