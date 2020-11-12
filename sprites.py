
import pygame
# Импортируем настройки из файла settings.py
from settings import *
# Переобозначаем вектор(двумерный) для удобства использования
vector2 = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    """Объект игрока"""
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        # Загружаем изображение персонажа
        self.image = pygame.image.load(r'Vic_front.png').convert_alpha()
        # Получаем область персонажа
        self.rect = self.image.get_rect()
        # Удаляем фон, отсавляя только модель персонажа
        self.image.set_colorkey(back_gr)
        # Указываем начальную позицию персонажа
        self.rect.center = (WIDTH//2, HEIGHT//2)
        # Указываем начальную позицию игрока, но через вектор
        self.pos = pygame.math.Vector2(WIDTH//2, HEIGHT//2)
        # Скорость игрока
        self.vel = vector2(0, 0)
        # Ускорение игрока
        self.ac = vector2(0, 0)

    def update(self):
        """Функция передвижения игрока в пространстве"""
        self.ac = vector2(0, 1.15)
        # Считывание всех нажатых клавиш
        self.keys = pygame.key.get_pressed()

        if (self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]) and self.rect.x > 5:
            self.ac.x = -player_ac
        if (self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]) and self.rect.x < 1200:
            self.ac.x = player_ac

        # Учёт силы трения (для того, чтобы игрок не скользил)
        self.ac += self.vel * player_friction
        # Расчёт передвижения игрока
        self.vel += self.ac
        self.pos += self.vel + 0.5 * self.ac

        self.rect.midbottom = self.pos


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




