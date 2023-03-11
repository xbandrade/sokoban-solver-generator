import random

import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle

from game import Game
from generator import generate
from widgets import Label, LevelClear

RESTART_EVENT = pygame.USEREVENT + 1
PREVIOUS_EVENT = pygame.USEREVENT + 2
NEXT_EVENT = pygame.USEREVENT + 3
RANDOM_GAME_EVENT = pygame.USEREVENT + 4
random.seed(5)

def play_game(window, level=1, random_game=False, random_seed=None, **widgets):
	moves = 0
	if random_game:
		if not random_seed:
			random_seed = random.randint(0, 99999)
		generate(window, seed=random_seed, visualizer=widgets['toggle'].getValue())
	if level <= 1:
		widgets['prev_button'].hide()
	else:
		widgets['prev_button'].show()
	if level >= 6:
		widgets['next_button'].hide()
	else:
		widgets['next_button'].show()
	if random_game or level == 0:
		widgets['label'].set_text(f'Seed {random_seed}', 18)
	else:
		widgets['label'].set_text(f'Level {level}', 30)
	game = Game(level=level, window=window)
	game_loop = True
	while game_loop:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				game_loop = False
				return {
					'keep_playing': False,
					'reset': -1, 
					'random_game': False,
				}
			elif event.type == RESTART_EVENT:
				game_loop = False
				print(f'Restarting level {level}\n')
				window.fill((0, 0, 0, 0))
				return {
					'keep_playing': True,
					'reset': level, 
					'random_game': False,
					'random_seed': random_seed,
				}
			elif event.type == PREVIOUS_EVENT:
				game_loop = False
				print(f'Previous level {level - 1}\n')
				window.fill((0, 0, 0, 0))
				return {
					'keep_playing': True,
					'reset': level - 1, 
					'random_game': False
				}
			elif event.type == NEXT_EVENT:
				game_loop = False
				print(f'Next level {level + 1}\n')
				window.fill((0, 0, 0, 0))
				return {
					'keep_playing': True,
					'reset': level + 1, 
					'random_game': False
				}
			elif event.type == RANDOM_GAME_EVENT:
				game_loop = False
				print('Loading a random puzzle\n')
				window.fill((0, 0, 0, 0))
				return {
					'keep_playing': True,
					'reset': 0, 
					'random_game': True,
				}
		moves += game.player.update()
		game.floor_group.draw(window)
		game.goal_group.draw(window)
		game.object_group.draw(window)
		pygame_widgets.update(events)
		widgets['label'].draw()
		widgets['visualizer'].draw_multiline()
		widgets['moves_label'].set_text(f' Moves - {moves} ', 20)
		pygame.display.update()
		if game.is_level_complete():
			print(f'Level Complete! - {moves} moves')
			widgets['level_clear'].draw()
			pygame.display.update()
			game_loop = False
			pygame.time.delay(2000)
		pygame.time.delay(100)
	pygame.time.delay(100)
	del game
	print('Objects cleared!\n')
	return {
		'keep_playing': True,
		'reset': 0 if random_game else -1, 
		'random_game': random_game,
	}


def sidebar_widgets(window):
	restart = Button(
		window, 1055, 140, 130, 40, text='Restart', radius=5,
		font=pygame.font.SysFont('Verdana', 18, bold=True),
		onClick=lambda: pygame.event.post(pygame.event.Event(RESTART_EVENT)),
		borderColor='black', borderThickness=2,
	)
	random_game = Button(
		window, 1055, 200, 130, 40, text='Random', radius=5,
		font=pygame.font.SysFont('Verdana', 18, bold=True),
		onClick=lambda: pygame.event.post(pygame.event.Event(RANDOM_GAME_EVENT)),
		borderColor='black', borderThickness=2,
	)
	visualizer = Label(window, f'Visualize\ngeneration', 1050, 260, 14)
	toggle = Toggle(window, 1160, 275, 20, 25, handleRadius=12)
	moves = Label(window, f' Moves - 0 ', 1055, 80, 20)
	prev_button = Button(
		window, 1030, 12, 22, 40, text='<', radius=2,
		font=pygame.font.SysFont('Verdana', 18, bold=True),
		onClick=lambda: pygame.event.post(pygame.event.Event(PREVIOUS_EVENT)),
		borderColor='black', borderThickness=2,
	)
	next_button = Button(
		window, 1188, 12, 22, 40, text='>', radius=2,
		font=pygame.font.SysFont('Verdana', 18, bold=True),
		onClick=lambda: pygame.event.post(pygame.event.Event(NEXT_EVENT)),
		borderColor='black', borderThickness=2,
	)
	label = Label(window, f'Level 0', 1055, 10, 30)
	level_clear = LevelClear(window, f'Level Clear!')
	return {
		'restart': restart,
		'random_button': random_game,
		'moves_label': moves,
		'prev_button': prev_button, 
		'next_button': next_button, 
		'label': label, 
		'level_clear': level_clear,
		'toggle': toggle,
		'visualizer': visualizer,
	}


def main():
	pygame.init()
	displayIcon = pygame.image.load('img/icon.png')
	pygame.display.set_icon(displayIcon)
	window = pygame.display.set_mode((1216, 640))
	pygame.display.set_caption('Sokoban')
	level = 1
	keep_playing = True
	random_game = False
	random_seed = None
	widgets = sidebar_widgets(window)
	while keep_playing:
		print(f'Loading level {level}\n')
		game_data = play_game(window, level, random_game, random_seed, **widgets)
		keep_playing = game_data.get('keep_playing', False)
		if not keep_playing:
			pygame.quit()
			quit()
		reset = game_data.get('reset', -1)
		random_game = game_data.get('random_game', False)
		random_seed = game_data.get('random_seed')
		level = reset if reset >= 0 else min(level + 1, 6)

	
if __name__ == '__main__':
	# wall: +, box: @, player: *, goal: X, box on goal: $, player on goal: %, empty: -
	main()