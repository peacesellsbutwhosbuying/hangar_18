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
        # Спаун игрока
        self.player = Player(self)
        p_dang = Platform(-2000, 0, 2000, 2000, orange)
        p_main = Platform(-1000, HEIGHT - 48, 10000, 50, BLACK)
        p1 = Platform(1000, HEIGHT - 150, 50, 10, BLACK)
        p2 = Platform(1, 1, 0, 0, BLACK)
        p3 = Platform(2, 2, 0, 0, BLACK)
        p4 = Platform(2, 2, 0, 0, BLACK)
        p5 = Platform(2, 2, 0, 0, BLACK)
        p6 = Platform(2, 2, 0, 0, BLACK)

        # Добавление спрайта игрока в группу спрайтов
        self.all_sprites.add(self.player)
        self.all_sprites.add(p_dang, p_main)
        self.bullets = pygame.sprite.Group()
        # Спаун платформы с перечисление нужных аргументов из списка
        self.platforms.add(p1, p2, p3, p4, p5, p6)
        self.all_sprites.add(p1, p2, p3, p4, p5, p6)
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

        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        hits_main = pygame.sprite.spritecollide(self.player, self.main_platform, False)
        hits_dang = pygame.sprite.spritecollide(self.player, self.danger_plat, False)

        if hits_dang:
            self.game_over_screen()

        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0
            self.player.vel.x = 0.0000000002
        if hits_main:
            self.player.pos.y = hits_main[0].rect.top
            self.player.vel.y = 0




        """ПРОКРУТКА ЭКРАНА"""
        # Если игрок доходит до экрана по горизонтали, то экран прокручивается

        if self.player.rect.centerx >= 0.5 * WIDTH:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
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
                plat.rect.x += 2
        if self.player.vel.x <= 0.0000000002:
            for plat in self.danger_plat:
                plat.rect.x += 2

        while len(self.platforms) < 2:
            width = random.randint(50, 100)
            p = Platform(random.randrange(WIDTH + 20, WIDTH + 520, 100),
                         HEIGHT - 125,
                         width,
                         100,
                         BLACK)
            self.platforms.add(p)
            self.all_sprites.add(p)



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
