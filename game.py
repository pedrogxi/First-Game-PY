import pygame


class Game():
    def __init__(self):
        self.rodando, self.jogando = True, False
        self.down_key, self.up_key, self.right_key, self.left_key = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_W = 1200, 700
