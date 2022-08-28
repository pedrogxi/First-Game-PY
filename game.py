import pygame
import random
from pygame.locals import *
from assets.img import _load_imagens
from assets.font._load_font import font
from menu import MainMenu


class Game():
    def __init__(self):
        # Variaveis
        self.rodando, self.jogando = True, False  # vamos utilizar para o looping
        self.down_key, self.up_key, self.right_key, self.left_key, self.start_key = False, False, False, False, False
        self.shoot, self.sair = False, False
        # Tela
        self.DISPLAY_W, self.DISPLAY_H = 1200, 700
        self.tela = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption("Space Shoot")

        # Menu
        self.curr_menu = MainMenu(self)

        # Taxa de atualização da tela
        self.clock = pygame.time.Clock()
        self.FPS = 30

        # Status de jogo
        self.nivel = 0
        self.vida = 5
        self.velocidade_player = 6
        self.inimigos_em_tela = []
        self.inimigos_por_fase = 4
        self.inimigo_vel = 2
        self.laser_vel = 8

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
                self.jogador.shoot()    

            # Movimentação do jogador e Colisão com as paredes
            if self.up_key and self.jogador.y - self.velocidade_player + 10 > 0:  # para cima
                self.jogador.y -= self.velocidade_player
            if self.down_key and self.jogador.y + self.velocidade_player + 80 < self.DISPLAY_H:  # para baixo
                self.jogador.y += self.velocidade_player

            if self.right_key and self.jogador.x + self.velocidade_player + 100 < self.DISPLAY_W:  # para direita
                self.jogador.x += self.velocidade_player
            if self.left_key and self.jogador.x - self.velocidade_player - 10 > 0:  # para esquerda
                self.jogador.x -= self.velocidade_player

            self.jogador.moveLaserJogador(
                self.laser_vel, self.inimigos_em_tela)
            for inimigo in self.inimigos_em_tela[:]:
                inimigo.moveLaserPlayer(self.laser_vel, self.jogador)
            
            if self.jogador.vida == 0:
                self.vida -= 1
                self.jogador.vida = 100

            self.resetKeys()  
            self.lose()           

    def drawWindow(self):
        # Background
        self.tela.blit(_load_imagens.BACKGROUND, (0, 0))

        # Desenhando o overlay do jogo
        vida_label = font.render(
            f"Vidas: {self.vida}", 1, (225, 225, 225))
        nivel_label = font.render(
            f"Nivel: {self.nivel}", 1, (225, 225, 225))

        if len(self.inimigos_em_tela) == 0:
            self.nivel += 1
            self.inimigo_vel += 0.5
            self.inimigos_por_fase += 2

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

            # Inimigo
            if random.randrange(0, 2*60) == 1 and inimigo.x <= 1200:
                inimigo.shoot()

            if self.colision(inimigo, self.jogador):
                self.jogador.vida -= 30
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
    
    def drawText(self, text, size, x, y):
        font_name = 'assets/font/gameovercre1.ttf'
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.tela.blit(text_surface, text_rect)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando, self.jogando = False, False
                self.curr_menu.run_display = False

            if self.curr_menu.run_display:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.up_key = True
                    if event.key == pygame.K_DOWN:
                        self.down_key = True
                    if event.key == pygame.K_DOWN:
                        self.down_key = True   
                    if event.key == pygame.K_DOWN:
                        self.down_key = True
                    if event.key == pygame.K_RETURN:
                        self.start_key = True
                    if event.key == pygame.K_ESCAPE:
                        self.sair = True

        key = pygame.key.get_pressed()
        if self.jogando:
            if key[pygame.K_a]:  # Esquerda
                self.left_key = True
            if key[pygame.K_d]:  # Direita
                self.right_key = True
            if key[pygame.K_w]:  # Cima
                self.up_key = True
            if key[pygame.K_s]:  # Baixo
                self.down_key = True
            if key[pygame.K_SPACE]: # Atirando
                self.shoot = True
            if key[pygame.K_ESCAPE]: # Voltar
                self.jogando = False

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

    def lose(self):
        """
        Retorna Verdadeiro caso O plyer perca
        """
        lose_count = 5

        if self.vida <= 0:
            while not lose_count == 0:
                self.jogando = False
                self.checkEvents()
                self.clock.tick(1)
                self.tela.fill((0,0,0))
                lost_label = font.render(f"Voce perdeu! Voltando para o menu em: {lose_count}", 1, (255,255,255))
                self.tela.blit(lost_label, (self.DISPLAY_W/2 - lost_label.get_width()/2, 350))
                pygame.display.update()
                
                lose_count -= 1

            self.curr_menu.run_display = True
            self.jogando = False

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

        def shoot(self):
            if self.cooldown_counter == 0:
                laser = Game.Laser(self.x, self.y, self.player_laser)
                self.lasers_em_tela.append(laser)
                self.cooldown_counter = 1

        def moveLaserPlayer(self, vel, obj):
            self.shootCooldown()
            for laser in self.lasers_em_tela:
                laser.move(vel)
                if laser.offScreen(Game().DISPLAY_W):
                    self.lasers_em_tela.remove(laser)
                elif laser.collide(obj):
                    obj.vida -= 10
                    self.lasers_em_tela.remove(laser)

        def shootCooldown(self):
            if self.cooldown_counter >= self.COOLDOWN:
                self.cooldown_counter = 0
            elif self.cooldown_counter > 0:
                self.cooldown_counter += 1

        def get_width(self):
            return self.player_img.get_width()

        def get_height(self):
            return self.player_img.get_height()

    class Laser():
        def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, tela):
            tela.blit(self.img, (self.x, self.y))

        def move(self, vel):
            self.x -= vel

        def offScreen(self, width):
            return not(self.x <= width and self.x >= 0)

        def collide(self, obj):
            return Game.colision(self, objeto1=self, objeto2=obj)

    class Jogador(Players):
        def __init__(self, x, y, vida):
            super().__init__(x, y, vida)
            self.vida = vida

            self.player_img = _load_imagens.YELLOW_SPACE_SHIP
            self.player_laser = _load_imagens.YELLOW_LASER
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

        def moveLaserJogador(self, vel, objs):
            self.shootCooldown()
            for laser in self.lasers_em_tela:
                laser.move(-vel)
                if laser.offScreen(Game().DISPLAY_W):
                    self.lasers_em_tela.remove(laser)
                else:
                    for inimigo in objs:
                        if laser.collide(inimigo):
                            objs.remove(inimigo)
                            if laser in self.lasers_em_tela:
                                self.lasers_em_tela.remove(laser)

        def draw(self, tela):
            super().draw(tela=tela)
            self.lifebar(tela=tela)

    class Inimigos(Players):
        def __init__(self, id, x, y, color, vida=100):
            super().__init__(x, y, vida=vida)

            # Imagens dos inimigos
            ENEMY_COLOR = {
                "red": (_load_imagens.INIMIGO_VERMELHO, _load_imagens.RED_LASER),
                "green": (_load_imagens.INIMIGO_VERDE, _load_imagens.GREEN_LASER),
                "blue": (_load_imagens.INIMIGO_AZUL, _load_imagens.BLUE_LASER)
            }

            self.player_img, self.player_laser = ENEMY_COLOR[color]
            self.mask = pygame.mask.from_surface(self.player_img)

        def move(self, vel):
            self.x -= vel

        def shoot(self):
            if self.cooldown_counter == 0:
                laser = Game.Laser(self.x-20, self.y, self.player_laser)
                self.lasers_em_tela.append(laser)
                self.cooldown_counter = 1
