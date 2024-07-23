import pygame as pg
import json
from enemy import Enemy
from world import World
import constants as c
pg.init()

#Crear un reloj
clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

# Cargar imagenes

# Mapa
map_image = pg.image.load("niveles/level.png").convert_alpha()
# Enemigo
enemy_image = pg.image.load("imagen/enemy_1.png").convert_alpha()

# Cargar el archivo json para la ruta del nivel
with open("niveles/level.tmj") as file:
    world_data = json.load(file)

# Crear el mundo
world = World(world_data, map_image)
world.process_data()

# Crear grupos de imagenes
enemy_group = pg.sprite.Group()
# Crear un enemigo y ruta de patrullaje
enemy = Enemy(world.waypoints, enemy_image)

# Añadir imagenes a los grupos
enemy_group.add(enemy)

run = True
while run:

    clock.tick(c.FPS)
    # Colocar un color de fondo
    screen.fill("grey100")

    # Dibujar el mundo
    world.draw(screen)

    # Actualizar los grupos
    enemy_group.update()

    # Dibujar grupos
    enemy_group.draw(screen)

    # Manejo del evento
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()

pg.quit()