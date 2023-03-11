import pygame


class Label:
	def __init__(self, window, text, x, y, font_size, color='black'):
		self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
		self.lines = text.split('\n')
		self.images = [self.font.render(line, 1, color) for line in self.lines]
		max_width = max(image.get_width() for image in self.images)
		total_height = (sum(image.get_height() for image in self.images) + 
		  				(len(self.lines) - 1) * font_size // 2)
		self.rect = pygame.Rect(x, y, max_width + 10, total_height + 10)
		self.window = window
		self.text = text

	def set_text(self, new_text, font_size, color='black'):
		self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
		self.text = new_text
		self.image = self.font.render(new_text, 1, color)
		_, _, w, h = self.image.get_rect()
		self.rect = pygame.Rect(self.rect.x, self.rect.y, w + 10, h + 10)
		self.draw()

	def draw(self):
		pygame.draw.rect( 
			self.window, 
			pygame.Color('gray'), 
			(self.rect.x, 
    		self.rect.y, 
			self.rect.width, 
			self.rect.height) 
		) 
		pygame.draw.rect( 
			self.window, 
			(0, 0, 0), 
			(self.rect.x, 
    		self.rect.y, 
			self.rect.width, 
			self.rect.height), 
			width=3 
		) 
		text_pos_x = (self.rect.width - self.image.get_width()) // 2 + self.rect.x 
		text_pos_y = (self.rect.height - self.image.get_height()) // 2 + self.rect.y 
		self.window.blit(self.image, (text_pos_x,text_pos_y))


	def draw_multiline(self):
		pygame.draw.rect(
			self.window,
			pygame.Color('gray'),
			(self.rect.x,
			self.rect.y,
			self.rect.width,
			self.rect.height)
		)
		pygame.draw.rect(
			self.window,
			(0, 0, 0),
			(self.rect.x,
			self.rect.y,
			self.rect.width,
			self.rect.height),
			width=3
		)
		offset = ((self.rect.height - sum(image.get_height() for image in self.images) - 
				   (len(self.images) - 1)) // 2 + self.rect.y)
		for image in self.images:
			text_pos_x = (self.rect.width - image.get_width()) // 2 + self.rect.x
			text_pos_y = offset
			offset += image.get_height()
			self.window.blit(image, (text_pos_x,text_pos_y))


class LevelClear(Label):
	def __init__(self, window, text, x=256, y=192, font_size=60, color='black'):
		super().__init__(window, text, x, y, font_size, color)
		self.w, self.h = 512, 256
		self.rect = pygame.Rect(x, y, self.w, self.h)

	def draw(self):
		transparent_surface = pygame.Surface(
			(self.rect.width, self.rect.height), pygame.SRCALPHA
		)
		transparent_surface.set_alpha(100)
		transparent_surface.fill((0, 255, 0))
		pygame.draw.rect(
			self.window,
			'#008000',
			(self.rect.x,
			self.rect.y,
			self.rect.width,
			self.rect.height),
			width=4
		)
		text_pos_x = (self.rect.width - self.image.get_width()) // 2 + self.rect.x
		text_pos_y = (self.rect.height - self.image.get_height()) // 2 + self.rect.y
		self.window.blit(transparent_surface, (self.rect.x, self.rect.y))
		self.window.blit(self.image, (text_pos_x,text_pos_y))
