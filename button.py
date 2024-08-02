import pygame as pg

class Button():
    def __init__(self, x, y, image, sound_click, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click
        self.sound_click = sound_click
    
    def draw(self, surface):
        action = False
        # Obtener la posicion del mouse
        pos = pg.mouse.get_pos()

        # Verificar si el mouse se encuentra sobre el boton y condiciones de clickeo
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                # Verificar si el boton es de un solo click, entonces devuelve Verdadero
                if self.single_click:
                    self.clicked = True
                    if self.sound_click:
                        self.sound_click.play()
                self.clicked = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Dibujar el boton en pantalla
        surface.blit(self.image, self.rect)
        return action