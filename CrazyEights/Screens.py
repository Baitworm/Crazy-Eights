import pygame
from Player import Player,Ai
from Buttons import *

class Screen(object):

    def __init__(self, name, font_name ,app):
        self._name = name
        self._buttons = []
        self._font_name = font_name
        self._app = app
        self._font = pygame.font.SysFont(self._font_name,25)
    
    def add_button(self, type, posRatios, sizeRatios):
        pass

    def get_sprites(self):
        return self._buttons
    
    def get_font(self):
        return self._font
    
    def get_buttons(self):
        return self._buttons
    
class TitleScreen(Screen):

    def __init__(self, name, font, app):
        super().__init__(name,font, app)

    def add_button(self, type, posRatios, sizeRatios):
        btn = PureText(posRatios, sizeRatios, "Crazy Eights", 3, self._font_name, self._app)
        if type == 'Credits':
            btn = CreditsButton(posRatios, sizeRatios,"Credits",3,self._font_name, self._app)
        else:
            if type == 'Start':
                btn = StartButton(posRatios, sizeRatios,type, 3, self._font_name, self._app)
        self._buttons.append(btn)
        
        
class CreditsScreen(Screen):
    def __init__(self, name, font, app):
        super().__init__(name,font, app)

    def add_button(self, type, pos, sizeRatios):
        btn = PureText(pos, sizeRatios, type, 1, self._font_name, self._app)

        if type == 'Back':
            btn = BackButton(pos, sizeRatios, "←", 1, self._font_name, self._app)
                
        self._buttons.append(btn)

class PlayingScreen(Screen):
    def __init__(self, name, font, app):
        super().__init__(name, font, app)
        self._players = []

    def add_to_screen(self,whatToAdd):
        self._buttons.append(whatToAdd)

    def add_player(self, pos, amountPts, rotation): # figure out positions later
        self._players.append(Player(amountPts, rotation, pos, self._app))
        self._buttons.append(self._players[-1])

    def addAI(self,pos,amountPts, rotation):
        self._players.append(Ai(amountPts, rotation, pos, self._app))
        self._buttons.append(self._players[-1])
        
    def get_players(self):
        return self._players
        
    def get_stock(self):
        for button in self._buttons:
            if type(button) is Stock:
                return button
        return None
    
    def get_deck(self):
        for button in self._buttons:
            if type(button) is Deck:
                return button
        return None
    
class WinnerScreen(Screen):
    def __init__(self, name, font, app):
        super().__init__(name, font, app)
        self._players = []
    def add_to_screen(self,whatToAdd):
        self._buttons.append(whatToAdd)
        
    def get_players(self):
        return self._players
    
    def set_players(self, setTo):
        self._players = setTo