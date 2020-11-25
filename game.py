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
        self.font_name = pygame.font.match_font(FONT_NAME)

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
        self.fast_platforms = pygame.sprite.Group()
        # Спаун игрока
        self.player = Player(self)
        p_dang = Platform(-2000, 0, 2000, 2000, orange)
        p_main = Platform(-1000, HEIGHT - 48, 10000, 50, BLACK)

        f1 = Platform(1, 1, 1, 1, BLUE)
        f2 = Platform(2, 2, 1, 1, BLUE)
        f3 = Platform(3, 3, 1, 1, BLUE)
        # Добавление спрайта игрока в группу спрайтов
        self.all_sprites.add(self.player)
        self.fast_platforms.add(f1, f2, f3)
        self.all_sprites.add(f1, f2, f3)
        self.all_sprites.add(p_dang, p_main)
        self.bullets = pygame.sprite.Group()
        # Спаун платформы с перечисление нужных аргументов из списка
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
        fast_hits = pygame.sprite.spritecollide(self.player, self.fast_platforms, False)
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        hits_main = pygame.sprite.spritecollide(self.player, self.main_platform, False)
        hits_dang = pygame.sprite.spritecollide(self.player, self.danger_plat, False)

        if hits_dang:
            self.game_over_screen()

        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0


        if fast_hits:
            self.game_over_screen()

        if hits_main:
            self.player.pos.y = hits_main[0].rect.top
            self.player.vel.y = 0

        """ПРОКРУТКА ЭКРАНА"""
        # Если игрок доходит до экрана по горизонтали, то экран прокручивается
        if self.player.rect.centerx >= 0.5 * WIDTH:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)

        #if self.player.vel.x <= 0:
        for plat in self.main_platform:
            plat.rect.x += 0.1

        #if self.player.vel.x <= 0:
        for plat in self.danger_plat:
            plat.rect.x += 0

        if self.player.rect.centerx >= 0.5 * WIDTH:
            for plat in self.fast_platforms:
                plat.rect.x -= abs(self.player.vel.x)
                if plat.rect.x <= 0:
                    plat.kill()

        while len(self.fast_platforms) < 1:
            p = Platform(WIDTH,
                         HEIGHT - 125,
                         random.randint(50, 100),
                         random.randint(100, 250),
                         BLACK)
            self.fast_platforms.add(p)
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
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrow UP or W to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to RUN!", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def game_over_screen(self):
        """Окно Game Over"""
        self.playing = False
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrow UP or W to JUMP DuDe!", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to RUN AGAIN!", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        pygame.mixer.music.pause()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.start_screen()

while g.running:

    g.new_game()
pygame.quit()
