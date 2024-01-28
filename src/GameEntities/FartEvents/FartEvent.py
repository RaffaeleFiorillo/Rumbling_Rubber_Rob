import pygame
from src.Utils.GAME_conf import HEIGHT as S_HEIGHT, WIDTH as S_WIDTH, COLOR as S_COLOR
from src.GameEntities.MainCharacter import FartingBalloon


class FartEvent:
	WIDTH = S_WIDTH
	HEIGHT = FartingBalloon.IMAGE.get_size()[1] + 50
	COLOR = tuple(int(pixel_value*0.4) for pixel_value in S_COLOR)
	
	def __init__(self, x, y, duration):
		self.x = x
		self.y = self.HEIGHT+y
		self.duration = duration
		self.has_been_activated = False
	
	def is_inside_screen(self):
		return 0 < self.y + self.HEIGHT and self.y - self.HEIGHT < S_HEIGHT  # the cloud should be deleted/replaced
	
	def is_before_screen(self):
		return 0 < self.y + self.HEIGHT
	
	def update(self, ds: float):
		self.y -= ds  # the FartEventManager should send by how much the cloud should move downwards
	
	def draw(self, screen):
		pygame.draw.rect(screen, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT), 0, 5, 5, 5, 5)
