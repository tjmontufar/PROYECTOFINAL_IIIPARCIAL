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
game_over = False
game_outcome = 0 # -1 Si pierde, 1 si gana
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None

##########################################################
#               CARGA DE IMAGENES
##########################################################

# Mapa
map_image = pg.image.load('imagen/niveles/level.png').convert_alpha()

# Enemigo
enemy_images = {
    "weak": pg.image.load('imagen/enemigos/enemy_1.png').convert_alpha(),
    "medium": pg.image.load('imagen/enemigos/enemy_2.png').convert_alpha(),
    "strong": pg.image.load('imagen/enemigos/enemy_3.png').convert_alpha(),
    "elite": pg.image.load('imagen/enemigos/enemy_4.png').convert_alpha()
}
enemy_image = pg.image.load('imagen/enemigos/enemy_1.png').convert_alpha()

# Botones
buy_turret_image = pg.image.load('imagen/botones/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('imagen/botones/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('imagen/botones/upgrade_turret.png').convert_alpha()
begin_image = pg.image.load('imagen/botones/begin.png').convert_alpha()
restart_image = pg.image.load('imagen/botones/restart.png').convert_alpha()

# Imagen de la torreta
turret_spritesheets = []
# Cambiar la imagen de la torreta si sufre mejoras
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'imagen/torretas/turret_{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)

# Imagen del cursor de la torreta
cursor_turret = pg.image.load('imagen/torretas/cursor_turret.png').convert_alpha()

# Cargar el archivo json para la ruta del nivel
with open('imagen/niveles/level.tmj') as file:
    world_data = json.load(file)

# Cargar fuentes para mostrar texto en pantalla
text_font = pg.font.SysFont("Consolas", 24, bold=True)
large_font = pg.font.SysFont("Consolas", 36)

# Funciones para colocar texto en pantalla
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

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
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

            # Deducir el costo de la torreta
            world.money -= c.BUY_COST

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
world.process_enemies()

# Crear grupos de imagenes
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Crear botones
turret_buy_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)

run = True
while run:

    clock.tick(c.FPS)
    # Colocar un color de fondo
    screen.fill("grey100")

    ##########################################################
    #               SECCION DE ACTUALIZACION
    ##########################################################

    if game_over == False:
        # Revisar si el juagador ha perdido
        if world.health <= 0:
            game_over = True
            game_outcome = -1 # Perdió
        
        # Revisar si el jugador ha ganado
        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1 # Ganó

        # Actualizar los grupos
        enemy_group.update(world) 
        turret_group.update(enemy_group)

        # Marcar la torre seleccionada
        if selected_turret:
            selected_turret.selected = True

    ##########################################################
    #               SECCION DE DIBUJO
    ##########################################################

    # Dibujar el mundo
    world.draw(screen)

    # Dibujar grupos
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)
    
    # Mostrar textos en pantalla
    draw_text(str(world.health), text_font, "grey100", 0, 0) # Salud
    draw_text(str(world.money), text_font, "grey100", 0, 30) # Dinero
    draw_text(str(world.level), text_font, "grey100", 0, 60) # Nivel

    ##########################################################
    #               LOGICA DEL NIVEL
    ##########################################################

    # Verificar si el jugador ha perdido
    if game_over == False:
        # Revisar si el juego ha iniciado o no
        if level_started == False:
            if begin_button.draw(screen):
                level_started = True
        else:
            # Spawn de enemigos
            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

        # Revisar si la ola de enemigos ha finalizado
        if world.check_level_complete() == True:
            # Comenzar un nuevo nivel
            world.money += c.LEVEL_COMPLETE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()

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
        
        # Si la torreta es seleccionada, entonces mostrar el boton de mejora
        if selected_turret:
            # Si la torreta puede ser mejorada, entonces mostrar el boton de mejora
            if selected_turret.upgrade_level < c.TURRET_LEVELS:
                if upgrade_button.draw(screen):
                    # Verificar Si hay suficiente dinero para mejorar la torreta
                    if world.money >= c.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.UPGRADE_COST
    else:
        pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
        if game_outcome == -1:
            draw_text("FIN DEL JUEGO", large_font, "grey0", 310, 230)
        elif game_outcome == 1:
            draw_text("¡HAS GANADO!", large_font, "grey0", 315, 230)
        # Reiniciar el nivel
        if restart_button.draw(screen):
            # Restablecer las variables de juego a su posicion inicial
            game_over = False
            level_started = False
            placing_turrets = False
            selected_turret = None
            last_enemy_spawn = pg.time.get_ticks()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            # Limpiar los grupos de enemigos y torretas
            enemy_group.empty()
            turret_group.empty()

    # Manejo del evento
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        #Manejo de eventos del ratón
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #Chequiar si el ratón se encuentra sobre una torreta
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # Limpiar la seleccion de la torre
                selected_turret = None
                clear_selection()
                if placing_turrets == True:
                    # Revisar si hay suficiente dinero para poner una torreta
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)


    pg.display.flip()

pg.quit()