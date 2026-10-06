import pygame
import sys


# Initialize Pygame
pygame.init()


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
PLAYER_COLOR = (0, 255, 0)
INVADER_COLOR = (255, 0, 0)
BULLET_COLOR = (255, 255, 255)
ENEMY_BULLET_COLOR = (255, 165, 0)  # Orange
FPS = 60


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders Clone")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((64, 16))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5
player_group = pygame.sprite.GroupSingle(Player())

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((8, 16))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.speed = -8

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, invader_rect):
        super().__init__()
        self.image = pygame.Surface((4, 8))
        self.image.fill(ENEMY_BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.midtop = invader_rect.midbottom
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


bullet_group = pygame.sprite.Group()

enemy_bullet_group = pygame.sprite.Group()  # New group for enemy bullets


def setup_invaders():
    invaders = []
    for row in range(8):
        for col in range(5):
            x = (col * (64 + 10)) + 25
            y = 10 + (row * (32 + 10))
            invader = pygame.Rect(x, y, 64, 32)
            invaders.append(invader)
    return invaders


invaders_list = setup_invaders()

score = 0
font = pygame.font.SysFont(None, 36)  # Corrected line


def main():
    global score, invaders_list

    running = True
    clock = pygame.time.Clock()
    direction_x = -1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not bullet_group.sprites():
                    new_bullet = Bullet()
                    new_bullet.rect.centerx = player_group.sprite.rect.centerx
                    new_bullet.rect.bottom = player_group.sprite.rect.top
                    bullet_group.add(new_bullet)

        screen.fill((0, 0, 0))

        player_group.update()
        player_group.draw(screen)

        # Move invaders as a group
        for invader in invaders_list:
            invader.x += direction_x * 2

        # Edge detection — use the whole list, which now may shrink
        if invaders_list:
            leftmost = min(i.left for i in invaders_list)
            rightmost = max(i.right for i in invaders_list)
            if leftmost <= 0 or rightmost >= SCREEN_WIDTH:
                direction_x *= -1
                for invader in invaders_list:
                    invader.y += 32 + 10

        # Bullet-vs-invader collision. Iterate over a copy so we can remove safely.
        if bullet_group.sprites():
            bullet = bullet_group.sprites()[0]
            hit_index = None
            for i, invader in enumerate(invaders_list):
                if bullet.rect.colliderect(invader):
                    hit_index = i
                    break
            if hit_index is not None:
                invaders_list.pop(hit_index)
                bullet.kill()
                score += 10

        # Draw invaders
        for invader in invaders_list:
            pygame.draw.rect(screen, INVADER_COLOR, invader)

        # Update and draw bullets
        bullet_group.update()
        bullet_group.draw(screen)

        enemy_bullet_group.update()  # New line to update enemy bullets
        enemy_bullet_group.draw(screen)  # New line to draw enemy bullets

        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    
    main()
