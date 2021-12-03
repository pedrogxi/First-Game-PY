from game import Game

g = Game()
g.jogando = True
while g.rodando:
    g.gameLoop()