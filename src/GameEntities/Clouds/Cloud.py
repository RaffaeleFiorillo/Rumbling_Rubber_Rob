import random
import pygame
from src.Utils.GAME_conf import HEIGHT


class Cloud:
	IMAGES_NUMBER = 10
	IMAGES = [pygame.image.load(f"assets/Images/Clouds/Cloud_{i}.png") for i in range(1, IMAGES_NUMBER+1)]
	IMAGES_PROBABILITIES = [0.10, 0.10, 0.10, 0.10, 0.10, 0.04, 0.04, 0.20, 0.24, 0.04]
	SPEED_REDUCTION_FROM_LAYERS_DISTANCE = {-1: 0.4, 0: 0.8, 1: 1.2, 2: 1.4}
	AVERAGE_WIDTH = 150
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.layer = random.choice([-1, 0, 1, 2])
		
		self.image_alpha = 175 + self.layer*25  # random.randint(100, 255)
		# Adjust size based on layer
		scale_factor = 1.0 + (self.layer * 0.1)  # You can adjust the scale factor as needed
		image = random.choices(self.IMAGES, self.IMAGES_PROBABILITIES[:self.IMAGES_NUMBER])[0].convert_alpha()
		size = image.get_size()
		width, height = int(size[0] * scale_factor), int(size[1] * scale_factor)
		self.image = pygame.transform.scale(image, (width, height))
		self.image.set_alpha(self.image_alpha)  # makes the cloud translucent to a certain degree
		self.size = self.image.get_size()
		
		self.speed_reduction_according_to_speed = self.SPEED_REDUCTION_FROM_LAYERS_DISTANCE[self.layer]
	
	def is_inside_screen(self):
		return self.y-100 < HEIGHT  # the cloud should be deleted/replaced
	
	def update(self, ds: float):
		# the CloudManager should send by how much the cloud should move downwards
		self.y += ds*self.speed_reduction_according_to_speed
		# print(self.is_inside_screen())
		
	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))
