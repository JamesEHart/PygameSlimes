import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 900
BACKGROUND_COLOR = (30, 30, 30)
SLIME_COLOR = (0, 255, 0)
SLIME_RADIUS = 5
JUMP_STRENGTH_Y = 100
MIN_JUMP_STRENGTH_Y = 50
JUMP_STRENGTH_X = 50
MIN_JUMP_STRENGTH_X = -50
GRAVITY = 1
NUM_SLIMES = 10000

# Slime class
class Slime:
    def __init__(self):
        self.x = random.randint(SLIME_RADIUS, WIDTH - SLIME_RADIUS)
        self.y = random.randint(SLIME_RADIUS, HEIGHT - SLIME_RADIUS)
        self.vx = random.uniform(MIN_JUMP_STRENGTH_X, JUMP_STRENGTH_X)
        self.vy = random.uniform(MIN_JUMP_STRENGTH_Y, JUMP_STRENGTH_Y)
    
    def move(self):
        self.vy += GRAVITY  # Apply gravity
        self.x += self.vx
        self.y += self.vy
        
        # Collision with walls (hard borders)
        if self.x - SLIME_RADIUS <= 0:
            self.x = SLIME_RADIUS
            self.vx *= -1
        if self.x + SLIME_RADIUS >= WIDTH:
            self.x = WIDTH - SLIME_RADIUS
            self.vx *= -1
        if self.y - SLIME_RADIUS <= 0:
            self.y = SLIME_RADIUS
            self.vy *= -1
        if self.y + SLIME_RADIUS >= HEIGHT:
            self.y = HEIGHT - SLIME_RADIUS
            self.vy *= -0.8  # Bounce effect
            if abs(self.vy) < 1:
                self.vy = random.uniform(-JUMP_STRENGTH_X, -JUMP_STRENGTH_Y / 2)  # Randomize jump
    
    def draw(self, screen):
        pygame.draw.circle(screen, SLIME_COLOR, (int(self.x), int(self.y)), SLIME_RADIUS)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime Jump Simulator")
clock = pygame.time.Clock()

# Create slimes
slimes = [Slime() for _ in range(NUM_SLIMES)]

# Main loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for slime in slimes:
        slime.move()
        slime.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()