import pygame
import sys


# Initialize Pygame
pygame.init()


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
PLAYER_COLOR = (0, 255, 0)  # Green color for the player ship
INVADER_COLOR = (255, 0, 0)  # Red color for the invaders
FPS = 60  # Frames per second to control the game speed


# Create the screen and set the caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders Clone")


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


def setup_invaders():
    invaders = []
    for row in range(8):
        for col in range(5):
            x = (col * (64 + 10)) + 25  # Spacing between invaders and some padding on the left
            y = -20 + (row * (32 + 10))  # Spacing between rows with some padding at the top
            invader = pygame.Rect(x, y, 64, 32)
            invaders.append(invader)
    return invaders


# Setup the invaders list
invaders_list = setup_invaders()


def main():
    running = True
    clock = pygame.time.Clock()
    direction_x = -1  # Start moving to the left

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen with black color
        screen.fill((0, 0, 0))  # Black background

        # Update and draw sprites
        player_group.update()
        player_group.draw(screen)

        # Move and update invaders
        for invader in invaders_list:
            invader.x += direction_x * 2  # Each invader moves twice as fast as the player

        # Check if any invader has reached an edge to change direction and drop down
        leftmost_invader = min(invaders_list, key=lambda i: i.left)
        rightmost_invader = max(invaders_list, key=lambda i: i.right)

        if leftmost_invader.x <= 0 or rightmost_invader.x >= SCREEN_WIDTH - 64:
            direction_x *= -1
            for invader in invaders_list:
                invader.y += 32 + 10  # Drop down by one row height plus some padding

        # Draw invaders
        for invader in invaders_list:
            pygame.draw.rect(screen, INVADER_COLOR, invader)

        # Draw everything to the screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
