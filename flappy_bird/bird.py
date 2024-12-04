import pygame
from constants import *


class Bird(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        base_surf = pygame.image.load('assets/bird.png').convert_alpha()
        self.__right_surf = pygame.transform.scale_by(base_surf, 0.1)
        self.__up_surf = pygame.transform.rotate(self.__right_surf, 45)
        self.__down_surf = pygame.transform.rotate(self.__right_surf, -45)

        self.image = self.__right_surf
        self.rect = self.image.get_rect(center=(int(WIDTH * 0.25), HEIGHT//2))

        self.__velocity = 0
        self.__pressed = False


    def process_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.__pressed:
                self.__velocity = -JUMP_SPEED
                self.__pressed = True
        else:
            self.__pressed = False


    def move(self) -> None:
        self.__velocity += GRAVITY
        self.rect.y += self.__velocity
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.__velocity = 0


    def animate(self) -> None:
        cx,cy = self.rect.center
        if self.__velocity < -5:
            self.image = self.__up_surf
        elif self.__velocity > 5:
             self.image = self.__down_surf
        else:
            self.image = self.__right_surf
        self.rect = self.image.get_rect(center=(cx,cy))


    def update(self) -> None:
        self.process_input()
        self.move()
        self.animate()