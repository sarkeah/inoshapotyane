import pygame.font


class Button:

    def __init__(self, gui_settings, screen, msg):  # инициализация параметров кнопки
        self.gui_settings = gui_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (100, 45, 100)
        self.text_color = (134, 242, 134)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)
        self.button_clicked = False

    def prep_msg(self, msg):  # подготовка надписи на кнопке
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):  # прорисовка на экране
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
