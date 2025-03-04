import pygame
import random
import sys
import time

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Pop Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load balloon image
BALLOON_IMAGE = pygame.image.load("balloon.png")
BALLOON_IMAGE = pygame.transform.scale(BALLOON_IMAGE, (60, 80))

# Load sounds
pygame.mixer.music.load("background.mp3")  # Background music
pygame.mixer.music.play(-1)  # Loop forever
pop_sound = pygame.mixer.Sound("pop.wav")  # Pop sound

# Balloon settings
BALLOON_RADIUS = 30
FONT = pygame.font.SysFont(None, 48)

# Timer
GAME_DURATION = 60
start_time = time.time()

# Score
score = 0

# Balloon class
class Balloon:
    def __init__(self):
        self.x = random.randint(BALLOON_RADIUS, WIDTH - BALLOON_RADIUS)
        self.y = HEIGHT + random.randint(0, 300)
        self.speed = random.randint(2, 5)

    def move(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(BALLOON_IMAGE, (self.x - 30, self.y - 40))

# Create balloons
balloons = [Balloon() for _ in range(5)]

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    elapsed_time = time.time() - start_time
    remaining_time = max(0, GAME_DURATION - int(elapsed_time))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for balloon in balloons[:]:
                distance = ((balloon.x - mouse_x) ** 2 + (balloon.y - mouse_y) ** 2) ** 0.5
                if distance <= BALLOON_RADIUS:
                    balloons.remove(balloon)
                    balloons.append(Balloon())
                    score += 10
                    pop_sound.play()  # Play pop sound

    for balloon in balloons:
        balloon.move()
        if balloon.y + BALLOON_RADIUS < 0:
            balloons.remove(balloon)
            balloons.append(Balloon())
        balloon.draw()

    # Draw score and timer
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    timer_text = FONT.render(f"Time: {remaining_time}s", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (10, 60))

    pygame.display.flip()

    if remaining_time <= 0:
        running = False

# Stop background music
pygame.mixer.music.stop()

# Game Over screen
screen.fill(WHITE)
game_over_text = FONT.render(f"Game Over!", True, BLACK)
final_score_text = FONT.render(f"Your Score: {score}", True, BLACK)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - 120, HEIGHT // 2 + 10))
pygame.display.flip()

pygame.time.wait(5000)
pygame.quit()
sys.exit()
