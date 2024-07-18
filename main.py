import pygame as pg
import constants as c
pg.init()

#Limpiar el reloj
clock = pg.time.Clock()


screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

# Cargar imagenes
enemy_image = pg.image.load('ima')

run = True
while run:

    clock.tick(c.FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

pg.quit()
