import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import *

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
        tmx_data = load_pygame('data/map.tmx')

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # fence
        for x, y, surf, in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # water
        water_frames = import_folder('graphics/water')
        for x, y, surf, in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, self.all_sprites, obj.name)

        # wildflowers
        # for x, y, surf, in tmx_data.get_layer_by_name('Decoration').tiles():
        #     Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
        # 얘네는 이렇게 할 필요가 없다는 거지?
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, self.all_sprites)

        self.player = Player((400, 300), self.all_sprites) 
        Generic(
            pos = (0, 0),
            surf = pygame.image.load('graphics/world/ground.png').convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS['ground']
        )
        # self.player = Player((640, 360), self.all_sprites) # 1280 * 720에서...
        # self.player = Player((400, 300), self.all_sprites)
        # 이게 generic 뒤에 있으면 가려서 안 보임...ㅠㅠ 근데 LAYERS 값을 이용해서 레이어를 적용하면 순서 상관 없음

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
            # for sprite in self.sprites(): # 근데 이거 sprites()는 어디서 온거야?
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): 
                # 이렇게 정렬해주면 object보다 player.y가 위에 있을 때 object 뒤에 player가,
                # object보다 player.y가 아래에 있을 때 object 앞에 player가 오게 된다!
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    # self.display_surface.blit(sprite.image, sprite.rect)
                    self.display_surface.blit(sprite.image, offset_rect)