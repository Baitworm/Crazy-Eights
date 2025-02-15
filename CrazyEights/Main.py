import pygame
import random
from Buttons import Deck, Stock, PureText
from Card import Card
from Screens import CreditsScreen, TitleScreen, PlayingScreen, WinnerScreen
from Player import *
import time

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (139, 0, 0)

class App: # class where the screen is set (most of this class was based on this http://pygametutorials.wikidot.com/tutorials-basic)
    
    def __init__(self,x,y): #constructor setting whether or not the app is running or not, which screen it should display, and the size of the screen displayed
        self.running = True
        self.display = None
        self._size = self._width,self._height = x,y
        """
            gameState = 0 means its on the credits screen
            gameState = 1 means its on the title screen
            gameState = 2 mean its on the play
            gameState = 3 mean its on the very end basically just quit the game
        """
        self._gameState = 1
        self._currentScreen = None #which screen should be current
        self._cardSize = (self._size[0] / 10 / self._size[0], self._size[1] / 4 / self._size[1])
        self._currentTurn = 0

    def on_init(self): # initialize all pygame modules and shows a resizable window and makes the application run
        pygame.init()
        pygame.display.set_caption('Crazy Eights')
        self.display = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE) #different mode types 
        self.running = True

    def on_loop(self):
        self.display.fill(RED)
        for i in self._currentScreen.get_buttons():
            i.process(self.display)
        if self._gameState == 2 and type(self._currentScreen) is PlayingScreen:
            for player in self._currentScreen.get_players():
                if player.get_points() > 100:
                    self.end_game()
            if self._currentTurn % 4 != 0:
                self._currentScreen.get_players()[self._currentTurn % 4].play_hand(self._currentScreen.get_stock())
        if self._gameState == 3 and type(self._currentScreen) is WinnerScreen:
            self.end_game()
        pygame.display.update()
                    
    def createDeckAndStock(self):
        suits = ["Spades",'Hearts','Clubs','Diamonds']
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        deck = []
        for suit in suits: # set the deck of cards
            for rank in ranks:
                deck.append(Card(rank, suit, self))
        random.shuffle(deck)
        stock = deck.pop()
        while stock.get_rank() == '8':
            deck.insert(len(deck)//2,stock)
            stock = deck.pop()
        
        stock.set_card_image("Not Cover")
        deckPos = (self._size[0]/ 3.5 / self._size[0], self._size[1]/ 3 /self._size[1])
        stockPos = (self._size[0] / 1.5 / self._size[0], self._size[1]/ 3 /self._size[1])
        return Deck(deckPos, self._cardSize, deck, self), Stock(stockPos, self._cardSize, stock, self)


    def run(self):
        if self.on_init() == False: # check if the program is still running
            self.running = False

        #code below is to set up the deck
        deck,stock = self.createDeckAndStock()
        
        #below are some variables for the screens (basically each gamestate has a different screen and each screen contains the actual functionality of the program)
        sizeRatio = 25/self._height
        titleStuff = TitleScreen('Title','arial', self) # set title screen
        titleStuff.add_button("Crazy Eights", ( (self._width/2 - titleStuff.get_font().size("Crazy Eights")[0]*2/3) / self._width, 0), sizeRatio)
        titleStuff.add_button("Start", ( (self._width/8 - titleStuff.get_font().size("Start")[0]/2) / self._width, (self._height*5/7 - titleStuff.get_font().size("Start")[1]/2) / self._height), sizeRatio)
        titleStuff.add_button("Credits", ( (self._width/8 - titleStuff.get_font().size("Credits")[0]/2) / self._width, (self._height*7/8 - titleStuff.get_font().size("Credits")[1]/2) / self._height), sizeRatio)
        self._currentScreen = titleStuff

        creditStuff = CreditsScreen('Credits', 'arial', self) # set credits screen
        creditStuff.add_button("Back",(0,0), sizeRatio)
        creditStuff.add_button("Card designs: https://github.com/hanhaechi/playing-cards", (self._width/ 40 /self._width, self._height/ 6 / self._height), sizeRatio)

        playingStuff = PlayingScreen('Game', 'arial', self)
        playingStuff.add_to_screen(deck)
        playingStuff.add_to_screen(stock)

        pos = (1/2 - self._cardSize[0]/2, 1 - self._cardSize[1])
        playingStuff.add_player(pos, 0,0)
        playingStuff.add_to_screen(PureText((pos[0], pos[1] - self._height/10/self._height),(self._width/20/self._width),'0',0,'arial',self))

        pos = (0, 1/2 - self._cardSize[1]/2)
        playingStuff.addAI(pos, 0, 90)
        playingStuff.add_to_screen(PureText((pos[0] + self._cardSize[0] + self._width/15/self._width, pos[1]),(self._width/20/self._width),'0',0,'arial',self))

        pos = (1/2 - self._cardSize[0]/2, 0)
        playingStuff.addAI(pos, 0, 180)
        playingStuff.add_to_screen(PureText((pos[0], pos[1] + self._cardSize[1] + self._height/20/self._height),(self._width/20/self._width),'0',0,'arial',self))

        pos = (1 - self._cardSize[0], 1/2 - self._cardSize[1]/2)
        playingStuff.addAI(pos, 0, 270)
        playingStuff.add_to_screen(PureText((pos[0] - self._width/20/self._width, pos[1]),(self._width/20/self._width),'0',0,'arial',self))

        winStuff = WinnerScreen('End Screen', 'arial', self)
        winStuff.add_to_screen(PureText((1/4 ,1/4),(self._width /20 / self._width),"Winner", 0, 'arial', self))
        winStuff.set_players(playingStuff.get_players())

        for i in range(5):
            for player in playingStuff.get_players():
                player.add_to_hand(deck.get_cards().pop())

        
        currentScreens = [creditStuff,titleStuff,playingStuff,winStuff]
        while(self.running):
            for event in pygame.event.get(): # check events and see if we need to do anything with them
                if event.type == pygame.QUIT: #stops the app from running when pygame quits
                    self.running = False
                if event.type == pygame.VIDEORESIZE: #sets the width,height, and size of the app to the event (what the user changed it to)
                    self._size = self._width,self._height = event.w,event.h
                    
            self._currentScreen = currentScreens[self._gameState]
            self.on_loop()

        pygame.quit()

    def end_game(self):
        self._gameState = 3
        min = self.get_current_screen().get_players()[0].get_points()
        index = 0
        for i in range(len(self.get_current_screen().get_players())):
            player = self.get_current_screen().get_players()[i]
            if player.get_points() < min:
                min = player.get_points()
                index = i
        if type(self.get_current_screen()) is WinnerScreen:
            self.get_current_screen().get_buttons()[0].update_text("Player" + " " + str(index + 1) +" WON!")

    def reset_round(self,player_to_exclude):
        for player in self.get_current_screen().get_players():
            if player is player_to_exclude:
                continue
            point_sum = 0
            for card in player.get_hand():
                point_sum += card.get_points()
            player.add_points(point_sum)
            player.get_hand().clear()

        for i in range(len(self.get_current_screen().get_buttons()) - 1, -1, -1):
            item = self.get_current_screen().get_buttons()[i]
            if type(item) is Deck or type(item) is Stock:
                del self.get_current_screen().get_buttons()[i]
            
            if type(item) is Player or type(item) is Ai:
                self.get_current_screen().get_buttons()[i+1].update_text(str(self.get_current_screen().get_buttons()[i].get_points()))

        new_deck, newStock = self.createDeckAndStock()
        
        for i in range(5):
            for player in self.get_current_screen().get_players():
                player.add_to_hand(new_deck.get_cards().pop())

        self.get_current_screen().get_buttons().append(new_deck)
        self.get_current_screen().get_buttons().append(newStock)

        self.set_current_turn(0)

    def set_gamestate(self,setTo):
        self._gameState = setTo
    
    def get_gamestate(self):
        return self._gameState
    
    def set_current_screen(self,setTo):
        self._currentScreen = setTo
    
    def get_current_screen(self):
        return self._currentScreen
    
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height

    def get_current_turn(self):
        return self._currentTurn
    
    def set_current_turn(self,setTo):
        self._currentTurn = setTo

    def get_card_size(self):
        return self._cardSize
    

if __name__ == "__main__" :

    theApp = App(640,400)
    theApp.run()
