import pygame as pg
import json
from enemy import Enemy
from turret import Turret
from button import Button
from world import World
import constants as c
pg.init()

import os
os.system('cls' if os.name == 'nt' else 'clear')

#Crear un reloj
clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

#Variables del Juego
placing_turrets = False
selected_turret = None

# Cargar imagenes

# Mapa
map_image = pg.image.load("imagen/niveles/level.png").convert_alpha()

# Enemigo
enemy_image = pg.image.load("imagen/enemigos/enemy_1.png").convert_alpha()

# Botones
buy_turret_image = pg.image.load("imagen/botones/buy_turret.png").convert_alpha()
cancel_image = pg.image.load("imagen/botones/cancel.png").convert_alpha()

#Torre individual imagen 
turret_sheet = pg.image.load("imagen/torretas/turret_1.png").convert_alpha()
cursor_turret = pg.image.load("imagen/torretas/cursor_turret.png").convert_alpha()

# Cargar el archivo json para la ruta del nivel
with open("imagen/niveles/level.tmj") as file:
    world_data = json.load(file)

# Crear un grupo de torretas
def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

    #Calcular la secuencia de numeros del titulo
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x

    #Chequiar si el titulo es valido
    if world.tile_map[mouse_tile_num] == 7:

        #Chequiar si el cursor se encuentra sobre una torre
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False

        #Si la torre no es una torre no valida, no crearla
        if space_is_free == True:
            new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

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

# Crear botones
turret_buy_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)

run = True
while run:

    clock.tick(c.FPS)
    # Colocar un color de fondo
    screen.fill("grey100")

    #############################
    # Seccion de Actualizacion
    #############################

    # Actualizar los grupos
    enemy_group.update()
    turret_group.update()

    # Marcar la torre seleccionada
    if selected_turret:
        selected_turret.selected = True

    #############################
    # Seccion de Dibujo
    #############################

    # Dibujar el mundo
    world.draw(screen)

    # Dibujar grupos
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    # Dibujar botones
    if turret_buy_button.draw(screen):
        placing_turrets = True
    
    #Si la colocacion de la torre es correcta, crear la torre
    if placing_turrets == True:
        #Cursor en la torre
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            cursor_rect.center = cursor_pos
        screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen):
            placing_turrets = False

    # Manejo del evento
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        #Manejo de eventos del ratón
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #Chequiar si el ratón se encuentra sobre una torre
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # Limpiar la seleccion de la torre
                selected_turret = None
                clear_selection()
                if placing_turrets == True:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)


    pg.display.flip()

pg.quit()