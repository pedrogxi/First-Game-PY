import pygame
from assets.img import imagens

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.runing = True
        self.window_size = self.width, self.height = 1200, 700

        self.FPS = 27

        self.bg_x = 0
        self.bg_x2 = 0

        # instanciando um novo objeto de Clock        
        self.clock = pygame.time.Clock()

        self.windown = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Space Shoot")

    def game_loop(self):
        while self.runing:
            self.clock.tick(self.FPS)

            self.draw_window()

            self.check_events()

    def draw_window(self):
        

        pygame.display.update()
    
    def move_backgounf(self):
        self.bg_x = -1.4        
        self.windown.blit(imagens.BACKGROUND, (0,0))
        self.window.blit(imagens.STARS)

    def check_events(self):
        for event in pygame.event.get():
                # se clicar no x da janela, a janela vai fechar
                if event.type == pygame.QUIT:
                    self.runing = False

game = Game()
game.game_loop()