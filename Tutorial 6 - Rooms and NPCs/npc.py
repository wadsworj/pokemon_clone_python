import pygame
import config

class Npc:
    def __init__(self, name, image, x_postition, y_position):
        print("npc created")
        self.name = name
        self.position = [x_postition, y_position]
        self.image = pygame.image.load("imgs/" + str(image) + ".png")
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)
        self.monster = None
        self.monsters = []

    def update(self):
        print("npc updated")

    def update_position(self, new_position):
        self.position[0] = new_position[0]
        self.position[1] = new_position[1]


    def render(self, screen, camera):
        self.rect = pygame.Rect(self.position[0] * config.SCALE - (camera[0] * config.SCALE), self.position[1] * config.SCALE - (camera[1] * config.SCALE), config.SCALE, config.SCALE)
        screen.blit(self.image, self.rect)
