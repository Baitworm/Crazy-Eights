import pygame
import math

class Button: #https://thepythoncode.com/article/make-a-button-using-pygame-in-python
    
    def __init__(self, posRatio, sizeRatio, app):
        self._posRatio = posRatio
        self._sizeRatio = sizeRatio
        self._debounce = pygame.time.get_ticks()
        self._app = app
        self._beingPressed = False

    def process(self,surfaceToDraw):
        pass

    def _on_press(self):
        pass
    
    def _check_on_bounds(self,containedPos,containerPos,containerSize):
        return containerPos[0] <= containedPos[0] <= (containerPos[0] + containerSize[0]) and containerPos[1] <= containedPos[1] <= (containerPos[1] + containerSize[1])
    

class TextButton(Button):

    def __init__(self, posRatio, sizeRatio, text, outlineSize, fontName, app):
        super().__init__(posRatio, sizeRatio, app)
        self._text = text
        self._outlineSize = outlineSize
        self._fontName = fontName
        self._font = pygame.font.SysFont(self._fontName, self._app.get_width() // 25)
    
    def process(self, surfaceToDraw):
        app_height = self._app.get_height()
        app_width = self._app.get_width()
        self._font = pygame.font.SysFont(self._fontName, math.floor(self._sizeRatio * app_width))
        fontRender = self._font.render(self._text,False,(0,0,0),(139, 0, 0))
        pos = (self._posRatio[0] * app_width, self._posRatio[1] * app_height)
        surfaceToDraw.blit(fontRender,pos)
        

        mousePos = pygame.mouse.get_pos()
        if self._check_on_bounds(mousePos, pos, fontRender.get_size()):
            if pygame.mouse.get_pressed(num_buttons=3)[0] and not self._beingPressed:
                self._beingPressed = True
                if pygame.time.get_ticks() - self._debounce >= 100:
                    self._debounce = pygame.time.get_ticks()
                    self._on_press()
            else:
                if not pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self._beingPressed = False

    def update_text(self, updateTo):
        self._text = updateTo
class CreditsButton(TextButton):
    
    def __init__(self, pos, sizeRatio, text, outlineSize, font, app):
        super().__init__(pos, sizeRatio, text, outlineSize, font, app)

    def _on_press(self):
       self._app.set_gamestate(0)
        
class BackButton(TextButton):
    def __init__(self, pos, sizeRatio, text, outlineSize, font, app):
        super().__init__(pos, sizeRatio, text, outlineSize, font, app)

    def _on_press(self):
        self._app.set_gamestate(1)

class PureText(TextButton):
    def __init__(self, pos, sizeRatio, text, outlineSize, font, app):
        super().__init__(pos, sizeRatio, text, outlineSize, font, app)
    
class StartButton(TextButton):
    def __init__(self, pos, sizeRatio, text, outlineSize, font, app):
        super().__init__(pos, sizeRatio, text, outlineSize, font, app)

    def _on_press(self):
        self._app.set_gamestate(2)

class Deck(Button):
    def __init__(self, posRatio, sizeRatio, cardsGiven, app):
        super().__init__(posRatio, sizeRatio, app)
        self.image = pygame.image.load("Cover.jpg").convert()
        self.cardsInDeck = cardsGiven
        self.timesPlayerPressed = 0

    def process(self, surfaceToDraw):
        app_width = self._app.get_width()
        app_height = self._app.get_height()
        pos = (app_width * self._posRatio[0], app_height * self._posRatio[1])
        scaledImage = pygame.transform.smoothscale(self.image,(self._sizeRatio[0] * app_width, self._sizeRatio[1] * app_height))
        surfaceToDraw.blit(scaledImage,pos)
        mousePos = pygame.mouse.get_pos()
        if self._check_on_bounds(mousePos, pos, scaledImage.get_size()):
            if pygame.mouse.get_pressed(num_buttons=3)[0] and not self._beingPressed:
                self._beingPressed = True
                if pygame.time.get_ticks() - self._debounce >= 100 and self._app.get_current_turn() % 4 == 0:
                    self._debounce = pygame.time.get_ticks()
                    self._on_press()
            else:
                if not pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self._beingPressed = False

    def _on_press(self):
        # add card to player from deck
        if not self.get_cards() or self.timesPlayerPressed >= 5:
            self._app.set_current_turn(self._app.get_current_turn() + 1)
            self.timesPlayerPressed = 0
        else:
            if not self._app.get_current_screen().get_players()[0].has_playable_cards():
                self._app.get_current_screen().get_players()[0].add_to_hand(self.cardsInDeck.pop())
                self.timesPlayerPressed += 1

    def get_cards(self):
        return self.cardsInDeck

class Stock(Button): #just show what you can add
    def __init__ (self, posRatio, sizeRatio, startingCard, app):
        super().__init__(posRatio, sizeRatio, app)
        self.cardsInStock = [startingCard]
        self.image = startingCard.get_image()

    def add_card_to_stock(self,cardToAdd):
        self.cardsInStock.append(cardToAdd)
        cardToAdd.set_card_image("Not Cover")
        self.image = cardToAdd.get_image()

    def get_card(self):
            return self.cardsInStock[-1]
    
    def process(self, surfaceToDraw):
        app_width = self._app.get_width()
        app_height = self._app.get_height()
        pos = (app_width * self._posRatio[0], app_height * self._posRatio[1])
        scaledImage = pygame.transform.smoothscale(self.image,(self._sizeRatio[0] * app_width, self._sizeRatio[1] * app_height))
        surfaceToDraw.blit(scaledImage,pos)
        mousePos = pygame.mouse.get_pos()
        if self._check_on_bounds(mousePos, pos, scaledImage.get_size()):
            if pygame.mouse.get_pressed(num_buttons=3)[0] and not self._beingPressed:
                self._beingPressed = True
                if pygame.time.get_ticks() - self._debounce >= 100 and self._app.get_current_turn() % 4 == 0:
                    self._debounce = pygame.time.get_ticks()
                    self._on_press()
            else:
                if not pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self._beingPressed = False
    
    def _on_press(self):
        self._app.set_current_turn(self._app.get_current_turn()+1)
        player = self._app.get_current_screen().get_players()[0]
        player.on_turn_end()
        if player.is_hand_empty():
            self._app.reset_round(player)