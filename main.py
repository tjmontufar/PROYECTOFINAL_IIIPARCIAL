import pygame as pg
import json
from enemy import Enemy
from turret import Turret
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
#Torre individual imagen 
cursor_turret = pg.image.load("imagen/cursor_turret.png").convert_alpha()


# Cargar el archivo json para la ruta del nivel
with open("niveles/level.tmj") as file:
    world_data = json.load(file)

# Crear un grupo de torretas
def create_turret(mouse_pos):
    mouse_title_x = mouse_pos[0] // c.TITLE_SIZE
    mouse_title_y = mouse_pos[1] // c.TITLE_SIZE
    #Calcular la secuencia de numeros del titulo
    mouse_tile_num = (mouse_title_y * c.COLS) + mouse_title_x
    #Chequiar si el titulo es valido
    if world.tile_map[mouse_tile_num] == 7:
        #Chequiar si el cursor se encuentra sobre una torre
        space_is_free = True
        for turret in turret_group:
            if (mouse_title_x, mouse_title_y) == (turret.title_x, turret.title_y):
                space_is_free = False
        #Si la torre no es una torre no valida, no crearla
        if space_is_free == True:
            new_turret = Turret(cursor_turret, mouse_title_x, mouse_title_y)
            turret_group.add(new_turret)


# Crear el mundo
world = World(world_data, map_image)
world.process_data()

# Crear grupos de imagenes
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

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
    turret_group.draw(screen)

    # Manejo del evento
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        #Manejo de eventos del ratón
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #Chequiar si el ratón se encuentra sobre una torre
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                create_turret(mouse_pos)


    pg.display.flip()

pg.quit()