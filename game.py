import pygame
from settings import *
# Импортируем значения параметров


class Game():

    """Объект игры"""

    def __init__(self):
        """Функция основынх настроек игры"""
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hangar 18")
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        """Функция новой игры"""
        self.all_sprites = pygame.sprite.Group()
        self.run()  # Запускаем функию run() для группирования игры

    def run(self):
        """Функция содержит основной цикл игры"""
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()       # Запуск событий
            self.update()       # Запуск обновлений
            self.draw()         # Запуск отрисовки

    def update(self):
        self.all_sprites.update()

    def events(self):
        """ Функция основных событий игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw (self):
        """Функия отрисовки"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        pygame.display.flip()

    def start_screen(self):
        """Окно запуска игры"""
        pass

    def GO_screen(self):
        """Окно Game Over"""
        pass
g = Game()
g.start_screen()

while g.running:
    g.new()
    g.GO_screen()
pygame.quit()