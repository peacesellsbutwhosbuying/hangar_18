import pygame
from settings import *
from sprites import *
# Импортируем значения параметров


class Game():

    """Объект игры"""

    def __init__(self):
        """Функция основынх настроек игры"""
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def new_game(self):
        """Функция новой игры"""
        # Создаём гурппу спрайтов
        self.all_sprites = pygame.sprite.Group()
        # Создаём отдельную группу спрайтов для платформ
        self.platforms = pygame.sprite.Group()
        # Спаун игрока
        self.player = Player(self)
        # Добавление спрайта игрока в группу спрайтов
        self.all_sprites.add(self.player)
        # Спаун платформы с перечисление нужных аргументов
        p1 = Platform(0, HEIGHT - 48, WIDTH, 50)
        # Добавление платформы в группы спрайтов
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        # Запускаем функию run() для группирования игры
        p2 = Platform(WIDTH//2, HEIGHT//2 + 100, 50, 10)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
        self.run_game()

    def run_game(self):
        """Функция содержит основной цикл игры"""
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            # Запуск событий
            self.events()
            # Запуск обновлений
            self.update_screen()
            # Запуск отрисовки
            self.draw()

    def update_screen(self):
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0

    def events(self):
        """ Функция основных событий игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.jump()

    def draw (self):
        """Функия отрисовки"""
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        pygame.display.flip()

    def start_screen(self):
        """Окно запуска игры"""
        pass

    def game_over_screen(self):
        """Окно Game Over"""
        pass


g = Game()
g.start_screen()

while g.running:
    g.new_game()
    g.game_over_screen()
pygame.quit()
