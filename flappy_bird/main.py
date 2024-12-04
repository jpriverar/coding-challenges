import pygame
from random import randint
from constants import *
from bird import Bird
from pipe import Pipe


def display_score() -> None:
    score_surf = score_font.render(f'Score: {score}', False, 'white')
    score_rect = score_surf.get_rect(topleft=(0,0))
    screen.blit(score_surf, score_rect)


def check_collision() -> bool:
    # return pygame.sprite.spritecollide(bird, pipe_group, False)
    for pipe in pipe_group.sprites():
        if pygame.sprite.collide_mask(bird, pipe):
            return True
    return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
score = 0

score_font = pygame.font.Font(None, 50)
background_surf = pygame.image.load('assets/backgrounds/forest.png').convert()
background_surf = pygame.transform.scale_by(background_surf, 0.9)
background_rect = background_surf.get_rect(topleft=(0,0))

bird = Bird()
bird_group = pygame.sprite.GroupSingle(bird)

pipe_group = pygame.sprite.Group()
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, PIPE_GENERATION_PERIOD)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pipe_timer:
            height = randint(100, HEIGHT - 300)
            pipes = Pipe.get_pipes(height, PIPE_SPACE)
            pipe_group.add(pipes)

    screen.blit(background_surf, background_rect)
    display_score()

    pipe_group.update()
    pipe_group.draw(screen)

    bird_group.update()
    #pygame.draw.rect(screen, 'blue', bird.rect)
    bird_group.draw(screen)

    if check_collision() or bird.rect.bottom == HEIGHT:
        running = False

    pygame.display.update()
    clock.tick(60)
                 
pygame.quit()