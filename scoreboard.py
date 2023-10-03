import pygame.font


class Scoreboard:

    def __init__(self, gui_settings, screen, stats):  # инициализация начальной таблицы рекордов и состояния
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.gui_settings = gui_settings
        self.stats = stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):  # подготовка для вывода на экран надписи со счётом игрока
        score_str = str(self.stats.score)
        self.score_image = self.font.render("Счёт: " + score_str, True, self.text_color, self.gui_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right-20
        self.score_rect.top = 20

    def prep_high_score(self):  # подготовка для вывода на экран надписи с рекордом
        high_score_str = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render('Рекорд: ' + high_score_str, True, self.text_color,
                                                 self.gui_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def show_score(self):  # вывод на экран всей статистики
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.lives_image, self.lives_rect)

    def prep_level(self):  # подготовка для вывода на экран надписи с уровнем сложности
        self.level_image = self.font.render('Уровень: ' + str(self.stats.level), True, self.text_color,
                                            self.gui_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):  # подготовка для вывода на экран надписи с оставшимися жизнями игрока
        self.lives_image = self.font.render('Жизней: X' + str(self.stats.boat_left), True, self.text_color,
                                            self.gui_settings.bg_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.screen_rect.left + 20
        self.lives_rect.top = self.screen_rect.top + 20
