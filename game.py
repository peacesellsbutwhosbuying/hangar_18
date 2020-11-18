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
        pygame.mixer.music.load('source/bgmusic.wav')
        # pygame.mixer.music.play(-1)

    def new_game(self):
        """Функция новой игры"""
        # Создаём гурппу спрайтов
        self.all_sprites = pygame.sprite.Group()
        # Создаём отдельную группу спрайтов для платформ
        self.platforms = pygame.sprite.Group()
        # Спаун игрока
        self.player = Player(self)
        self.bullets = pygame.sprite.Group()
        # Спаун платформы с перечисление нужных аргументов
        p1 = Platform(0, HEIGHT - 48, WIDTH, 50)
        p2 = Platform(WIDTH//2, HEIGHT//2 + 100, 50, 10)
        p3 = Platform(WIDTH//2, HEIGHT//4 + 100, 50, 10)
        mob1 = Mob(100, 100, 100)
        self.all_sprites.add(p1, p2, p3, mob1)
        self.platforms.add(p1, p2, p3)
        # Добавление спрайта игрока в группу спрайтов
        self.all_sprites.add(self.player)
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
        """ПРОКРУТКА ЭКРАНА"""
        # Если игрок доходит до экрана по горизонтали, то экран прокручивается
        if self.player.rect.centerx <= WIDTH // 4:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)
        if self.player.rect.centerx >= 0.75 * WIDTH:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
        if self.player.rect.centery <= HEIGHT//4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
        if self.player.rect.top >= 0.75 * HEIGHT + 30:
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)

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
        pass


g = Game()
g.start_screen()

while g.running:
    g.new_game()
    g.game_over_screen()
pygame.quit()
