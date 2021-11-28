import pygame
import os


class Game():
    def __init__(self):
        # Constantes do jogo
        self.rodando, self.jogando = True, False  # vamos utilizar para o looping
        self.down_key, self.up_key, self.right_key, self.left_key, self.start_key = False, False, False, False, False
        # Tela
        self.DISPLAY_W, self.DISPLAY_H = 1200, 700
        self.tela = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption("Fisrt game")

        # Taxa de atualização da tela
        self.clock = pygame.time.Clock()
        self.FPS = 30

        # Font
        self.fonte = pygame.font.Font('assets/fonte/gameovercre1.ttf', 40)

        # Carregando imagem dos INIMIGOS
        self.INIMIGO_VERMELHO = pygame.image.load(
            os.path.join("assets", "pixel_ship_red_small.png"))
        self.INIMIGO_VERDE = pygame.image.load(
            os.path.join("assets", "pixel_ship_green_small.png"))
        self.INIMIGO_AZUL = pygame.image.load(
            os.path.join("assets", "pixel_ship_blue_small.png"))
        # Carregando nave do PLAYER
        self.YELLOW_SPACE_SHIP = pygame.image.load(
            os.path.join("assets", "player.png"))
        # Carregando os LASERS
        self.RED_LASER = pygame.image.load(
            os.path.join("assets", "pixel_laser_red.png"))
        self.YELLOW_LASER = pygame.image.load(
            os.path.join("assets", "pixel_laser_yellow.png"))
        self.GREEN_LASER = pygame.image.load(
            os.path.join("assets", "pixel_laser_green.png"))
        self.BLUE_LASER = pygame.image.load(
            os.path.join("assets", "pixel_laser_blue.png"))
        # Carregando background
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(
            os.path.join("assets", "background1.png")), (self.DISPLAY_W, self.DISPLAY_H))

        # Status de jogo
        self.nivel = 0
        self.vida = 5
        self.inimigos_em_tela = []
        self.inimigo_vel = 1
        self.laser_vel = 5

    def gameLoop(self):

        while self.jogando:
            self.clock.tick(self.FPS)

            self.drawWindow()

            self.checkEvents()
            if self.start_key:
                self.jogando = False


            self.resetKeys()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando, self.jogando = False, False

            if event.type == pygame.KEYDOWN:

                if event.type == pygame.K_RETURN:
                    self.start_key = True
                if event.type == pygame.K_UP:
                    self.up_key = True
                if event.type == pygame.K_DOWN:
                    self.down_key = True
                if event.type == pygame.K_RIGHT:
                    self.right_key = True
                if event.type == pygame.K_LEFT:
                    self.left_key = True

    def drawWindow(self):
        player = self.Jogador(x=40, y=320)

        self.tela.blit(self.BACKGROUND, (0, 0))

        vida_label = self.fonte.render(
            f"Vidas: {self.vida}", 1, (225, 225, 225))
        nivel_label = self.fonte.render(
            f"Nivel: {self.vida}", 1, (225, 225, 225))

        self.tela.blit(vida_label, (10, 10))
        self.tela.blit(nivel_label, (self.DISPLAY_W -
                       nivel_label.get_width() - 10, 10))

        player.draw(self.tela) # Coloca o jogador na tela

        pygame.display.update()

    def resetKeys(self):
        self.down_key, self.up_key, self.right_key, self.left_key, self.start_key = False, False, False, False, False

    class Players():
        def __init__(self, x, y, vida=100):
            self.x, self.y = x, y
            self.vida = vida
            self.lasers_em_tela = []
            # Imagens do player/inimigo em questão
            self.player_img = None
            self.player_laser = None
            # Tempo em que os inimigos aparecem na tela
            self.COOLDOWN = 30
            self.cooldown_counter = 0

        def draw(self, tela):
            tela.blit(self.player_img, (self.x, self.y))

            for laser in self.lasers_em_tela:
                laser.draw(tela)

        def getPosision(self):
            """
            Retorna um dicionario com a posição do objeto em questão
            """
            pos = {
                "x": self.player_img.get_width(),
                "y": self.player_laser.get_height()
            }
            return pos

    class Jogador(Players):
        def __init__(self, x, y, vida=100):
            super().__init__(x, y, vida)
            img_player = Game()
            self.player_img = img_player.YELLOW_SPACE_SHIP
            self.player_laser = img_player.YELLOW_LASER
            self.mask = pygame.mask.from_surface(self.player_img)
            self.max_life = vida

        def healthbar(self, tela):
            pos = super().getPosision()

            pygame.draw.rect(tela, (255, 0, 0),
                             (self.x, self.y + pos["y"] + 10, pos["x"], 10))
            pygame.draw.rect(tela, (0, 255, 0), (self.x, self.y +
                             pos["y"] + 10, pos["x"] * (self.vida/self.max_health), 10))

        def draw(self, tela):
            super().draw(tela=tela)
            self.healthbar(tela=tela)
