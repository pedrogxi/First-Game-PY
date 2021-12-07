from game import Game

g = Game()
# g.jogando = True
while g.rodando:
    g.curr_menu.displayMenu()
    g.gameLoop()