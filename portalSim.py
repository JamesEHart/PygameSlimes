import pygame
import pymunk
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BALL_RADIUS = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Portal Physics Sim")

space = pymunk.Space()
space.gravity = (0, 980)

def create_wall(start, end):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, start, end, 5)
    shape.elasticity = 0.8
    space.add(body, shape)

# Add walls
create_wall((0, 0), (0, HEIGHT))  # Left
create_wall((0, HEIGHT), (WIDTH, HEIGHT))  # Bottom
create_wall((WIDTH, HEIGHT), (WIDTH, 0))  # Right
create_wall((WIDTH, 0), (0, 0))  # Top

# Ball setup
def create_ball(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BALL_RADIUS))
    body.position = x, y
    shape = pymunk.Circle(body, BALL_RADIUS)
    shape.elasticity = 0.8
    space.add(body, shape)
    return body

ball = create_ball(WIDTH // 2, HEIGHT // 2)

# Portals
portal_entrance = None
portal_exit = None

def create_portal(x, y, is_entrance=True):
    global portal_entrance, portal_exit
    if is_entrance:
        portal_entrance = (x, y)
    else:
        portal_exit = (x, y)

def check_portal_teleport():
    if portal_entrance and portal_exit:
        bx, by = ball.position
        ex, ey = portal_entrance
        if (bx - ex) ** 2 + (by - ey) ** 2 < BALL_RADIUS ** 2:
            ball.position = portal_exit
            return True
    return False

# Ball dragging
dragging = False

def handle_mouse_down(pos):
    global dragging
    bx, by = ball.position
    if (bx - pos[0]) ** 2 + (by - pos[1]) ** 2 < BALL_RADIUS ** 2:
        dragging = True

def handle_mouse_up():
    global dragging
    dragging = False

def handle_mouse_motion(pos):
    if dragging:
        ball.position = pos

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                create_portal(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], is_entrance=True)
            elif event.key == pygame.K_t:
                create_portal(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], is_entrance=False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_up()
        elif event.type == pygame.MOUSEMOTION:
            handle_mouse_motion(event.pos)
    
    check_portal_teleport()
    if not dragging:
        space.step(1 / 60)
    
    pygame.draw.circle(screen, BLUE, (int(ball.position.x), int(ball.position.y)), BALL_RADIUS)
    
    if portal_entrance:
        pygame.draw.circle(screen, ORANGE, portal_entrance, 10)
    if portal_exit:
        pygame.draw.circle(screen, BLUE, portal_exit, 10)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()