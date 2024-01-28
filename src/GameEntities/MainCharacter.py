import pygame
import threading
import time
from src.Utils.GAME_conf import WIDTH, HEIGHT, G_FONT


class FartingBalloon:
    MAX_X_SPEED = 1000  # maximum speed the character is able to reach in the x-axis: pixels/second
    MAX_Y_SPEED = 2200  # maximum speed the character is able to reach in the y-axis: pixel/second
    Y_SPEED_INCREASE_STEP = 10  # the amount of speed gained each time the player farts
    GRAVITY_ACCELERATION = -2000  # the speed at which vertical speed is lost pixel/second^2
    FART_SPEED_BOOST = 2000  # how much speed the fart provides: pixel/second
    FART_IMAGE = pygame.image.load("assets/Images/Others/fart.png").convert_alpha()
    FART_IMAGE.set_alpha(150)
    IMAGE = pygame.image.load("assets/Images/Main Character/Character2.png").convert_alpha()
    # DEATH_IMAGE = pygame.image.load("assets/Images/Main Character/dead.png").convert_alpha()
    DEATH_SOUND = pygame.mixer.Sound("assets/Sounds/main character death.mp3")
    ACCEPTED_OVERLAP_PERCENTAGE = 0.7
    COOL_DOWN_TIME = 2  # immunity time after an enemy hits you
    FONT = G_FONT
    
    def __init__(self, x=465, y=HEIGHT):
        self.image = self.IMAGE
        self.size = tuple(self.image.get_size())
        self.x = 200
        self.y = y-self.size[1]
        # HUD
        self.distance_traveled = 0  # serves as the game's score in meters
        self.lives = 5  # number of lives. When it reaches 0 it is Game Over
        self.cool_down_timer = 0  # duration of the fart
        self.fart_coo = (0, 0)
        self.has_immunity = lambda: self.cool_down_timer > 0
        # Collision
        self.get_hitbox = lambda: (self.x, self.y, self.size[0], self.size[1])
        self.hitbox = self.get_hitbox()
        # Movement
        self.speed = [0, 0]  # speed vector at which the entity moves in the current frame
    
    # ---------------------------- Collisions Effects ------------------------------------
    def _change_image_cycle(self):
        time.sleep((self.COOL_DOWN_TIME * 0.15))
        self.image = self.IMAGE
        self.IMAGE.set_alpha(100)  # makes the player become translucent
        time.sleep((self.COOL_DOWN_TIME * 0.85))
        self.IMAGE.set_alpha(255)  # makes the player become normal
    
    def _apply_meme_collision_effect(self):
        pass
    
    def _apply_fart_failure_effect(self):
        self.DEATH_SOUND.play()
        # self.image = self.DEATH_IMAGE
        self.lives -= 1
        self.cool_down_timer = self.COOL_DOWN_TIME
        hit_animation_thread = threading.Thread(target=self._change_image_cycle)
        hit_animation_thread.start()
    
    # -------------------------- Collisions Detection -----------------------------------
    def _is_colliding_with_hitbox(self, hitbox):
        # Calculate overlap along the x-axis
        x_overlap = max(0, min(self.hitbox[0] + self.hitbox[2], hitbox[0] + hitbox[2]) - max(self.hitbox[0], hitbox[0]))
        # Calculate overlap along the y-axis
        y_overlap = max(0, min(self.hitbox[1] + self.hitbox[3], hitbox[1] + hitbox[3]) - max(self.hitbox[1], hitbox[1]))
        # Calculate the overlap area
        overlap_area = x_overlap * y_overlap
        # Calculate the area of the main character's hitbox
        character_area = self.hitbox[2] * self.hitbox[3]
        # Calculate the percentage of the main character's hitbox that is inside the object's hitbox
        overlap_percentage = overlap_area / character_area
        
        # Check if the overlap percentage is greater than the threshold
        return overlap_percentage >= self.ACCEPTED_OVERLAP_PERCENTAGE
    
    def is_colliding_with_meme(self, enemy_hitbox: (int, int, int, int)):
        if self._is_colliding_with_hitbox(enemy_hitbox):  # not self.has_immunity() and
            self._apply_meme_collision_effect()
    
    # ------------------------------ Speed Control --------------------------------------
    def change_speed_x(self, direction):
        # direction: 1-> go right; 0-> do nothing; -1-> go left
        self.speed[0] = self.MAX_X_SPEED * direction

    def _update_fart_coo(self):
        self.fart_coo = (self.x+19, self.y+self.size[1])
    
    def change_speed_y(self, button_pressing_imprecision: float):
        # direction: 1-> go down; 0-> do nothing; -1-> go up
        self.speed[1] = self.FART_SPEED_BOOST
        self.cool_down_timer = 0.5
        # self.MAX_Y_SPEED += self.Y_SPEED_INCREASE_STEP
        # self.FART_SPEED_BOOST += self.Y_SPEED_INCREASE_STEP
    
    # ------------------------------ General --------------------------------------------
    def update(self, dt):
        self.speed = [self.speed[0], self.speed[1]]
        self.x += self.speed[0] * dt
        altitude_travelled = self.speed[1] * dt
        self.y -= altitude_travelled
        self.distance_traveled += int(altitude_travelled*((self.y+self.size[1]) <= HEIGHT))
    
        self.speed[1] += self.GRAVITY_ACCELERATION * dt
    
        # Guarantee that an agent does not go outside the screen
        self.x = min(WIDTH - self.size[0], max(0, self.x))
        self.y = min(HEIGHT - self.size[1], max(HEIGHT // 2, self.y))
        self.speed[1] = min(self.MAX_Y_SPEED, self.speed[1])
        # self.hitbox = self.get_hitbox()
        self.cool_down_timer = min(self.COOL_DOWN_TIME, max(0, self.cool_down_timer - 1 * dt))

    def draw_stats(self, screen):
        # the distance traveled
        screen.blit(self.FONT.render(f"{self.distance_traveled/100}m", True, (0, 255, 255)), (645, 170))
    
    def draw(self, screen):
        if self.cool_down_timer > 0:
            self._update_fart_coo()
            pygame.draw.line(screen, (151, 193, 21), (self.fart_coo[0]+10, self.y+self.size[1]),
                             (self.fart_coo[0]+10, self.fart_coo[1]), 10)
            screen.blit(self.FART_IMAGE, self.fart_coo)
        screen.blit(self.image, (self.x, self.y))
