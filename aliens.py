import pygame
from pygame.sprite import Sprite
from random import randint


class Alien(Sprite):

    def __init__(self, gui_settings, screen):  # создание пришельца с его начальными параметрами
        super(Alien, self).__init__()
        self.screen = screen
        self.gui_settings = gui_settings
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.bonus = randint(0, gui_settings.bonus_chanse)

    def blitem_alien(self):  # отображение пришельца на экране
        self.screen.blit(self.image, self.rect)

    def update(self):  # изменение положения пришельца на экране в зависимости от его скорости
        self.x += self.gui_settings.alien_speed * self.gui_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):  # проверка на прикасновение пришельца к правой или левой границе экрана
        screen_rect = self.screen.get_rect()
        if (self.rect.right >= screen_rect.right) or (self.rect.left <= 0):
            return True
