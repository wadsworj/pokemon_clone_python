import pygame
import config

class Building:
    def __init__(self, image_name, position, size):
        print("npc created")
        self.position = position[:]
        self.size = size[:]
        self.image = pygame.image.load("imgs/rooms/" + str(image_name) + ".png")
        self.image = pygame.transform.scale(self.image, (self.size[0] * config.SCALE, self.size[1] * config.SCALE))

    def update(self):
        pass

    def render(self, screen, camera):
        self.rect = pygame.Rect(self.position[0] * config.SCALE - (camera[0] * config.SCALE), self.position[1] * config.SCALE - (camera[1] * config.SCALE), config.SCALE, config.SCALE)
        screen.blit(self.image, self.rect)
