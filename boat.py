import pygame


class Boat:

    def __init__(self, gui_settings, screen):  # инициализация корабля с начальными характеристиками
        self.screen = screen
        self.gui = gui_settings
        self.image = pygame.image.load('images/boat.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.hor = float(self.rect.centerx)
        self.vert = float(self.rect.centery)
        self.moving = {'right': False, 'left': False, 'top': False, 'bottom': False}

    def blitem(self):  # отображение корабля на экране
        self.screen.blit(self.image, self.rect)

    def update(self):  # обновление положения корабля в зависимости от действий игрока
        if self.moving['right'] and self.rect.right < self.screen_rect.right:
            self.hor += self.gui.boat_speedx
        if self.moving['left'] and self.rect.left > 0:
            self.hor -= self.gui.boat_speedx
        if self.moving['top'] and self.rect.top > 0:
            self.vert -= self.gui.boat_speedyup
        if self.moving['bottom'] and self.rect.bottom < self.screen_rect.bottom:
            self.vert += self.gui.boat_speedydown
        self.rect.centerx = self.hor
        self.rect.centery = self.vert

    def center_boat(self):  # возвращени корабля в начальную точку при потере жизни или переходе на новый уровень
        self.rect.centerx = self.screen_rect.centerx
        self.hor = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.vert = float(self.rect.centery)
