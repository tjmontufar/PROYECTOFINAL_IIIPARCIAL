import pygame as pg
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA

class World():
    def __init__(self, data, map_image):
        self.level = 1
        self.game_speed = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
    
    def process_data(self):
        # Procesar los datos del nivel
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)
 
    def process_waypoints(self, data):
        # Iterar sobre los waypoints para extraer coordenadas X e Y
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x,temp_y))

    def process_enemies(self):
        if 1 <= self.level <= c.TOTAL_LEVELS:
            try:
                enemies = ENEMY_SPAWN_DATA[self.level - 1]
                for enemy_type in enemies:
                    enemies_to_spawn = enemies[enemy_type]
                    for _ in range(enemies_to_spawn):
                        self.enemy_list.append(enemy_type)
                random.shuffle(self.enemy_list)
            except IndexError:
             print(f"Error: Nivel {self.level - 1} está fuera del rango para ENEMY_SPAWN_DATA")
        
    # Chequear si el nivel ha finalizado
    def check_level_complete(self):
        if (self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True
    
    def reset_level(self):
        # Reiniciar los valores del enemigo
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
    
    def draw(self, surface):
        surface.blit(self.image, (0, 0))