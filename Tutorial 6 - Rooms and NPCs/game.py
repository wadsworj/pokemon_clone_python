import random

import pygame
import config
import math
import utilities
from events import game_event_handler

from player import Player
from game_state import GameState, CurrentGameState
from monsterfactory import MonsterFactory
from game_view.map import Map
from game_view.battle import Battle

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.game_state = GameState.NONE
        self.current_game_state = CurrentGameState.MAP
        self.player_has_moved = False
        self.monster_factory = MonsterFactory()
        self.map = Map(screen)
        self.maps = [self.map]
        self.battle = None
        self.player = None
        self.event = None

    def set_up(self):
        player = Player(1, 1)
        self.player = player
        print("do set up")
        self.game_state = GameState.RUNNING

        self.map.load("01", self.player)

    def update(self):
        if self.current_game_state == CurrentGameState.MAP:
            self.player_has_moved = False
            self.screen.fill(config.BLACK)
            # print("update")
            self.handle_events()

            if self.player_has_moved:
                self.determine_game_events()

            self.map.render(self.screen, self.player)

        elif self.current_game_state == CurrentGameState.BATTLE:
            self.battle.update()
            self.battle.render()

            if self.battle.monster.health <= 0:
                self.current_game_state = CurrentGameState.MAP

        if self.event is not None:
            self.event.render()
            self.event.update()

    def determine_game_events(self):
        map_tile = self.map.map_array[self.player.position[1]][self.player.position[0]]
        print(map_tile)

        if map_tile == config.MAP_TILE_ROOM_EXIT:
            self.player.position = self.map.player_exit_position[:]
            self.maps.pop()
            self.map = self.maps[-1]
            return

        # if the map tile is a door, we need a room
        if utilities.test_if_int(map_tile):
            room = Map(self.screen)
            room.load_room(self.map.file_name, map_tile, self.player)
            self.map = room
            self.maps.append(room)
            return

        for npc in self.map.objects:
            if npc == self.map.player:
                continue

            if npc.position[:] == self.map.player.position[:]:
                game_event_handler.handle(self, self.player, npc)

        for exit_position in self.map.exit_positions:
            if self.player.position[:] == exit_position['position'][:]:
                map_file = exit_position['map']
                map = Map(self.screen)

                config.MAP_CONFIG[map_file]['start_position'] = exit_position['new_start_position'][:]

                map.load(map_file, self.player)
                self.maps.pop()
                self.map = map
                self.maps.append(map)

        if self.player.monsters:
            self.determine_pokemon_found(map_tile)

    def determine_pokemon_found(self, map_tile):
        if map_tile not in config.MONSTER_TYPES:
            return

        random_number = utilities.generate_random_number(1, 10)

        # 20 percent chance of hitting pokemon
        if random_number <= 2:
            found_monster = self.monster_factory.create_monster(map_tile)
            print("you found a monster!")
            print("Monster Type: " + found_monster.type)
            print("Attack: " + str(found_monster.attack))
            print("Health: " + str(found_monster.health))

            self.battle = Battle(self.screen, found_monster, self.player)
            self.current_game_state = CurrentGameState.BATTLE

    def handle_events(self):
        if self.event is not None:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            #     handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.NONE
                elif event.key == pygame.K_w: # up
                    self.move_unit(self.player, [0, -1])
                elif event.key == pygame.K_s: # down
                    self.move_unit(self.player, [0, 1])
                elif event.key == pygame.K_a: # left
                    self.move_unit(self.player, [-1, 0])
                elif event.key == pygame.K_d: # right
                    self.move_unit(self.player, [1, 0])
                #these are for debug
                elif event.key == pygame.K_UP: # up
                    self.move_unit(self.player, [0, -10])
                elif event.key == pygame.K_DOWN: # down
                    self.move_unit(self.player, [0, 10])
                elif event.key == pygame.K_LEFT: # left
                    self.move_unit(self.player, [-10, 0])
                elif event.key == pygame.K_RIGHT: # right
                    self.move_unit(self.player, [10, 0])

    def move_unit(self, unit, position_change):
        new_position = [unit.position[0] + position_change[0], unit.position[1] + position_change[1]]

        # check if off map
        if new_position[0] < 0 or new_position[0] > (len(self.map.map_array[0]) - 1):
            return

        if new_position[1] < 0 or new_position[1] > (len(self.map.map_array) - 1):
            return

        # check for valid movement
        if self.map.map_array[new_position[1]][new_position[0]] in config.IMPASSIBLE:
            return

        self.player_has_moved = True

        unit.update_position(new_position)