import pygame
import os
import random
from pygame.locals import* #

pygame.font.init()


WIDTH, HEIGHT = 1200, 700
TELA = pygame.display.set_mode((WIDTH, HEIGHT)) #TAMANHO DA TELA
pygame.display.set_caption("Jogo1") #TÍTULO DO GAME

# Imagens dos inimigos
INIMIGO_VERMELHO = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
INIMIGO_VERDE = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
INIMIGO_AZUL = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "player.png"))
# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
# Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background1.png")), (WIDTH, HEIGHT))

class Laser(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, janela):
        janela.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.x -= vel
       

    def off_screen(self, width):
        return not(self.x <= width and self.x >= 0)

    def collision(self, obj):
        return collide(self, obj)




class Players(): #naves INIMIGAS E DO JOGADOR COMPARTILHAM PROPRIEDADES SEMELHANTES, PORTANTO, PODEMOS REUTILIZA-LAS.
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x #DEFININDO OS PARAMETROS DE POSICIONAMENTO HORIZONTAL
        self.y = y #PARAMETROS VERTICAIS
        self.health = health #LIFEBAR
        self.player_img = None
        self.laser_img = None #OU self.bullets.img
        self.lasers = []
        self.cool_down_counter = 0
        

    def draw(self, janela):
       janela.blit(self.player_img, (self.x, self.y))
       for laser in self.lasers:
           laser.draw(janela)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.player_img.get_width()

    def get_height(self):    
        return self.player_img.get_height()

class Player(Players):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health) #classe pai 
        self.player_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.player_img) #.mask É UMA MASCARA QUE PPTERMIE REALIZAR A COLISÃO PERFEITA DE PIXELS
        self.max_health = health
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, janela):
        super().draw(janela)
        self.healthbar(janela)

    def healthbar(self, janela):
        pygame.draw.rect(janela, (255,0,0), (self.x, self.y + self.player_img.get_height() + 10, self.player_img.get_width(), 10))
        pygame.draw.rect(janela, (0,255,0), (self.x, self.y + self.player_img.get_height() + 10, self.player_img.get_width() * (self.health/self.max_health), 10))


class Inimigo(Players):
        COLOR_MAP = {
                    "red": (INIMIGO_VERMELHO, RED_LASER),
                    "green": (INIMIGO_VERDE, GREEN_LASER),
                    "blue": (INIMIGO_AZUL, BLUE_LASER)
                    }

        def __init__(self, x, y, color, health=100):
            super().__init__(x, y, health)
            self.player_img, self.laser_img = self.COLOR_MAP[color]
            self.mask = pygame.mask.from_surface(self.player_img)
        
        def move(self, SPEED):
            self.x -= SPEED 
        
        def shoot(self):
             if self.cool_down_counter == 0:
                laser = Laser(self.x-20, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main(): #LOOP PRINCIPAL
    run = True #JOGO RODANDO
    FPS = 30
    SPEED = 7 #VELOCIDADE DO PLAYER #player_vel
    nivel = 0
    vidas = 5
    fonte = pygame.font.Font('assets/fonte/gameovercre1.ttf', 40) #DEFININDO FONTE E TAMANHO DA FONTE
    lost_font = pygame.font.Font('assets/fonte/gameovercre1.ttf', 50)
    
    inimigos = []
    comprimento_fase = 5
    inimigo_vel = 1

    laser_vel = 5

    player = Player(40, 320) #POSICIONAMENTO DO PLAYER NO CANTO ESQUERDO DA TELA

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def draw_window(): 
        TELA.blit(BACKGROUND, (0,0)) #blit DEFINE A CAMADA QUE DESIGINAMOS A IMAGEM COM UMA COORDENADA, SENDO O "0" COMO A PRIMEIRA
        vidas_label = fonte.render(f"Vidas: {vidas}", 1, (225, 225, 225)) #TEXTO E SUA COR
        nivel_label = fonte.render(f"Nivel: {nivel}", 1, (225, 225, 225)) #TEXTO E SUA COR
        
        #pygame.display.update() #ATUALIZA O LOOP DE ACORDO COM O FRAME RATE DEFINIDO
        
        TELA.blit(vidas_label, (10, 10)) #LOCALIZADA NO CANTO SUPERIOR ESQUERDO DA TELA, 10 PIXELS ABAIXO E 10 PIXELS PRA DIREITA
        TELA.blit(nivel_label, (WIDTH - nivel_label.get_width() - 10, 10)) #É DIFICIL SABER A LOCALIZAÇÃO EXATA DO CANTO DIREITO, ENTAO, USANDO MATEMATICA, BASTA SUBTRARIR A ÁREA DA JANELA

        for inimigo in inimigos:
            inimigo.draw(TELA)

        player.draw(TELA)
        
        if lost:
            lost_label = lost_font.render("Voce perdeu! Pressione Esc para SAIR", 1, (255,255,255))
            TELA.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

                    
        pygame.display.update()

    while run: #DEFININDO O LOOP
        clock.tick(FPS)
        draw_window()
        
        if vidas <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:    
            if lost_count > FPS * 3:
                run = False
            else:
                continue    

        if len(inimigos) ==0:
            nivel += 1
            comprimento_fase += 5
            for i in range(comprimento_fase):
                inimigo = Inimigo(random.randrange(WIDTH, 2400), random.randrange(-200, HEIGHT), random.choice(["red", "blue", "green"]))#AJUSTAR O NASCIMENTO ALEATÓRIO NA POSIÇÃO X
                inimigos.append(inimigo)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                

        key = pygame.key.get_pressed() #NA VERSÃO 0.0.1 UTILIZAMOS O: [0] COMO x, E O: [1] COMO y         
        if key[pygame. K_a] and player.x - SPEED > 0:  #LIMITE DAS BORDAS
                player.x -= SPEED # esquerda
        if key[pygame. K_d] and player.x + SPEED + 100 < WIDTH: #LIMITE DAS BORDAS
                player.x += SPEED # direita
        if key[pygame. K_w] and player.y - SPEED > 0: #LIMITE DAS BORDAS
                player.y -= SPEED #cima          
        if key[pygame. K_s] and player.y + SPEED + 100 < HEIGHT: #LIMITE DAS BORDAS
                player.y += SPEED # baixo
        if key[pygame.K_SPACE]:
            player.shoot()        
        
            

        for inimigo in inimigos[:]:
            inimigo.move(inimigo_vel)
            inimigo.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                inimigo.shoot()

            if collide(inimigo, player):
                player.health -= 10
                inimigos.remove(inimigo)
            elif inimigo.x + inimigo.get_width() < 0:
                vidas -=1
                inimigos.remove(inimigo)
                

        player.move_lasers(-laser_vel, inimigos)

                   
main()
