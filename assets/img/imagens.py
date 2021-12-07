import pygame
import os

INIMIGO_VERMELHO = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
INIMIGO_VERDE = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
INIMIGO_AZUL = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Carregando nave do PLAYER
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "player.png"))
# Carregando os LASERS
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
# Carregando background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background1.png")), (1200, 700))
