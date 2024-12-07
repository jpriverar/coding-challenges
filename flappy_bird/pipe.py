import pygame
from constants import *


class Pipe(pygame.sprite.Sprite):
    UP = 1
    DOWN = 2

    @staticmethod
    def get_pipes(height: int, space: int):
        up_pipe = Pipe(height, dir=Pipe.UP)
        down_pipe = Pipe(up_pipe.rect.bottom + space, dir=Pipe.DOWN)
        return up_pipe, down_pipe


    def __init__(self, height: int, dir: int) -> None:
        super().__init__()

        base_image = pygame.image.load('assets/pipe.png').convert_alpha()
        base_image = pygame.transform.scale_by(base_image, (0.4, 0.5))
        if dir == Pipe.DOWN:
            base_image = pygame.transform.rotate(base_image, 180)
        self.image = base_image
        self.mask = pygame.mask.from_surface(self.image)

        self.dir = dir
        if self.dir == Pipe.DOWN:
            self.rect = self.image.get_rect(topleft=(WIDTH, height))
        elif self.dir == Pipe.UP:
            self.rect = self.image.get_rect(bottomleft=(WIDTH, height))


    def move(self) -> None:
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

    
    def update(self) -> None:
        self.move()