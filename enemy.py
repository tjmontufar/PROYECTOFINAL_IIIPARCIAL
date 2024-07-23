import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 2
        self.angle = 0
        self.original_image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        # Calcular la dirección hacia el siguiente waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Si no hay más waypoints, el enemigo se detiene
            self.kill()

        # Calcular la distancia hacia el objetivo
        dist = self.movement.length()
        # Ajustar la velocidad si es necesario para no pasar el waypoint
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
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
