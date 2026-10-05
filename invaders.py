import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_COLOR = (0, 255, 0)  # Green color for the player ship
FPS = 60  # Frames per second to control the game speed

# Create the screen and set the caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ZX80 Space Invaders Clone")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((64, 16))  # Simple rectangle for the player ship
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2  # Center the player horizontally
        self.rect.bottom = SCREEN_HEIGHT - 20  # Position slightly above the bottom

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5  # Move left by 5 pixels
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5  # Move right by 5 pixels

# Set up the player sprite group
player_group = pygame.sprite.GroupSingle(Player())

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen with black color
        screen.fill((0, 0, 0))  # Black background

        # Update and draw sprites
        player_group.update()
        player_group.draw(screen)

        # Draw everything to the screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
