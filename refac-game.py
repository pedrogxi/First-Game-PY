import pygame
from assets.img import _load_imagens as img


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.runing = True
        self.window_size = self.width, self.height = 1200, 700

        self.FPS = 27

        # instanciando um novo objeto de Clock
        self.clock = pygame.time.Clock()

        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Space Shoot")

        self.bg_speed = 5
        self.bg = Background(self.window, img.STARS, self.bg_speed)


    def game_loop(self):
        while self.runing:
            self.clock.tick(self.FPS)

            self.render_window()

            self.check_events()

    def render_window(self):
        self.window.blit(img.BACKGROUND, (0,0))

        self.bg.update()
        self.bg.render()

        pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            # se clicar no x da janela, a janela vai fechar
            if event.type == pygame.QUIT:
                self.runing = False


class Background():
    def __init__(self, window, bgimage, move_speed: int = 1.4) -> None:
        self.window = window
        self.image = bgimage
        self.rect_bg_image = self.image.get_rect()
        self.rect_bg_image_width = self.rect_bg_image.width

        self.x = self.rect_bg_image.width
        self.y = 0

        self.moving_speed = move_speed

    def update(self):
        # faz com que a imagem se mova da direita para esquerda
        self.x -= self.moving_speed
        
        # faz com que o x da imagem resete se ela tiver chegado ao fim
        if self.x <= - self.rect_bg_image_width:
            self.x = self.rect_bg_image_width
        
    def render(self):
        self.window.blit(self.image, (self.x, self.y))


game = Game()
game.game_loop()
