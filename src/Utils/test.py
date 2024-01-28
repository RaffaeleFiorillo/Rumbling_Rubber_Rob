import pygame

# Initialize pygame
pygame.init()

# Set the screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spacebar Sound Recorder")

# Load sound
sound_file = "../../assets/Sounds/videoplayback.mp3"
music = pygame.mixer.Sound(sound_file)

# Colors
WHITE = (255, 255, 255)


# Main function
def main():
    running = True
    space_pressed_times = []
    
    # Record the start time of the game
    start_time = 0
    clock = pygame.time.Clock()
    pygame.time.wait(2000)
    music.play()
    
    with open("spacebar_presses.txt", "w") as file:
        while running:
            dt = clock.tick(30) / 1000.0  # Cap the frame rate at 30 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Record the time when spacebar is pressed
                    start_time = pygame.time.get_ticks()
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    # Calculate how long the spacebar was pressed
                    press_duration = pygame.time.get_ticks() - start_time
                    # Write the data to a text file
                    file.write(f"Pressed Time: {start_time}, Press Duration: {press_duration}\n")
    
    pygame.quit()


if __name__ == "__main__":
    main()
    
    

if __name__ == "__main__":
    main()