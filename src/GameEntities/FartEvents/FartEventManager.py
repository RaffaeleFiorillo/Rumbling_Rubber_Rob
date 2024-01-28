import random

import pygame
import math
from .FartEvent import FartEvent


class FartEventManager:
	POINTER_COO = (661, 392)
	GOOD_FART_SOUND = pygame.mixer.Sound("assets/Sounds/good_fart.mp3")
	BAD_FART_SOUND = pygame.mixer.Sound("assets/Sounds/bad_fart.mp3")
	SUPER_BAD_FART_SOUND = pygame.mixer.Sound("assets/Sounds/bad_fart.mp3")
	GOOD_PENALTY = 0.5
	SEMI_BAD_PENALTY = GOOD_PENALTY*10
	BAD_PENALTY = GOOD_PENALTY*40
	SUPER_BAD_PENALTY = GOOD_PENALTY*100
	FREQUENCIES = [1.5, 1, 0.75]
	FREQUENCIES_LEVEL = {f: i+1 for i, f in enumerate(FREQUENCIES)}
	FREQUENCY_CHANGE_PROBABILITY = 0.01
	FREQUENCY_CHANGE_PROBABILITIES = [FREQUENCY_CHANGE_PROBABILITY, 1-FREQUENCY_CHANGE_PROBABILITY]
	FONT = pygame.font.SysFont("comicsans", 25, True)
	
	def __init__(self):
		self.fart_events: [FartEvent]
		self._load_pressing_times()  # the times at which the player must press SPACE to Fart
		self.angle = 90
		self.angular_speed_deduction = -50  # degrees/second
		self.time_elapsed = 0
		self.pointer_length = 90
		self.pointer_head_coo = (0, 0)
		self.pointer_color = (0, 0, 0)
		
		self.gas_available = 210
		self.gas_cost_for_fart_boost = 1
		self.main_character_is_alive = lambda: self.gas_available > 0
		self.frequency = 1
		
		self.frequency_value_image: pygame.Surface
		self._update_frequency_value_image()
		# self.fart_events = self.fart_events[:96]
	
	def _update_frequency_value_image(self):
		self.frequency_value_image = self.FONT.render(f"{self.FREQUENCIES_LEVEL[self.frequency]}", True, (0, 255, 255))
		self.frequency_value_coo = (660-self.frequency_value_image.get_size()[0]//2, 460)
	
	def _update_pointer_head_coo(self):
		# Calculate the end point of the line based on the angle and length
		angle_radians = math.radians(self.angle)
		x = self.POINTER_COO[0] + self.pointer_length * math.cos(angle_radians)
		y = self.POINTER_COO[1] - self.pointer_length * math.sin(angle_radians)
		self.pointer_head_coo = (x, y)  # Subtract sin for Y-axis inversion
	
	def _load_pressing_times(self):
		self.fart_events = []
		with open("assets/Data/PressingFrequencyData.txt", "r") as file:
			for specs_line in file:
				pass
		
	def _change_frequency(self):
		if random.choices([1, 0], self.FREQUENCY_CHANGE_PROBABILITIES)[0]:
			self.frequency = random.choice(self.FREQUENCIES)
			self._update_frequency_value_image()
	
	def _play_fart_sound(self):
		if 100 >= self.angle >= 70:
			self.GOOD_FART_SOUND.play()
		else:
			self.BAD_FART_SOUND.play()
	
	def react_to_farting(self):
		self.gas_available -= self.gas_cost_for_fart_boost
		self._increase_angle()
		self._play_fart_sound()
	
	def _increase_angle(self):
		self.angle += self.angular_speed_deduction*0.3  # self.get_correct_speed_coefficient()
		
	def _decrease_gas_available(self, dt):
		angle_sin = math.sin(math.radians(self.angle))
		if angle_sin > 0.9659258262890683:
			self.gas_available -= self.GOOD_PENALTY*dt*(1/self.frequency)
		elif 0.6946583704589971 < angle_sin <= 0.9659258262890683:
			self.gas_available -= self.SEMI_BAD_PENALTY*dt*(1/self.frequency)
		elif angle_sin >= 0.258819045102521:
			self.gas_available -= self.BAD_PENALTY*dt*(1/self.frequency)
		else:
			self.gas_available -= self.SUPER_BAD_PENALTY*dt*(1/self.frequency)
	
	def update(self, dt: int):
		self.angle = min(180,  max((self.angle - self.angular_speed_deduction*(1/self.frequency)*dt, 0)))
		self._decrease_gas_available(dt)
		self._update_pointer_head_coo()
		self._change_frequency()
	
	def draw_pointer(self, screen):
		# draw the meter's pointer
		pygame.draw.line(screen, self.pointer_color, self.POINTER_COO, self.pointer_head_coo, 2)
		screen.blit(self.frequency_value_image, (700, 700))
	
	def draw(self, screen):
		# the laughing gas bar
		pygame.draw.rect(screen, (89, 233, 74), (547, 58, self.gas_available, 92))
		screen.blit(self.frequency_value_image, self.frequency_value_coo)
		# [event.draw(screen) for event in self.fart_events if event.is_inside_screen()]
