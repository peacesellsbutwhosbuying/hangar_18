
import pygame
# Импортируем настройки из файла settings.py
from settings import *
# Переобозначаем вектор(двумерный) для удобства использования
vector2 = pygame.math.Vector2





class Player(pygame.sprite.Sprite):
    """Объект игрока"""
    def __init__(self,game):

        pygame.sprite.Sprite.__init__(self)
        # Переменная ходьбы
        self.walking = False
        # Переменная прыжка
        self.jumping = False
        # Текущий кадр
        self.current_frame = 0
        # Последний обновлённый кадр
        self.last_update = 0
        # Загружаем изображение персонажа через функцию
        self.load_images()
        self.image = self.standing
        self.game = game
        # Получаем область персонажа
        self.rect = self.image.get_rect()
        # Удаляем фон, отсавляя только модель персонажа
        # Указываем начальную позицию персонажа
        self.rect.center = (WIDTH//2, HEIGHT//2)
        # Указываем начальную позицию игрока, но через вектор
        self.pos = pygame.math.Vector2(WIDTH//2, HEIGHT//2)
        # Скорость игрока
        self.vel = vector2(0, 0)
        # Ускорение игрока
        self.ac = vector2(0, 0)

    def load_images(self):
        """Функция загрузки изображений персонажа"""
        # Изображения когда персонаж стоит
        self.standing = pygame.image.load('Vic_front.png')
        # Удаление фона изображения
        self.standing.set_colorkey(back_gr)
        # Изображения, если игрок идёт вправо
        self.walk_right_frames = [pygame.image.load('Right_1.png'),
                                 pygame.image.load('Right_2.png'),
                                 pygame.image.load('Right_3.png'),
                                 pygame.image.load('Right_4.png')]
        # Удаление фона для анимации передвижения вправо
        for frame in self.walk_right_frames:
            frame.set_colorkey(back_gr)
        """Переворот изображений для анимации движения влево"""
        # Создаём пустой массив
        self.walk_left_frames = []
        for frame in self.walk_left_frames:
            frame.set_colorkey(back_gr)
        # Заполняем массив развёрнутыми изображениями
        for frame in self.walk_right_frames:
            self.walk_left_frames.append(pygame.transform.flip(frame, True, False))

    def jump(self):
        # Прыгаем только если стоим на поверхности
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def shoot(self):

        bullet = Bullet(self.rect.centerx, self.rect.top)









    def update(self):
        """Функция передвижения игрока в пространстве"""
        self.animate()
        self.ac = vector2(0, player_grav)
        # Считывание всех нажатых клавиш
        self.keys = pygame.key.get_pressed()

        if (self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]) and self.rect.x > 5:
            self.ac.x = -player_ac
        if (self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]) and self.rect.x < 1200:
            self.ac.x = player_ac

        # Учёт силы трения (для того, чтобы игрок не скользил)
        self.ac.x += self.vel.x * player_friction
        # Расчёт передвижения игрока
        self.vel += self.ac
        # Условие для остановки анимации
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.ac

        self.rect.midbottom = self.pos

    def animate(self):
        """Функция анимации игрока"""
        # Время игры
        now = pygame.time.get_ticks()

        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # Анимация персонажа
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_right_frames)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_right_frames[self.current_frame]
                else:
                    self.image = self.walk_left_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.walking:
            self.image = self.standing


class Platform(pygame.sprite.Sprite):
    """Объект платформ"""
    # На вход получаются аргументы ( координаты х и у, ширина и высота)
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        # Загружаем изображение с учётом ширины и высоты
        self.image = pygame.Surface((w, h))
        self.image.fill(BLACK)
        # Обозначаем область объекта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.facing = 1
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_d]:
            self.facing = 1
        if self.keys[pygame.K_RIGHT]:
            self.facing = 1
        if self.keys[pygame.K_a]:
            self.facing = -1
        if self.keys[pygame.K_LEFT]:
            self.facing = -1
        self.vel = 8 * self.facing
    def update(self):
        self.rect.x += self.vel





