import pygame

import config
from game_state import GameState


class ProfPickMonsterEvent:
    def __init__(self, screen, game, player):
        self.screen = screen
        self.game = game
        self.prof_image = pygame.image.load("imgs/prof.png")
        self.dialog = pygame.image.load("imgs/dialog.png")

        self.cut = 0
        self.max_cut = 2

    def load(self):
        pass

    def render(self):
        if self.cut == 0:
            self.render_scene_0()
        elif self.cut == 1:
            self.render_scene_1()
        elif self.cut == 2:
            self.render_scene_2()

    def render_scene_0(self):
        self.screen.blit(self.dialog, (0, 300))
        font = pygame.font.Font('fonts/PokemonGb.ttf', 20)
        img = font.render("hello, I am the prof", True, config.BLACK)
        self.screen.blit(img, (40, 400))
        pass

    def render_scene_1(self):
        self.screen.blit(self.dialog, (0, 300))
        font = pygame.font.Font('fonts/PokemonGb.ttf', 20)
        img = font.render("pick your pokemon!", True, config.BLACK)
        self.screen.blit(img, (40, 400))
        pass

    def render_scene_2(self):
        self.screen.blit(self.dialog, (0, 300))
        font = pygame.font.Font('fonts/PokemonGb.ttf', 20)
        img = font.render("chose wisely...!", True, config.BLACK)
        self.screen.blit(img, (40, 400))
        pass

    def update(self):
        if self.cut > self.max_cut:
            self.game.event = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.game_state = GameState.ENDED
            #     handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = GameState.ENDED
                if event.key == pygame.K_RETURN:
                    self.cut = self.cut + 1
