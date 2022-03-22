import pygame

class Monster:
    def __init__(self, monster_type, id):
        print("player created")
        self.type = monster_type
        self.health = 10
        self.attack = 10
        self.id = id
        self.image = pygame.image.load("imgs/monsters/" + f"{self.id:03d}" + ".png")