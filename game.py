import pygame
import random
from pygame.locals import *
from assets.img import imagens
from assets.font.fonte import fonte
from time import sleep


class Game():
    def __init__(self):
        # Variaveis
        self.rodando, self.jogando = True, False  # vamos utilizar para o looping
        self.down_key, self.up_key, self.right_key, self.left_key, self.start_key = False, False, False, False, False
        self.shoot, self.sair = False, False
        # Tela
        self.DISPLAY_W, self.DISPLAY_H = 1200, 700
        self.tela = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption("Fisrt game")

        # Taxa de atualização da tela
        self.clock = pygame.time.Clock()
        self.FPS = 30

        # Status de jogo
        self.nivel = 0
        self.vida = 5
        self.velocidade_player = 10
        self.inimigos_em_tela = []
        self.inimigos_por_fase = 5
        self.inimigo_vel = 10
        self.laser_vel = 5

        # Posição do jogador
        self.pos_jogador_x = 40
        self.pos_jogador_y = 320
        # Objeto da nave do jogador
        self.jogador = self.Jogador(
            self.pos_jogador_x, self.pos_jogador_y, vida=100)

    def gameLoop(self):

        while self.jogando:
            self.clock.tick(self.FPS)

            self.drawWindow()

            self.checkEvents()

            if self.shoot:
                print("Atirando")

            # Movimentação do jogador e Colisão com as paredes
            if self.up_key and self.pos_jogador_y - self.velocidade_player + 10 > 0:  # para cima
                self.jogador.y -= self.velocidade_player
            if self.down_key and self.pos_jogador_y + self.velocidade_player + 80 < self.DISPLAY_H:  # para baixo
                self.jogador.y += self.velocidade_player

            if self.right_key and self.pos_jogador_x + self.velocidade_player + 100 < self.DISPLAY_W:  # para direita
                self.jogador.x += self.velocidade_player
            if self.left_key and self.pos_jogador_x - self.velocidade_player - 10 > 0:  # para esquerda
                self.jogador.x -= self.velocidade_player

            # self.jogador.move_lasers(self.laser_vel, self.tela)

            self.resetKeys()

    def drawWindow(self):
        # Background
        self.tela.blit(imagens.BACKGROUND, (0, 0))

        # Desenhando o overlay do jogo
        vida_label = fonte.render(
            f"Vidas: {self.vida}", 1, (225, 225, 225))
        nivel_label = fonte.render(
            f"Nivel: {self.nivel}", 1, (225, 225, 225))

        if len(self.inimigos_em_tela) == 0:
            self.nivel += 1
            self.inimigo_vel += 1
            self.inimigos_por_fase += 5

            for i in range(self.inimigos_por_fase):
                # Nascimento aleatorio dos inimigos
                color_enemy = random.choice(["red", "blue", "green"])
                range_de_nascimento_x = random.randrange(
                    (self.DISPLAY_W + 50), 3200)

                range_de_nascimento_y = random.randrange(
                    50, (self.DISPLAY_H - 50))
                inimigos = Game.Inimigos(
                    id=i, x=range_de_nascimento_x, y=range_de_nascimento_y, color=color_enemy)
                self.inimigos_em_tela.append(inimigos)

        for inimigo in self.inimigos_em_tela[:]:
            inimigo.move(self.inimigo_vel)

            if self.colision(inimigo, self.jogador):
                self.jogador.vida -= 10
                self.inimigos_em_tela.remove(inimigo)

            if inimigo.x + inimigo.get_width() < 0:
                self.vida -= 1
                self.inimigos_em_tela.remove(inimigo)

        for inimigos in self.inimigos_em_tela:
            inimigos.draw(self.tela)

        self.jogador.draw(self.tela)  # Coloca o jogador na tela

        self.tela.blit(vida_label, (10, 10))
        self.tela.blit(nivel_label, (self.DISPLAY_W -
                       nivel_label.get_width() - 10, 10))

        pygame.display.update()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando, self.jogando = False, False

        key = pygame.key.get_pressed()

        if key[pygame.K_a]:  # Esquerda
            self.left_key = True
        if key[pygame.K_d]:  # Direita
            self.right_key = True
        if key[pygame.K_w]:  # Cima
            self.up_key = True
        if key[pygame.K_s]:  # Baixo
            self.down_key = True
        if key[pygame.K_SPACE]:
            self.shoot = True
        if key[pygame.K_ESCAPE]:
            self.sair = True

    def resetKeys(self):
        self.down_key, self.up_key, self.right_key, self.left_key, self.start_key = False, False, False, False, False
        self.shoot, self.sair = False, False

    def colision(self, objeto1, objeto2):
        """
        Retorna Verdadeiro quando um Objeto colidir com o outro

        :param objeto1: object
        :param objeto2: object
        """
        offset_x = objeto2.x - objeto1.x
        offset_y = objeto2.y - objeto1.y
        return objeto1.mask.overlap(objeto2.mask, (offset_x, offset_y)) != None

    # def lose(self):
    #     """
    #     Retorna Verdadeiro caso O plyer perca
    #     """
    #     if self.vida <= 0:
    #         return True

    #     if self.jogador.vida == 0:
    #         self.vida -= 1
    #         self.jogador.vida = 100

    class Players():
        def __init__(self, x, y, vida):
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

        # def shoot(self):
        #     if self.cooldown_counter == 0:
        #         laser = Game.Laser(self.x, self.y, self.player_laser)
        #         self.lasers_em_tela.append(laser)
        #         self.cooldown_counter = 1

        # def shootCooldown(self):
        #     if self.cooldown_counter >= self.COOLDOWN:
        #         self.cooldown_counter = 0
        #     elif self.cooldown_counter > 0:
        #         self.cooldown_counter += 1

        # def move_lasers(self, vel, tela):
        #     self.shootCooldown()
        #     for laser in self.lasers_em_tela:
        #         laser.move(vel)
        #         laser.draw(tela)

        def get_width(self):
            return self.player_img.get_width()

        def get_height(self):
            return self.player_img.get_height()

    # class Laser():
    #     def __init__(self, x, y, img):
    #         self.x = x
    #         self.y = y
    #         self.img = img
    #         self.mask = pygame.mask.from_surface(self.img)

    #     def draw(self, tela):
    #         tela.blit(self.img, (self.x, self.y))

    #     def move(self, vel):
    #         self.x -= vel

    class Jogador(Players):
        def __init__(self, x, y, vida):
            super().__init__(x, y, vida)
            self.vida = vida

            self.player_img = imagens.YELLOW_SPACE_SHIP
            self.player_laser = imagens.YELLOW_LASER
            self.mask = pygame.mask.from_surface(self.player_img)
            self.max_life = vida

        def lifebar(self, tela):
            vida = self.vida
            max_life = self.max_life
            pos_vida_vermelha = (
                self.x, self.y + self.player_img.get_height() + 10, self.player_img.get_width(), 10)
            pos_vida_verde = (self.x, self.y + self.player_img.get_height() + 10,
                              self.player_img.get_width() * (vida/max_life), 10)

            pygame.draw.rect(tela, (255, 0, 0), pos_vida_vermelha)
            pygame.draw.rect(tela, (0, 255, 0), pos_vida_verde)

        def draw(self, tela):
            super().draw(tela=tela)
            self.lifebar(tela=tela)

    class Inimigos(Players):
        def __init__(self, id, x, y, color, vida=100):
            super().__init__(x, y, vida=vida)

            # Imagens dos inimigos
            ENEMY_COLOR = {
                "red": (imagens.INIMIGO_VERMELHO, imagens.RED_LASER),
                "green": (imagens.INIMIGO_VERDE, imagens.GREEN_LASER),
                "blue": (imagens.INIMIGO_AZUL, imagens.BLUE_LASER)
            }

            self.player_img, self.player_laser = ENEMY_COLOR[color]
            self.mask = pygame.mask.from_surface(self.player_img)

        def move(self, vel):
            self.x -= vel
