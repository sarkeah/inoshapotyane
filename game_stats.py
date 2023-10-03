import configparser


class GameStats:

    def __init__(self, gui_settings):  # создание начальной статистики
        self.gui_settings = gui_settings
        self.reset_stats()
        self.high_score = self.get_high_score()

    def reset_stats(self):  # создание изменяемых параметров
        self.game_active = False
        self.boat_left = self.gui_settings.boat_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):  # получение рекордного счёта из ини файла(за все прошлые игры)
        conf = configparser.ConfigParser()
        conf.read('highest_score.ini')
        if not conf.has_section('Highest_score'):
            conf['Highest_score']['score'] = '0'
            with open('highest_score.ini', 'w') as config:
                conf.write(config)
            return 0
        else:
            return int(conf['Highest_score']['score'])

    def exp_highest_score(self):  # записываем рекордный счёт в ини файл
        if self.score > self.high_score:
            self.high_score = self.score
            conf = configparser.ConfigParser()
            conf.read('highest_score.ini')
            conf['Highest_score']['score'] = str(self.score)
            with open('highest_score.ini', 'w') as config:
                conf.write(config)
