import pygame
from settings import *
from sprites import *
import random
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
        pygame.mixer.music.load('source/bgmusic.wav')
        pygame.mixer.music.play(-1)
        # Создаём гурппу спрайтов
        self.all_sprites = pygame.sprite.Group()
        # Создаём отдельную группу спрайтов для платформ
        self.main_platform = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.danger_plat = pygame.sprite.Group()
        self.fast_platforms1 = pygame.sprite.Group()
        self.fast_platforms2 = pygame.sprite.Group()
        self.fast_platforms3 = pygame.sprite.Group()
        # Спаун игрока
        self.player = Player(self)
        p_dang = Platform(-2000, 0, 2000, 2000, orange)
        p_main = Platform(-1000, HEIGHT - 48, 10000, 50, BLACK)

        f1 = Platform(1, 1, 1, 1, BLUE)
        f2 = Platform(2, 2, 1, 1, BLUE)
        f3 = Platform(3, 3, 1, 1, BLUE)
        # Добавление спрайта игрока в группу спрайтов
        self.all_sprites.add(self.player)
        self.all_sprites.add(p_dang, p_main)
        self.bullets = pygame.sprite.Group()
        # Спаун платформы с перечисление нужных аргументов из списка
        self.all_sprites.add(f1, f2, f3)
        self.fast_platforms1.add(f1)
        self.fast_platforms2.add(f2)
        self.fast_platforms2.add(f3)
        self.danger_plat.add(p_dang)
        self.main_platform.add(p_main)

        # Запускаем функию run() для группирования игры
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
        fast_hits1 = pygame.sprite.spritecollide(self.player, self.fast_platforms1, False)
        fast_hits2 = pygame.sprite.spritecollide(self.player, self.fast_platforms2, False)
        fast_hits3 = pygame.sprite.spritecollide(self.player, self.fast_platforms3, False)
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        hits_main = pygame.sprite.spritecollide(self.player, self.main_platform, False)
        hits_dang = pygame.sprite.spritecollide(self.player, self.danger_plat, False)

        if hits_dang:
            self.game_over_screen()

        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0


        if fast_hits1:
            self.player.pos.y = fast_hits1[0].rect.top
            self.player.vel.y = 0
            for plat in self.danger_plat:
                plat.rect.x += 2

        if fast_hits2:
            self.player.pos.y = fast_hits2[0].rect.top
            self.player.vel.y = 0


        if fast_hits3:
            self.player.pos.y = fast_hits3[0].rect.top
            self.player.vel.y = 0

            """for plat in self.danger_plat:
                plat.rect.x -= 4"""

        if hits_main:
            self.player.pos.y = hits_main[0].rect.top
            self.player.vel.y = 0

        """ПРОКРУТКА ЭКРАНА"""
        # Если игрок доходит до экрана по горизонтали, то экран прокручивается

        if self.player.rect.centerx >= 0.5 * WIDTH:
            self.player.pos.x -= abs(self.player.vel.x)
            for i in range(1000):
                i += 0.5
                for plat in self.platforms:
                    plat.rect.x -= abs(self.player.vel.x) * i
                    if plat.rect.x <= 0:
                        plat.kill()
        """if self.player.rect.centerx < WIDTH//2:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)"""

        if self.player.rect.centery <= HEIGHT//4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
        if self.player.rect.top >= 0.75 * HEIGHT + 30:
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)

        if self.player.vel.x <= 0:
            for plat in self.main_platform:
                plat.rect.x += 0.1
        if self.player.vel.x == 0:
            for plat in self.danger_plat:
                plat.rect.x += 1

        if self.player.rect.centerx >= 0.5 * WIDTH:
            for plat in self.fast_platforms1:
                plat.rect.x -= abs(self.player.vel.x)
                if plat.rect.x <= 0:
                    plat.kill()
        if self.player.rect.centerx >= 0.5 * WIDTH:
            for plat in self.fast_platforms2:
                plat.rect.x -= abs(self.player.vel.x)
                if plat.rect.x <= 0:
                    plat.kill()
        if self.player.rect.centerx >= 0.5 * WIDTH:
            for plat in self.fast_platforms3:
                plat.rect.x -= abs(self.player.vel.x)
                if plat.rect.x <= 0:
                    plat.kill()

        """while len(self.platforms) < 4:
            width = random.randint(100, 200)
            p = Platform(random.randrange(WIDTH + 20, WIDTH + 2000),
                         random.randrange(HEIGHT - 300, HEIGHT - 100),
                         width,
                         10,
                         BLACK)
            self.platforms.add(p)
            self.all_sprites.add(p)"""

        """while len(self.fast_platforms) < 2:
            width = random.randint(100, 200)
            p = Platform(random.randrange(WIDTH + 20, WIDTH + 1020),
                         random.randrange(HEIGHT - 300, HEIGHT - 100),
                         width,
                         10,
                         BLUE)
            self.fast_platforms.add(p)
            self.all_sprites.add(p)"""

        while len(self.fast_platforms1) < 1:
            p = Platform(random.randint(WIDTH + 100, WIDTH + 100),
                         HEIGHT - 150,
                         random.randint(50, 80),
                         10,
                         BLUE)
            self.fast_platforms1.add(p)
            self.all_sprites.add(p)
        while len(self.fast_platforms2) < 1:
            p = Platform(random.randint(WIDTH - 200, WIDTH + 280),
                         HEIGHT - 150,
                         random.randint(50, 80),
                         10,
                         BLUE)
            self.fast_platforms2.add(p)
            self.all_sprites.add(p)
        """while len(self.fast_platforms3) < 1:
            p = Platform(random.randint(WIDTH + 90, WIDTH + 110),
                         HEIGHT - 100,
                         random.randint(100, 200),
                         10,
                         BLUE)
            self.fast_platforms3.add(p)
            self.all_sprites.add(p)"""

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

                if event.key == pygame.K_SPACE:
                    self.bullet = Bullet(self.player.rect.centerx, self.player.rect.centery)
                    self.all_sprites.add(self.bullet)
                    self.bullets.add(self.bullet)

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
        self.playing = False


g = Game()
g.start_screen()

while g.running:

    g.new_game()
    g.game_over_screen()
pygame.quit()
