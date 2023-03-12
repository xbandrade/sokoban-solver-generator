import pygame


class Label:
	def __init__(self, window, text, x, y, font_size, transparency=False, color='black'):
		self.x = x
		self.y = y
		self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
		self.lines = text.split('\n')
		if len(self.lines) == 1:
			self.image = self.font.render(text, 1, color)
		self.images = [self.font.render(line, 1, color) for line in self.lines]
		self.max_width = max(image.get_width() for image in self.images)
		self.total_height = (sum(image.get_height() for image in self.images) + 
		  				(len(self.lines) - 1) * font_size // 2)
		self.rect = pygame.Rect(x, y, self.max_width + 10, self.total_height + 10)
		self.window = window
		self.transparency = transparency
		self.solved = False

	def set_text(self, new_text, font_size, color='black'):
		self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
		self.image = self.font.render(new_text, 1, color)
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
		self.window.blit(self.image, (text_pos_x, text_pos_y))

		
	def set_multiline(self, new_text, font_size, color='black'):
		self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
		self.text = new_text
		self.lines = new_text.split('\n')
		self.images = [self.font.render(line, 1, color) for line in self.lines]
		self.max_width = max(self.max_width, max(image.get_width() for image in self.images))
		self.total_height = (sum(image.get_height() for image in self.images) + 
		  					 (len(self.lines) - 1) * font_size // 2)
		self.rect = pygame.Rect(self.x, self.y, self.max_width + 10, self.total_height + 10)
		self.draw_multiline()

	def draw_multiline(self):
		transparent_surface = pygame.Surface(
			(self.rect.width, self.rect.height), pygame.SRCALPHA
		)
		transparent_surface.set_alpha(160)
		transparent_surface.fill((200, 0, 0) if not self.solved else (0, 255, 0))
		if not self.transparency:
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
		if self.transparency:
			self.window.blit(transparent_surface, (self.rect.x, self.rect.y))
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
		self.image = self.font.render(text, 1, color)

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
