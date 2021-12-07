import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -120

    def drawCursor(self):
        self.game.drawText("*", 30, self.cursor_rect.x, self.cursor_rect.y)

    def blitScreen(self):
        self.game.tela.blit(self.game.tela, (0, 0))
        pygame.display.update()
        self.game.resetKeys


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = "Start"
        self.starx, self.starty = self.mid_w, self.mid_h + 50
        self.optx, self.opty = self.mid_w, self.mid_h + 100
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.cursor_rect.midtop = (self.starx + self.offset, self.starty)

    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            self.checkInput()
            self.game.tela.fill((0,0,0))
            self.game.drawText("Menu Principal", 56, self.mid_w, self.mid_h / 2 - 20)
            self.game.drawText("Start Game", 35, self.starx, self.starty)
            self.game.drawText("Options", 35, self.optx, self.opty)
            self.game.drawText("Credits", 35, self.creditsx, self.creditsy)
            self.drawCursor()
            self.blitScreen()
            self.game.resetKeys()
        
    def moveCursor(self):
        if self.game.down_key:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optx + self.offset, self.opty)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy) 
                self.state = "Credits" 
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.starx + self.offset, self.starty)
                self.state = "Start"
            
        if self.game.up_key:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.starx + self.offset, self.starty) 
                self.state = "Start" 
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optx + self.offset, self.opty)
                self.state = "Options"
        
    def checkInput(self):
        self.moveCursor()
        if self.game.start_key:
            if self.state == "Start":
                self.game.jogando = True
            elif self.state == "Options":
                pass
            elif self.state == "Credits":
                pass
            self.run_display = False
