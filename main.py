import pygame
from pygame.sprite import Group
import functions as func
from settings import Setting
from boat import Boat
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():  # основная процедура. Создаём экран, необходимые объекты, настраиваем отображение и обнавляем экран
    pygame.init()
    gui_settings = Setting()
    screen = pygame.display.set_mode((gui_settings.screen_width, gui_settings.screen_height))
    boat = Boat(gui_settings, screen)
    bullets = Group()
    aliens = Group()
    pygame.display.set_caption('Инопрешеленцы приехали')
    play_button = Button(gui_settings, screen, 'Играть')
    stats = GameStats(gui_settings)
    board = Scoreboard(gui_settings, screen, stats)
    func.create_fleet(gui_settings, screen, boat, aliens)
    while True:
        func.check_events(gui_settings, screen, stats, play_button, boat, bullets)
        if stats.game_active:
            boat.update()
            func.update_bullets(gui_settings, screen, stats, board, boat, aliens, bullets)
            func.update_aliens(gui_settings, stats, board, screen, boat, aliens, bullets)
        func.update_screen(gui_settings, screen, stats, board, boat, aliens, bullets, play_button)


run_game()  # запуск игры
