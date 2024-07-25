import pygame as pg
import math
import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)
        self.range = 90
        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        # Posicion de la variable
        self.tile_x = tile_x
        self.tile_y = tile_y

        # Calcular el centro de las coordenadas
        self.x = (self.tile_x + 0.5)* c.TILE_SIZE
        self.y = (self.tile_y + 0.5)* c.TILE_SIZE

        # Animacion de la variable
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        # Actualizar imagen
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x , self.y)

        # Crear un rango de torres
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        
    def load_images(self):
        # Extraer las imagenes de la hoja de animacion
        size = self.sprite_sheet.get_height()
        animation_list = []

        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list
    
    def update(self, enemy_group):
        # Si el objetivo fue localizado, aplicar animacion de disparo
        if self.target:
            self.play_animation()
        else:
            # Busqueda desde nueva posicion a la actual
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)
    
    def pick_target(self, enemy_group):
        # Buscar un objetivo
        x_dist = 0
        y_dist = 0

        # Calcular la distancia entre la torre y el enemigo
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist**2 + y_dist**2)
            if dist < self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))

    def play_animation(self):
        # Actualizar imagen
        self.original_image = self.animation_list[self.frame_index]
        
        # Actualizar tiempo
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1

            # Chequear si la animacion ha terminado
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # Recorrer el tiempo completo y limpieza de torres
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x , self.y)
        surface.blit(self.image, self.rect)

        if self.selected:
            surface.blit(self.range_image, self.range_rect)