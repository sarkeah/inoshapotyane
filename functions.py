import sys
from time import sleep
import pygame
from bullet import Bullet
from aliens import Alien


def check_events(gui_settings, screen, stats, play_button, boat, bullets):
    # Принимает тип действия игрока и распределяет по нужным функциям
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.exp_highest_score()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(gui_settings, stats, play_button, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, gui_settings, screen, stats, boat, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, boat)


def check_keydown_events(event, gui_settings, screen, stats, boat, bullets):
    # Обрабатывает действия, передаваемые нажатиями клавиш
    if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
        boat.moving['right'] = True
    if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
        boat.moving['left'] = True
    if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
        boat.moving['top'] = True
    if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
        boat.moving['bottom'] = True
    if event.key == pygame.K_SPACE:
        fire(gui_settings, screen, boat, bullets)
    if event.key == pygame.K_ESCAPE:
        stats.exp_highest_score()
        sys.exit()


def check_keyup_events(event, boat):
    # Обрабатывает действия, передаваемые отпусканием клавиш
    if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
        boat.moving['right'] = False
    if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
        boat.moving['left'] = False
    if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
        boat.moving['top'] = False
    if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
        boat.moving['bottom'] = False


def update_screen(gui_settings, screen, stats, board, boat, aliens, bullets, play_button):
    # Обновляет позицию объектов на экране
    screen.fill(gui_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.blitem_bullet()
    aliens.draw(screen)
    boat.blitem()
    board.show_score()
    if not stats.game_active:
        pygame.mouse.set_visible(True)
        if play_button.button_clicked:
            play_button.prep_msg('Ещё?:)')
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(gui_settings, screen, stats, board, boat, aliens, bullets):
    # Обновляет позицию пуль на экране и уничтожает их при достижении верхнего края экрана
    for bullet in bullets.sprites():
        bullet.update_bullet()
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_collisions(gui_settings, screen, stats, board, boat, aliens, bullets)


def check_bullet_collisions(gui_settings, screen, stats, board, boat, aliens, bullets):
    # Вызывает функции, отвечающие за взаимодействие объектов пуль и пришельцев, а также счёт
    check_bullets_bonus(gui_settings, stats, aliens, bullets)
    realize_bullets_bonus(gui_settings, aliens, bullets)
    check_high_score(stats, board)
    board.prep_score()
    if len(aliens) == 0:
        gui_settings.increase_speed()
        bullets.empty()
        del_bonuses(gui_settings)
        stats.level += 1
        board.prep_level()
        create_fleet(gui_settings, screen, boat, aliens)


def fire(gui_settings, screen, boat, bullets):
    # Создание новой пули
    new_bullet = Bullet(gui_settings, screen, boat)
    if len(bullets) < gui_settings.bullets_allowed:
        bullets.add(new_bullet)


def create_fleet(gui_settings, screen, boat, aliens):
    # Создание ряда пришельцев и изменение очков, получаемых за одного пришельца в зависимости от уровня сложности
    alien = Alien(gui_settings, screen)
    number_aliens_x = get_number_alien_x(gui_settings, alien.rect.width)
    number_rows = get_number_rows(gui_settings, boat.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(gui_settings, screen, aliens, alien_number, row_number)
    gui_settings.alien_points += int(gui_settings.scale * 10)


def get_number_alien_x(gui_settings, alien_width):
    # Подсчёт количества создаваемых пришельцев в зависимости от ширины отображаемого экрана
    available_space_x = gui_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(gui_settings, screen, aliens, alien_number, row_number):
    # Создание одного пришельца и добавление в общий список
    alien = Alien(gui_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(gui_settings, boat_height, alien_height):
    # Подсчитывает количество рядов пришельцев в зависимости от высоты экрана
    available_space_y = (gui_settings.screen_height - (3 * alien_height) - boat_height)
    return int(available_space_y / (2 * alien_height))


def update_aliens(gui_settings, stats, board, screen, boat, aliens, bullets):
    # Проверяет условие достижения боковых и нижнего краёв экрана и обнавляет положение всех пришельцев
    check_fleet_edges(gui_settings, stats, board, screen, boat, aliens, bullets)
    check_aliens_bottom(gui_settings, stats, board, screen, boat, aliens, bullets)
    aliens.update()


def check_fleet_edges(gui_settings, stats, boards, screen, boat, aliens, bullets):
    # Проверяет всех пришельцев на соприкосновение с кораблём и достижение боковых краёв экрана
    for alien in aliens.sprites():
        if pygame.sprite.spritecollideany(boat, aliens):
            boat_hit(gui_settings, stats, boards, screen, boat, aliens, bullets)
        if alien.check_edges():
            change_fleet_direction(gui_settings, aliens)
            break


def change_fleet_direction(gui_settings, aliens):
    # Изменяет направление движения всех пришельцев
    for alien in aliens.sprites():
        alien.rect.y += gui_settings.alien_drop_speed
    gui_settings.fleet_direction *= -1


def boat_hit(gui_settings, stats, board, screen, boat, aliens, bullets):
    # Выполняет действия, связаные с столкновением корабля с пришельцем
    stats.boat_left -= 1
    board.prep_lives()
    if stats.boat_left == 0:
        stats.exp_highest_score()
        stats.reset_stats()
    del_bonuses(gui_settings)
    aliens.empty()
    bullets.empty()
    boat.center_boat()
    create_fleet(gui_settings, screen, boat, aliens)
    sleep(1)


def check_aliens_bottom(gui_settings, stats, boards, screen, boat, aliens, bullets):
    # Проверяет пришельцев на достижение нижнего края экрана
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            boat_hit(gui_settings, stats, boards, screen, boat, aliens, bullets)
            break


def check_play_button(gui_settings, stats, play_button, mouse_x, mouse_y):
    # Выполняет действия, связанные с нажатием кнопки "Играть" и "Ещё"
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True
        gui_settings.initialize_dynamic_settings()
        play_button.button_clicked = True
        del_bonuses(gui_settings)
        pygame.mouse.set_visible(False)


def del_bonuses(gui_settings):
    # Удаляет бонусы пуль
    gui_settings.big_bullet = False
    gui_settings.unstoppable_bullet = False


def check_bullets_bonus(gui_settings, stats, aliens, bullets):
    # Проверяет, попался ли в пришельце бонус для пуль
    for alien in aliens:
        if pygame.sprite.spritecollideany(alien, bullets):
            if alien.bonus == 1:
                gui_settings.big_bullet = True
            elif alien.bonus == 2:
                gui_settings.unstoppable_bullet = True
            stats.score += gui_settings.alien_points


def realize_bullets_bonus(gui_settings, aliens, bullets):
    # Изменяет поведение пуль если есть бонус на пробивающие пули
    if gui_settings.unstoppable_bullet:
        destroy_alien(aliens, bullets, False)
    else:
        destroy_alien(aliens, bullets, True)


def destroy_alien(aliens, bullets, bullet_destroy):
    # Выполняет действия, связанные с попаданием в пришельца
    for alien in aliens:
        if pygame.sprite.spritecollideany(alien, bullets):
            if alien.gui_settings.alien_hit_points > 0:
                alien.gui_settings.alien_hit_points -= 1
                pygame.sprite.groupcollide(bullets, aliens, bullet_destroy, False)
            else:
                pygame.sprite.groupcollide(bullets, aliens, bullet_destroy, True)


def check_high_score(stats, board):
    # Проверяет, побил ли пользователь рекорд
    if stats.score > stats.high_score:
        stats.exp_highest_score()
        board.prep_high_score()
