import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, gui_settings, screen, boat):  # инициализация пули с начальными параметрами
        super(Bullet, self).__init__()
        self.screen = screen
        if gui_settings.big_bullet:
            self.big_bullet_prep(boat)
        else:
            self.bullet_prep(boat)
        self.speed = gui_settings.bullet_speed

    def update_bullet(self):  # обновление положения на экране
        self.y -= self.speed
        self.rect.y = self.y

    def blitem_bullet(self):  # прорисовка изображения на экране
        self.screen.blit(self.image, self.rect)

    def bullet_prep(self, boat):  # подготовка изображения стандартной пули
        self.image = pygame.image.load('images/bullets.bmp')
        self.rect = self.image.get_rect()
        self.rect.centerx = boat.rect.centerx
        self.rect.top = boat.rect.top
        self.y = float(self.rect.y)

    def big_bullet_prep(self, boat):  # подготовка изображения большой пули(бонус)
        self.image = pygame.image.load('images/bullets_big.bmp')
        self.rect = self.image.get_rect()
        self.rect.centerx = boat.rect.centerx
        self.rect.top = boat.rect.top
        self.y = float(self.rect.y)
