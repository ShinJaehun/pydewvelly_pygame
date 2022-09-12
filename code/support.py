from os import walk, listdir
import pygame

def import_folder(path):
    surface_list = []
    # stackoverflow에서 알아낸 건데... walk()는 파일 순서가 정렬되는 것을 보장할 수 없음
    # 그래서 walk() 대신 sorted(listdir(path))를 사용하라고 함...
    # for _, __, img_files in walk(path):
    #     for image in img_files:
    #         full_path = path + '/' + image
    #         print(full_path)
    #         image_surf = pygame.image.load(full_path).convert_alpha()
    #         surface_list.append(image_surf)
    # return surface_list
    for img_file in sorted(listdir(path)):
        full_path = path + '/' + img_file
        image_surf = pygame.image.load(full_path).convert_alpha()
        surface_list.append(image_surf)
    return surface_list

def import_folder_dict(path):
    surface_dict = {}
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf
    return surface_dict