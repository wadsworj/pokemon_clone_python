import pygame
import config
import math
import utilities


class Battle:
    def __init__(self, screen, monster, player):
        self.screen = screen
        self.monster = monster
        self.player = player

    def load(self):
        pass

    def render(self):
        self.screen.fill(config.WHITE)

        #font = pygame.font.SysFont(None, 24)
        font = pygame.font.Font("fonts/PokemonGb.ttf", 16)

        self.screen.blit(battle_images["monster_pad"], (0, 300))
        self.screen.blit(battle_images["name_card"], (310, 300))
        self.screen.blit(battle_images["hp_bar"], (340, 335))


        self.screen.blit(self.player.monsters[0].image, (70, 250))

        self.screen.blit(battle_images["monster_pad"], (300, 100))
        self.screen.blit(battle_images["name_card"], (15, 100))
        self.screen.blit(battle_images["hp_bar"], (50, 135))
        self.screen.blit(battle_images["menu"], (0, 388))

        img = font.render("press enter to attack!", True, config.WHITE)
        self.screen.blit(img, (30, 430))

        self.screen.blit(self.monster.image, (370, 30))

        img = font.render(str(self.monster.name), True,
                          config.BLACK)
        self.screen.blit(img, (25, 110))

        img = font.render("Lv" + str(self.monster.level), True,
                          config.BLACK)
        self.screen.blit(img, (260, 110))


        # draw player's monster name
        img = font.render(str(self.player.monsters[0].name), True,
                          config.BLACK)
        self.screen.blit(img, (323, 311))

        img = font.render("Lv" + str(self.player.monsters[0].level), True,
                          config.BLACK)
        self.screen.blit(img, (555, 311))

        monster_percent = self.monster.health / self.monster.base_health
        monster_color = self.determine_health_color(monster_percent)
        pygame.draw.rect(self.screen, monster_color, pygame.Rect(91, 137, config.BATTLE_HEALTH_BAR_WIDTH * monster_percent, 16))

        player_monster_percent = self.player.monsters[0].health / self.player.monsters[0].base_health
        player_monster_color = self.determine_health_color(player_monster_percent)
        pygame.draw.rect(self.screen, player_monster_color, pygame.Rect(381, 337, config.BATTLE_HEALTH_BAR_WIDTH * player_monster_percent, 16))

        img = font.render("health: " + str(self.monster.health) + " Attack: " + str(self.monster.attack), True, config.BLACK)
        self.screen.blit(img, (25, 155))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.game_state = GameState.ENDED
            #     handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = GameState.ENDED
                if event.key == pygame.K_RETURN:
                    self.monster.health = self.monster.health - 1

    def determine_health_color(self, monster_percent):
        if monster_percent < .25:
            return config.RED
        if monster_percent < .7:
            return config.YELLOW
        return config.GREEN

battle_images = {
    "monster_pad": pygame.transform.scale(pygame.image.load("imgs/battle/monster_pad.png"), (300, 88)),
    "name_card": pygame.transform.scale(pygame.image.load("imgs/battle/name_card.png"), (300, 80)),
    "hp_bar": pygame.transform.scale(pygame.image.load("imgs/battle/hp_bar.png"), (250, 20)),
    "menu": pygame.image.load("imgs/battle/menu.png"),
}
