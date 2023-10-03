class Setting:

    def __init__(self):  # Инициализация настроек с неизменяемыми параметрами и изменяемыми в отдельной функции
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 40)
        self.boat_speedx = 1.5
        self.boat_speedyup = 0.8
        self.boat_speedydown = 1.8
        self.boat_limit = 3
        self.bullets_allowed = 3
        self.scale = 0.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):  # Изменяемым настройкам присваиваются базовые значения
        self.alien_speed = 0.5
        self.alien_drop_speed = 10
        self.alien_hit_points = 0
        self.bullet_speed = 1
        self.bonus_chanse = 30
        self.big_bullet = False
        self.unstoppable_bullet = False
        self.fleet_direction = 1
        self.alien_points = 5

    def increase_speed(self):  # Изменение параметров скорости пришельца и пули во всех направлениях
        if self.alien_speed <= 2:
            self.alien_speed += self.scale
        if self.alien_drop_speed <= 20:
            self.alien_drop_speed += self.scale * 2
        if self.bullet_speed <= 4:
            self.bullet_speed += self.scale
        if self.bonus_chanse >= 10:
            self.bonus_chanse -= self.scale * 2
        if self.alien_drop_speed > 10:
            self.alien_hit_points += self.scale * 2
