import pygame
import sys
from src.Utils.GAME_conf import SCREEN, WIDTH, HEIGHT, COLOR as S_COLOR
from src import GameEntities


class Base_Game:
	HUD_COVER = pygame.image.load("assets/Images/Others/background.png").convert_alpha()
	BACKGROUND_MUSIC = pygame.mixer.Sound("assets/Sounds/background_music.mp3")
	GAME_OVER_SOUND = pygame.mixer.Sound("assets/Sounds/game over.mp3")
	TUTORIAL_IMAGE = pygame.image.load("assets/Images/Others/tutorial.png").convert_alpha()
	GOAL_IMAGE = pygame.image.load("assets/Images/Others/goal.png").convert_alpha()
	FONT = pygame.font.SysFont("killer", 60)
	GAME_OVER_TEXT = FONT.render("The World Needs To Laugh More!", 1, (255, 0, 0))
	# GAME_OVER_IMAGE = pygame.image.load("")

	def __init__(self):
		self.game_over_message = "The game reached an End"
		
		# self.background_image = BACKGROUND_IMAGE
		self.screen = SCREEN
		
		self.main_character = GameEntities.FartingBalloon()
		self.fart_event_manager = GameEntities.FartEventManager()
		self.cloud_manager = GameEntities.CloudManager()
		# self.meme_manager = MainCharacter.EnemyManager()
		
		self.key_is_pressed_in_x = False
		self.key_is_pressed_in_y = False
		
		self.clock = pygame.time.Clock()
		self.dt = 0  # delta time: time between frames expressed in milliseconds
		self.is_running = True
	
	def start(self):
		self.tutorial_loop()
		self.game_loop()
	
	# ------------------------ Managements --------------------------------
	def player_input_management(self, event):
		# Check if the player presses or releases a button
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			pressed_keys = pygame.key.get_pressed()
			
			# Update the speed based on the currently pressed keys
			self.main_character.change_speed_x(pressed_keys[pygame.K_RIGHT] - pressed_keys[pygame.K_LEFT])
			
			if pressed_keys[pygame.K_SPACE]:
				self.main_character.change_speed_y(0.5)
				self.fart_event_manager.react_to_farting()
		
	def manage_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			self.player_input_management(event)
	
	def manage_collisions(self):
		# meme collisions
		# for meme in self.meme_manager.memes:
			# self.main_character.is_colliding_with_enemy(meme.hitbox)
		pass
	
	def tutorial_loop(self):
		self.BACKGROUND_MUSIC.play(1)
		self.screen.blit(self.GOAL_IMAGE, (0, 0))
		pygame.display.update()
		page_number = 1
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if page_number == 1:
						page_number = 2
						self.screen.blit(self.TUTORIAL_IMAGE, (0, 0))
						pygame.display.update()
					else:
						return None
			self.clock.tick(60)
			
	# ------------------------ Game Loop --------------------------------------
	def update(self):
		self.main_character.update(self.dt)
		self.fart_event_manager.update(self.dt)
		# self.meme_manager.update(self.dt)
		if self.main_character.y <= HEIGHT // 2:
			self.cloud_manager.update(self.dt*self.main_character.speed[1])
		
	def draw(self):
		self.screen.fill(S_COLOR)
		self.cloud_manager.draw_clouds_behind_character(self.screen)
		self.main_character.draw(self.screen)
		self.cloud_manager.draw_clouds_in_front_of_character(self.screen)
		# self.meme_manager.draw_memes(self.screen)
		self.main_character.draw_stats(self.screen)
		self.fart_event_manager.draw(self.screen)
		self.screen.blit(self.HUD_COVER, (0, 0))
		self.fart_event_manager.draw_pointer(self.screen)
		pygame.display.update()
	
	def game_loop(self):
		self.BACKGROUND_MUSIC.play(1)
		while self.fart_event_manager.main_character_is_alive():
			self.manage_input()
			self.manage_collisions()
			
			self.update()
			self.draw()
			self.dt = self.clock.tick(60) / 1000  # updating delta time
		
		self.game_over()
	
	def game_over(self):
		self.GAME_OVER_SOUND.play()
		self.screen.fill((0, 0, 0))
		self.screen.blit(self.GAME_OVER_TEXT, (100, 300))
		# self.screen.blit(self.GAME_OVER_IMAGE, (0, 0))
		pygame.display.update()
		
		for i in range(200):
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
		
		pygame.quit()
		sys.exit()
