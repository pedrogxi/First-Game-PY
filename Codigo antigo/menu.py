import pygame

class Menu():

    def __init__(self):
        # Definindo Constantes e nome do jogo
        self.WIDTH, self.HEIGHT =  1200, 700 
        self.tela = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Jogo 1")

    
    def start(self):
        WIDTH, HEIGHT = 1200, 700

        pygame.init()
        pygame.display.set_mode()


jogo = Menu()


