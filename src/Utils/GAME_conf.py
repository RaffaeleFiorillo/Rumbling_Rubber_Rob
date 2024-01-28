import pygame

pygame.init()
GAME_NAME = "Rumbling Rubber Rob - Story of a Balloon who Wanted Everybody to Laugh"
CharacterName = "NICK?"
pygame.display.set_caption(GAME_NAME)

WINDOW_RESOLUTIONS = {
	"normal": (504, 700),
	"4:3": (720, 500)
}

WINDOW_RESOLUTION_TYPE = "normal"
WIDTH, HEIGHT = WINDOW_RESOLUTIONS[WINDOW_RESOLUTION_TYPE]
COLOR = (10, 60, 255)
SCREEN = pygame.display.set_mode((WIDTH+321, HEIGHT))
G_FONT = pygame.font.SysFont("comicsans", 30, True)

# BACKGROUND_IMAGE = pygame.image.load("assets/Images/Others/background.png").convert_alpha()

# Set the window icon
pygame.display.set_icon(pygame.image.load("assets/Images/Others/game-icon.ico"))
