import pygame as pg
import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, image, title_x, title_y):
        pg.sprite.Sprite.__init__(self)
        self.title_x = title_x
        self.title_y = title_y
        #calcular centro de las coordenadas
        self.x = (self.title_x + 0.5)* c.TILE_SIZE
        self.y = (self.title_y + 0.5)* c.TILE_SIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x , self.y)