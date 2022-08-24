import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        # general setup
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            # print('up')
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            # print('down')
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            # print('left')
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            # print('right')
            self.direction.x = 1
        else:
            self.direction.x = 0

        # print(self.direction)

    def move(self, dt):

        # normalize a vector : 대각으로 이동할때 2 ** 1/2의 힘으로 이동하는 것을 제한
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        # print(self.direction)

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)