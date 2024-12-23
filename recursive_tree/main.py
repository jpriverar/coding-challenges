import pygame
import math
import random


def draw_tree(pos, angle, size):
    if size < 10: return

    # Draw this branch
    end_x = pos[0] + size * math.cos(angle)
    end_y = pos[1] + size * math.sin(angle) 
    pygame.draw.line(screen, 'white', pos, (end_x, end_y))

    # Draw the subtrees
    subtree_count = random.randint(MIN_BRANCHING_FACTOR, MAX_BRANCHING_FACTOR)
    for _ in range(subtree_count):
        angle_offset = math.radians(random.randint(MIN_ANGLE_OFFSET, MAX_ANGLE_OFFSET))
        size_decay = random.uniform(MIN_SIZE_DECAY, MAX_SIZE_DECAY)
        draw_tree((end_x, end_y), angle + angle_offset, size * size_decay)


WIDTH, HEIGHT = 600, 600
MIN_BRANCHING_FACTOR = 3
MAX_BRANCHING_FACTOR = 5
MIN_ANGLE_OFFSET = -45
MAX_ANGLE_OFFSET = 45
MIN_SIZE_DECAY = 0.3 
MAX_SIZE_DECAY = 0.9

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

draw_tree((WIDTH//2, HEIGHT), 3*math.pi/2, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    pygame.display.update()

pygame.quit()