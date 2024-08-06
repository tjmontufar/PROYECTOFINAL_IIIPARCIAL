import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.flash_duration = 0.1
        self.is_flashing = False
        self.flash_timer = 0

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)
        self.handle_flashing(world)
    
    def handle_flashing(self, world):
        if self.is_flashing:
            # Aplicar un tinte rojo temporalmente
            red_tint = pg.Surface(self.image.get_size(), pg.SRCALPHA)
            red_tint.fill((255, 0, 0, 128))  # Rojo con 50% de transparencia
            self.image.blit(red_tint, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
            # Actualizar el temporizador de parpadeo
            self.flash_timer -= world.delta_time * 1000  # Ajustar con delta time
            if self.flash_timer <= 0:
                self.is_flashing = False
                # Restaurar el color original del sprite
                self.image = pg.transform.rotate(self.original_image, self.angle)
                
    def move(self, world):
        # Calcular la dirección hacia el siguiente waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Si no hay más waypoints, el enemigo se detiene
            self.kill()
            world.health -= 1
            world.missed_enemies += 1

        # Calcular la distancia hacia el objetivo
        dist = self.movement.length()
        # Ajustar la velocidad si es necesario para no pasar el waypoint
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        # Calcular la dirección hacia el siguiente waypoint
        dist = self.target - self.pos

        # Usar la distancia para calcular el ángulo
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

        # Rotar la imagen y actualizar el rectángulo
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()