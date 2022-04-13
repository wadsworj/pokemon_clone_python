import pygame
import config
import math
import utilities
from building import Building
from npc import Npc


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.map_array = []
        self.camera = [0, 0]
        self.file_name = None
        self.player_exit_position = None
        self.objects = []
        self.exit_positions = []

    def load(self, file_name, player):
        self.file_name = file_name

        self.player = player
        self.objects = [player]

        with open('maps/' + file_name + ".txt") as map_file:
            for line in map_file:
                tiles = []
                for i in range(0, len(line) - 1, 2):
                    tiles.append(line[i])
                self.map_array.append(tiles)
            print(self.map_array)

        map_config = config.MAP_CONFIG[file_name]

        player.position = map_config['start_position'][:]

        for building_data in map_config["buildings"]:
            building = Building(building_data['sprite'], building_data['position'], building_data['size'])
            self.objects.append(building)

        for exit_position in map_config['exits']:
            self.exit_positions.append(exit_position)

    def load_room(self, map_name, room_name, player):
        self.player = player
        self.objects = [player]

        room_config = config.ROOM_CONFIG[map_name][str(room_name).zfill(2)]
        self.player.position = room_config['start_position'][:]
        self.player.player_exit_position = room_config['exit_position'][:]
        self.player_exit_position = room_config['exit_position'][:]

        # create our npcs
        for npc_data in room_config['npcs']:
            npc = Npc(npc_data['name'], npc_data['image'], npc_data['start_position'][0], npc_data['start_position'][1])
            self.objects.append(npc)

        with open('rooms/' + map_name + '/' + str(room_name).zfill(2) + ".txt") as room_file:
            for line in room_file:
                tiles = []
                for i in range(0, len(line) - 1, 2):
                    tiles.append(line[i])
                self.map_array.append(tiles)
            print(self.map_array)

        pass

    def render(self, screen, player):
        self.determine_camera(player)

        y_pos = 0
        for line in self.map_array:
            x_pos = 0
            for tile in line:
                if tile not in map_tile_image:
                    x_pos = x_pos + 1
                    continue
                image = map_tile_image[tile]
                rect = pygame.Rect(x_pos * config.SCALE - (self.camera[0] * config.SCALE), y_pos * config.SCALE - (self.camera[1] * config.SCALE), config.SCALE, config.SCALE)
                screen.blit(image, rect)
                x_pos = x_pos + 1

            y_pos = y_pos + 1

        # draw all objects on map
        for object in self.objects:
            object.render(self.screen, self.camera)

    def determine_camera(self, player):
        # y axis
        max_y_position = len(self.map_array) - config.SCREEN_HEIGHT / config.SCALE
        y_position = player.position[1] - math.ceil(round(config.SCREEN_HEIGHT/ config.SCALE / 2))

        if y_position <= max_y_position and y_position >= 0:
            self.camera[1] = y_position
        elif y_position < 0:
            self.camera[1] = 0
        else:
            self.camera[1] = max_y_position

        # x axis
        max_x_position = len(self.map_array[0]) - config.SCREEN_WIDTH / config.SCALE
        x_position = player.position[0] - math.ceil(round(config.SCREEN_WIDTH / config.SCALE / 2))

        if x_position <= max_x_position and x_position >= 0:
            self.camera[0] = x_position
        elif x_position < 0:
            self.camera[0] = 0
        else:
            self.camera[0] = max_x_position

map_tile_image = {
    config.MAP_TILE_GRASS : pygame.transform.scale(pygame.image.load("imgs/grass1.png"), (config.SCALE, config.SCALE)),
    config.MAP_TILE_WATER: pygame.transform.scale(pygame.image.load("imgs/water.png"), (config.SCALE, config.SCALE)),
    config.MAP_TILE_ROAD: pygame.transform.scale(pygame.image.load("imgs/road.png"), (config.SCALE, config.SCALE)),
    config.MAP_TILE_LAB_FLOOR: pygame.transform.scale(pygame.image.load("imgs/lab_tile.png"), (config.SCALE, config.SCALE)),
    config.MAP_TILE_LAB_WALL: pygame.transform.scale(pygame.image.load("imgs/lab_wall.png"), (config.SCALE, config.SCALE)),
    config.MAP_TILE_ROOM_EXIT: pygame.transform.scale(pygame.image.load("imgs/floor_mat.png"), (config.SCALE, config.SCALE)),
}
