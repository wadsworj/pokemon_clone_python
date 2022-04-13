import pygame

import config
from game_state import GameState
from monsterfactory import MonsterFactory


class PickMonsterEvent:
    def __init__(self, screen, game, player, monster):
        self.screen = screen
        self.game = game
        self.player = player
        self.dialog = pygame.image.load("imgs/dialog.png")
        self.monster_factory = MonsterFactory()

        if monster.name == "monster_cage_starter_01":
            self.monster = self.monster_factory.create_monster_index(1)
        elif monster.name == "monster_cage_starter_02":
            self.monster = self.monster_factory.create_monster_index(4)
        elif monster.name == "monster_cage_starter_03":
            self.monster = self.monster_factory.create_monster_index(7)

        self.cut = 0
        self.max_cut = 0

    def load(self):
        pass

    def render(self):
        if self.cut == 0:
            self.render_scene_0()

    def render_scene_0(self):
        self.screen.blit(self.dialog, (0, 300))
        self.screen.blit(self.monster.image, (100, 100))
        font = pygame.font.Font('fonts/PokemonGb.ttf', 20)
        img = font.render("you picked.... " + str(self.monster.name), True, config.BLACK)
        self.screen.blit(img, (40, 350))
        img = font.render("are you sure? (y/n)", True, config.BLACK)
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
                elif event.key == pygame.K_y:
                    self.player.monsters.append(self.monster)
                    self.game.event = None
                elif event.key == pygame.K_n:
                    self.game.event = None

                # if event.key == pygame.K_RETURN:
                #     self.cut = self.cut + 1
