import pygame
import pymunk
import pymunk.pygame_util

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Initialize pymunk space
space = pymunk.Space()
space.gravity = (0, 900)

# Create static walls
def create_wall(p1, p2):
    wall = pymunk.Segment(space.static_body, p1, p2, 5)
    wall.elasticity = 0.9
    wall.friction = 0.5
    space.add(wall)

create_wall((0, HEIGHT), (WIDTH, HEIGHT))  # Floor
create_wall((0, 0), (0, HEIGHT))           # Left wall
create_wall((WIDTH, 0), (WIDTH, HEIGHT))   # Right wall

def add_marble(pos, radius=15):
    body = pymunk.Body(mass=1, moment=pymunk.moment_for_circle(1, 0, radius))
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = marble_elasticity
    shape.friction = marble_friction
    space.add(body, shape)
    marbles.append((body, shape))

# Barrier and marble lists
dragging = False
start_pos = None
barrier_friction = 0.5
barrier_elasticity = 0.9
marble_friction = 0.5
marble_elasticity = 0.8
barriers = []
marbles = []

def add_barrier(p1, p2):
    barrier = pymunk.Segment(space.static_body, p1, p2, 5)
    barrier.elasticity = barrier_elasticity
    barrier.friction = barrier_friction
    space.add(barrier)
    barriers.append(barrier)

# Slider properties
slider_friction = pygame.Rect(650, 50, 100, 10)
slider_elasticity = pygame.Rect(650, 100, 100, 10)
slider_marble_friction = pygame.Rect(650, 150, 100, 10)
slider_marble_elasticity = pygame.Rect(650, 200, 100, 10)
handle_friction = pygame.Rect(650 + barrier_friction * 100, 45, 10, 20)
handle_elasticity = pygame.Rect(650 + barrier_elasticity * 100, 95, 10, 20)
handle_marble_friction = pygame.Rect(650 + marble_friction * 100, 145, 10, 20)
handle_marble_elasticity = pygame.Rect(650 + marble_elasticity * 100, 195, 10, 20)
sliding_friction = False
sliding_elasticity = False
sliding_marble_friction = False
sliding_marble_elasticity = False

def draw_slider(slider, handle, label, value):
    pygame.draw.rect(screen, (100, 100, 100), slider)
    pygame.draw.rect(screen, (200, 200, 200), handle)
    font = pygame.font.Font(None, 24)
    text = font.render(f"{label}: {value:.2f}", True, (255, 255, 255))
    screen.blit(text, (slider.x, slider.y - 20))

def main():
    global dragging, start_pos, barrier_friction, barrier_elasticity, marble_friction, marble_elasticity
    global sliding_friction, sliding_elasticity, sliding_marble_friction, sliding_marble_elasticity
    running = True
    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if handle_friction.collidepoint(event.pos):
                    sliding_friction = True
                elif handle_elasticity.collidepoint(event.pos):
                    sliding_elasticity = True
                elif handle_marble_friction.collidepoint(event.pos):
                    sliding_marble_friction = True
                elif handle_marble_elasticity.collidepoint(event.pos):
                    sliding_marble_elasticity = True
                else:
                    start_pos = event.pos
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    add_barrier(start_pos, event.pos)
                    dragging = False
                sliding_friction = False
                sliding_elasticity = False
                sliding_marble_friction = False
                sliding_marble_elasticity = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    end_pos = event.pos
                    pygame.draw.line(screen, (200, 200, 200), start_pos, end_pos, 5)
                elif sliding_friction:
                    handle_friction.x = max(slider_friction.x, min(event.pos[0], slider_friction.x + 100))
                    barrier_friction = (handle_friction.x - slider_friction.x) / 100
                elif sliding_elasticity:
                    handle_elasticity.x = max(slider_elasticity.x, min(event.pos[0], slider_elasticity.x + 100))
                    barrier_elasticity = (handle_elasticity.x - slider_elasticity.x) / 100
                elif sliding_marble_friction:
                    handle_marble_friction.x = max(slider_marble_friction.x, min(event.pos[0], slider_marble_friction.x + 100))
                    marble_friction = (handle_marble_friction.x - slider_marble_friction.x) / 100
                elif sliding_marble_elasticity:
                    handle_marble_elasticity.x = max(slider_marble_elasticity.x, min(event.pos[0], slider_marble_elasticity.x + 100))
                    marble_elasticity = (handle_marble_elasticity.x - slider_marble_elasticity.x) / 100
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    add_marble(pygame.mouse.get_pos())
                elif event.key == pygame.K_c:
                    for body, shape in marbles:
                        space.remove(body, shape)
                    marbles.clear()
                    for barrier in barriers:
                        space.remove(barrier)
                    barriers.clear()
        
        # Update handle positions
        handle_friction.x = slider_friction.x + int(barrier_friction * 100)
        handle_elasticity.x = slider_elasticity.x + int(barrier_elasticity * 100)
        handle_marble_friction.x = slider_marble_friction.x + int(marble_friction * 100)
        handle_marble_elasticity.x = slider_marble_elasticity.x + int(marble_elasticity * 100)
        
        # Draw sliders
        draw_slider(slider_friction, handle_friction, "Barrier Friction", barrier_friction)
        draw_slider(slider_elasticity, handle_elasticity, "Barrier Elasticity", barrier_elasticity)
        draw_slider(slider_marble_friction, handle_marble_friction, "Marble Friction", marble_friction)
        draw_slider(slider_marble_elasticity, handle_marble_elasticity, "Marble Elasticity", marble_elasticity)
        
        space.step(1/60)  # Physics step
        space.debug_draw(draw_options)  # Draw physics bodies
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()