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
in_menu = True
game_over = False
game_outcome = 0 # -1 Si pierde, 1 si gana
game_speed_toggle = False
game_paused = False
afford = False
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
confirm_exit = False
confirm_restart = False

##########################################################
#               CARGA DE IMAGENES
##########################################################

# Mapa
map_image = pg.image.load('imagen/niveles/level.png').convert_alpha()
# Menu principal
main_menu_image = pg.image.load('imagen/niveles/main_menu.png').convert_alpha()

# Enemigo
enemy_images = {
    "weak": pg.image.load('imagen/enemigos/enemy_1.png').convert_alpha(),
    "medium": pg.image.load('imagen/enemigos/enemy_2.png').convert_alpha(),
    "strong": pg.image.load('imagen/enemigos/enemy_3.png').convert_alpha(),
    "elite": pg.image.load('imagen/enemigos/enemy_4.png').convert_alpha()
}
enemy_image = pg.image.load('imagen/enemigos/enemy_1.png').convert_alpha()

# Botones
play_image = pg.image.load('imagen/botones/play.png').convert_alpha()
buy_turret_image = pg.image.load('imagen/botones/buy_turret_true.png').convert_alpha()
buy_turret_false_image = pg.image.load('imagen/botones/buy_turret_false.png').convert_alpha()
cancel_image = pg.image.load('imagen/botones/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('imagen/botones/upgrade_turret_true.png').convert_alpha()
upgrade_turret_false_image = pg.image.load('imagen/botones/upgrade_turret_false.png').convert_alpha()
begin_image = pg.image.load('imagen/botones/begin.png').convert_alpha()
restart_image = pg.image.load('imagen/botones/restart.png').convert_alpha()
fast_forward_false_image = pg.image.load('imagen/botones/fast_forward_false.png').convert_alpha()
fast_forward_true_image = pg.image.load('imagen/botones/fast_forward_true.png').convert_alpha()
exit_image = pg.image.load('imagen/botones/exit.png').convert_alpha()
yes_image = pg.image.load('imagen/botones/yes.png').convert_alpha()
not_image = pg.image.load('imagen/botones/no.png').convert_alpha()
pause_image = pg.image.load('imagen/botones/pause.png').convert_alpha()
continue_image = pg.image.load('imagen/botones/continue.png').convert_alpha()
restart_level_image = pg.image.load('imagen/botones/restart_level.png').convert_alpha()

# Cargar efectos de sonido
shot_fx = pg.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.5)

# Interfaz grafica
heart_image = pg.image.load('imagen/iconos/heart.png').convert_alpha()
coin_image = pg.image.load('imagen/iconos/coin.png').convert_alpha()
logo_image = pg.image.load('imagen/iconos/logo.png').convert_alpha()

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

def display_data():
    # Dibujar el panel
    pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
    screen.blit(logo_image, (c.SCREEN_WIDTH, 400))
    # Dibujar iconos

    # Mostrar textos en pantalla
    draw_text("NIVEL: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 10) # Nivel
    screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 35)) # Icono de salud
    draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40) # Salud
    screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 65)) # Icono de dinero
    draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 70) # Dinero
    

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
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
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
fast_forward_button = Button(c.SCREEN_WIDTH + 60, 300, fast_forward_false_image, False)
play_button = Button((1020 // 2) - 75, 400, play_image, True)
exit_button = Button(965, 5, exit_image, True)
pause_button = Button(915, 5, pause_image, True)
restart_level_button = Button(965, 55, restart_level_image, True)

run = True
while run:
    clock.tick(c.FPS)
    # Pantalla de inicio
    if not game_paused:
        if in_menu:
            # Dibujar el menú
            screen.blit(main_menu_image, (0, 0))
            if play_button.draw(screen):
                in_menu = False

        ##########################################################
        #               SECCION DE ACTUALIZACION
        ##########################################################

        elif not game_over:
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
            turret_group.update(enemy_group, world)

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

            display_data()

            ##########################################################
            #               LOGICA DEL NIVEL
            ##########################################################

            # Verificar si el jugador ha perdido
            if not game_over:
                # Revisar si el juego ha iniciado o no
                if not level_started:
                    if begin_button.draw(screen):
                        level_started = True
                else:
                    # Opcion de Aceleracion de juego
                    if fast_forward_button.draw(screen):
                        game_speed_toggle = not game_speed_toggle

                    if game_speed_toggle:
                        world.game_speed = 1
                        fast_forward_button.image = fast_forward_false_image
                    else:
                        world.game_speed = 2
                        fast_forward_button.image = fast_forward_true_image
                    
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
                    world.game_speed = 1

                # Dibujar botones para colocar torretas
                # Para el boton de la torreta, mostrar el costo de la torreta y dibujar el boton
                draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
                screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 130))

                # Actualizar la imagen del botón de compra de torretas si hay o no suficiente dinero
                if world.money >= c.BUY_COST:
                    turret_buy_button.image = buy_turret_image
                else:
                    turret_buy_button.image = buy_turret_false_image

                if turret_buy_button.draw(screen):
                    placing_turrets = True
                
                #Si la colocacion de la torreta es correcta, crear la torreta
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
                        # Mostrar el costo de la mejora
                        draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
                        screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 190))
                        # Actualizar la imagen del botón de mejora de torretas si hay o no suficiente dinero
                        if world.money >= c.UPGRADE_COST:
                            upgrade_button.image = upgrade_turret_image
                        else:
                            upgrade_button.image = upgrade_turret_false_image
                        if upgrade_button.draw(screen):
                            # Verificar Si hay suficiente dinero para mejorar la torreta
                            if world.money >= c.UPGRADE_COST:
                                selected_turret.upgrade()
                                world.money -= c.UPGRADE_COST

                # Revisar si el boton de salir es presionado
                if exit_button.draw(screen):
                    game_paused = True
                    confirm_exit = True
                
                # Revisar si el boton de pausa es presionado
                if pause_button.draw(screen):
                    game_paused = True
                
                # Revisar si el boton de reinicio es presionado
                if restart_level_button.draw(screen):
                    game_paused = True
                    confirm_restart = True
        else:
            pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
            if game_outcome == -1:
                draw_text("FIN DEL JUEGO", large_font, "grey0", 270, 230)
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
    else:
        # Confirmar la salida del juego
        if confirm_exit:
            pg.draw.rect(screen, "grey", (200, 200, 400, 200), border_radius = 30)
            draw_text("¿QUIERES SALIR?", large_font, "grey0", 250, 240)
            yes_button = Button(275, 320, yes_image, True)
            no_button = Button(425, 320, not_image, True)

            if yes_button.draw(screen):
                in_menu = True
                game_over = False
                confirm_exit = False
                game_paused = False
                # Restablecer el juego a su posición inicial
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                enemy_group.empty()
                turret_group.empty()

            if no_button.draw(screen):
                confirm_exit = False
                game_paused = False
        # Confirmar el reinicio del nivel
        elif confirm_restart:
            pg.draw.rect(screen, "grey", (200, 200, 400, 200), border_radius = 30)
            draw_text("¿REINICIAR NIVEL?", large_font, "grey0", 250, 240)
            yes_button = Button(275, 320, yes_image, True)
            no_button = Button(425, 320, not_image, True)

            if yes_button.draw(screen):
                game_over = False
                confirm_restart = False
                game_paused = False
                # Restablecer el juego a su posición inicial
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                enemy_group.empty()
                turret_group.empty()

            if no_button.draw(screen):
                confirm_restart = False
                game_paused = False
        # Pausar el juego
        elif game_paused:
            pg.draw.rect(screen, "grey", (200, 200, 400, 200), border_radius = 30)
            draw_text("JUEGO PAUSADO", large_font, "grey0", 250, 240)
            continue_button = Button(275, 320, continue_image, True)
            if continue_button.draw(screen):
                game_paused = False

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