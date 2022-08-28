import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        # self.all_sprites = pygame.sprite.Group()
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        Generic(
            pos = (0, 0),
            surf = pygame.image.load('graphics/world/ground.png').convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS['ground']
        )
        # self.player = Player((640, 360), self.all_sprites) # 1280 * 720에서...
        self.player = Player((400, 300), self.all_sprites) # 이게 generic 뒤에 있으면 가려서 안 보임...ㅠㅠ


    def run(self, dt):
        self.display_surface.fill('black')
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.customize_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2 
        for layer in LAYERS.values():
            for sprite in self.sprites(): # 근데 이거 sprites()는 어디서 온거야?
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    # self.display_surface.blit(sprite.image, sprite.rect)
                    self.display_surface.blit(sprite.image, offset_rect)