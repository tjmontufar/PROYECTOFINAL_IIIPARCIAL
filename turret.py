import pygame as pg
import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, title_x, title_y):
        pg.sprite.Sprite.__init__(self)
        self.range = 90
        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()

        # Posicion de la variable
        self.title_x = title_x
        self.title_y = title_y

        # Calcular el centro de las coordenadas
        self.x = (self.title_x + 0.5)* c.TILE_SIZE
        self.y = (self.title_y + 0.5)* c.TILE_SIZE

        # Animacion de la variable
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        # Actualizar imagen
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x , self.y)
        
    def load_images(self):
        # Extraer las imagenes de la hoja de animacion
        size = self.sprite_sheet.get_height()
        animation_list = []

        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list
    
    def update(self):
        # Busqueda desde nueva posicion a la actual
        if pg.time.get_ticks() - self.last_shot > self.cooldown:
            self.play_animation()

    def play_animation(self):
        # Actualizar imagen
        self.image = self.animation_list[self.frame_index]
        
        # Actualizar tiempo
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1

            # Chequear si la animacion ha terminado
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # Recorrer el tiempo completo y limpieza de torres
                self.last_shot = pg.time.get_ticks()