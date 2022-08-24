from os import walk
import pygame

def import_folder(path):
    # print(path)
    surface_list = []
    # for folder in walk(path):
    #     print(folder)
    for _, _, img_files in walk(path):
        # print(img_files)
        for image in img_files:
            # print(image)
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list