# Импортируем значения параметров
import pygame
from settings import *
from sprites import *
import random
from os import path


class Game():
    """Объект игры"""
    def __init__(self):
        """Функция основынх настроек игры"""
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_icon(pygame.image.load('source/icon.jpg'))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()
        self.score = 0

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, hs_file), 'w')as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new_game(self):
        """Функция новой игры"""
        self.score = 0
        pygame.mixer.music.load('source/bgmusic.wav')
        pygame.mixer.music.play(-1)
        # Создаём гурппу спрайтов
        self.player = Player(self)
        self.all_sprites = pygame.sprite.Group()
        self.pl = pygame.sprite.Group()
        self.pl.add(self.player)
        # Создание группы спрайтов
        self.main_platform = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.danger_plat = pygame.sprite.Group()
        self.fast_platforms = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.vents = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()

        p_dang = Platform(-2000, 0)
        p_main = MPlatform(-1000, HEIGHT - 48, 10000, 50, (231, 243, 247 ))
        f1 = Platform(1, 1)
        f2 = Platform(2, 2)
        f3 = Platform(3, 3)
        m1 = Mob(700, -1000)
        v1 = Vent(1, 1)
        # Добавление спрайтов в группы
        self.fast_platforms.add(f1, f2, f3)
        self.all_sprites.add(f1, f2, f3, m1)
        self.mobs.add(m1)
        self.all_sprites.add(p_dang, p_main, v1)
        self.bullets = pygame.sprite.Group()
        self.danger_plat.add(p_dang)
        self.main_platform.add(p_main)
        self.vents.add(v1)
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
        self.pl.update()
        fast_hits = pygame.sprite.spritecollide(self.player, self.fast_platforms, False)
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        hits_main = pygame.sprite.spritecollide(self.player, self.main_platform, False)
        hits_dang = pygame.sprite.spritecollide(self.player, self.mobs, False)
        for mob in self.mobs:
            m_gits = pygame.sprite.spritecollide(mob, self.bullets, False)
            if m_gits:
                mob.kill()
                for bullet in self.bullets:
                    bullet.kill()
                self.score += 10

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

            for mob in self.mobs:
                mob.rect.x -= 10
                if mob.rect.x <= 0:
                    mob.kill()

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
                    self.score += 10
            for vent in self.vents:
                vent.rect.x -= abs(self.player.vel.x)
                if vent.rect.x < 0:
                    vent.kill()
            for d in self.doors:
                d.rect.x -= abs(self.player.vel.x)
                if d.rect.x < 0:
                   d.kill()

        while len(self.fast_platforms) < 1:
            p = Platform(WIDTH,
                         HEIGHT - 125)
            self.fast_platforms.add(p)
            self.all_sprites.add(p)

        while len(self.fast_platforms) < 2:
            p = Platform(random.randint(WIDTH + 300, WIDTH + 600),
                         HEIGHT - 125)
            self.fast_platforms.add(p)
            self.all_sprites.add(p)

        while len(self.mobs) < 1:
            m = Mob(random.randrange(WIDTH + 100, WIDTH + 200),
                    random.randrange(HEIGHT - 300, HEIGHT - 200))
            self.mobs.add(m)
            self.all_sprites.add(m)

        while len(self.vents) < 1:
            v = Vent(random.randint(WIDTH + 1000, WIDTH + 5000), random.randint(10, 200))
            self.vents.add(v)
            self.all_sprites.add(v)
        while len(self.doors) < 1:
            d = Door(random.randint(WIDTH + 1000, WIDTH + 5000), 476)
            self.doors.add(d)
            self.all_sprites.add(d)

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
                    self.player.atack()
                    self.bullet = Bullet(self.player.rect.centerx, self.player.rect.centery)
                    self.all_sprites.add(self.bullet)
                    self.bullets.add(self.bullet)

    def draw (self):
        """Функия отрисовки"""
        self.screen.blit(pygame.image.load('source/back_front.png'), (0, 0))
        self.all_sprites.draw(self.screen)
        self.pl.draw(self.screen)
        self.draw_text(str(self.score), 22, BLACK,  WIDTH - 100, 50)

        pygame.display.flip()

    def start_screen(self):
        """Окно запуска игры"""
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("UP or W to jump\n SPACE to attack", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to RUN!", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH//2, 30)
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
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH // 2, 55)

        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGHSCORE!!!", 22, WHITE, WIDTH//2, 30)
            with open(path.join(self.dir, hs_file), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH // 2, HEIGHT/2 + 30)
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
