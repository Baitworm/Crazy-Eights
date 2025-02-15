import pygame,math

from Buttons import PureText
class Player:
    def __init__(self, points, rotation, posRatio, app):
        self._points = 80
        self._posRatio = posRatio
        self._rotation = rotation
        self._app = app
        self._hand = []
        self._attempting_to_play = []
        self._debounce = pygame.time.get_ticks()
        self._beingPressed = False

    def add_to_hand(self,toAdd):
        self._hand.append(toAdd)

    def has_playable_cards(self):
        stock = self._app.get_current_screen().get_stock()
        for card in self._hand:
            if card.playable(stock.get_card()):
                return True
        return False
    
    def find_card_in_playing_hand(self,cardToFind):
        for card in self._attempting_to_play:
            if card.__eq__(cardToFind):
                return True
            
        return False
    
    def process(self, surfaceToDraw):
        mousePos = pygame.mouse.get_pos()
        cardSize = self._app.get_card_size()
        app_width = self._app.get_width()
        app_height = self._app.get_height()
        spacing = cardSize[0] * app_width/2 #self.app.cardSize[0] * self.app.width / len(self.hand)
        x = app_width * self._posRatio[0]
        y = app_height * self._posRatio[1]
        
        if self._app.get_current_turn() % 4 == 0:
            trianglePoint = [(app_width * (self._posRatio[0] - .025), app_height * (self._posRatio[1] - .05)), (app_width * (self._posRatio[0] - .075), app_height * (self._posRatio[1] - .05)), (app_width * (self._posRatio[0] - .05),y)]
            pygame.draw.polygon(surfaceToDraw,(255,200,0),trianglePoint)
        for i in range(math.ceil(len(self._hand)/-2),math.ceil(len(self._hand)/2)):
            height,width = cardSize[1] * app_height, cardSize[0] * app_width
            try:
                cardIndex = i + math.floor(len(self._hand)/2)
                card = self._hand[cardIndex]
            except:
                break
            
            sizedImage = pygame.transform.smoothscale(card.get_image(),(width, height))
            rotatedImage = pygame.transform.rotate(sizedImage,self._rotation)
            
            
            if self._rotation % 180 == 0:
                x = app_width * self._posRatio[0] + spacing * i
            else:
                y = app_height * self._posRatio[1] + spacing * i
            
            if self.find_card_in_playing_hand(card):
                surfaceToDraw.blit(rotatedImage,(x, y - 10))
            else:
                surfaceToDraw.blit(rotatedImage,(x, y))
            if self.hovering(mousePos, (x,y), (width,height), spacing, card) and self._app.get_current_turn() % 4 == 0:
                if pygame.mouse.get_pressed(num_buttons=3)[0] and not self._beingPressed:
                    self._beingPressed = True
                    if pygame.time.get_ticks() - self._debounce >= 100:
                        self._debounce = pygame.time.get_ticks()
                        self._on_press(cardIndex)
                else:
                    if not pygame.mouse.get_pressed(num_buttons=3)[0]:
                        self._beingPressed = False
            
    def _on_press(self, indexCard):
        stock = self._app.get_current_screen().get_stock()
        curCard = self._hand[indexCard]
        if not self.find_card_in_playing_hand(curCard):
            if len(self._attempting_to_play) == 0:
                if curCard.playable(stock.get_card()):
                    self._attempting_to_play.append(curCard)
            for card in self._attempting_to_play:
                if curCard.is_same_rank(card):
                    self._attempting_to_play.append(curCard)
                    break
        else:
            self._attempting_to_play.remove(curCard)
        
    def hovering(self, mousePos, areaPos, areaSize, spacing, curCard):
        if self.__str__().__eq__("I am AI"):
            return False
        
        x_condition,y_condition = False,areaPos[1] <= mousePos[1] <= areaPos[1] + areaSize[1] 

        if not curCard.__eq__(self._hand[-1]):
            x_condition = areaPos[0] <= mousePos[0] <= areaPos[0] + spacing
        else:
            x_condition = areaPos[0] <= mousePos[0] <= areaPos[0] + areaSize[0]

        return x_condition and y_condition
    
    def on_turn_end(self):
        for card in self._attempting_to_play:
            for i in range(len(self._hand) - 1, -1, -1):
                if self._hand[i].__eq__(card):
                    self._hand.pop(i)
        self._attempting_to_play.clear() 

    def get_points(self):
        return self._points
    
    def add_points(self,toAdd):
        self._points += toAdd

    def get_hand(self):
        return self._hand
    
    def is_hand_empty(self):
            return not self._hand 
class Ai(Player):
    def __init__(self, points, rotation, posRatio, app):
        super().__init__(points, rotation, posRatio, app)

    def process(self, surfaceToDraw):
        app_width = self._app.get_width()
        app_height = self._app.get_height()
        spacing = self._app.get_card_size()[0] * app_width/2 #self.app.cardSize[0] * self.app.width / len(self.hand)
        x = app_width * self._posRatio[0]
        y = app_height * self._posRatio[1]
        trianglePoints = [[(app_width * (self._posRatio[0] + self._app.get_card_size()[0] + .1), app_height * (self._posRatio[1] + .125)), (app_width * (self._posRatio[0] + self._app.get_card_size()[0] + .1), app_height * (self._posRatio[1] + .175)), (app_width * (self._posRatio[0] + self._app.get_card_size()[0] + .05),app_height * (self._posRatio[1] + .15))],
                          [(app_width * (self._posRatio[0] + .025), app_height * (self._posRatio[1] + self._app.get_card_size()[1] + .05)), (app_width * (self._posRatio[0] + .075), app_height * (self._posRatio[1] + self._app.get_card_size()[1] + .05)), (app_width * (self._posRatio[0] + .05),app_height * (self._posRatio[1] + self._app.get_card_size()[1]))],
                          [(app_width * (self._posRatio[0] - .05), app_height * (self._posRatio[1] - .025)), (app_width * (self._posRatio[0] - .05), app_height * (self._posRatio[1] - .075)), (x,app_height * (self._posRatio[1] - .05))]]
        
        if self._app.get_current_turn() % 4 != 0:
            pygame.draw.polygon(surfaceToDraw,(255,200,0),trianglePoints[self._app.get_current_turn() % 4 - 1])

        for i in range(math.ceil(len(self._hand)/-2),math.ceil(len(self._hand)/2)):
            height,width = self._app.get_card_size()[1] * app_height, self._app.get_card_size()[0] * app_width
            try:
                cardIndex = i + math.floor(len(self._hand)/2)
                card = self._hand[cardIndex]
            except:
                break
            
            sizedImage = pygame.transform.smoothscale(card.get_image(),(width, height))
            rotatedImage = pygame.transform.rotate(sizedImage,self._rotation)
            
            
            if self._rotation % 180 == 0:
                x = app_width * self._posRatio[0] + spacing * i
            else:
                y = app_height * self._posRatio[1] + spacing * i

            surfaceToDraw.blit(rotatedImage,(x, y))

    

    def add_to_hand(self, toAdd):
        toAdd.set_card_image("Cover")
        super().add_to_hand(toAdd)

    def play_hand(self, stock):
        card = None
        self._app.set_current_turn(self._app.get_current_turn() + 1)
        for i in range(len(self._hand) - 1, -1, -1):
            if i > -1 and i < len(self._hand):
                card = self._hand[i]
                if card.playable(stock.get_card()) and not self._attempting_to_play:
                    card.set_card_image("Not Cover")
                    self._attempting_to_play.append(self._hand.pop(i))#stock.add_card_to_stock(self._hand.pop(i))
                else:
                    for otherCard in self._attempting_to_play:
                        if card.is_same_rank(otherCard):
                            if self._hand:
                                self._attempting_to_play.append(self._hand.pop(i))
                                i-=1
        
        if self._attempting_to_play:
            for card in self._attempting_to_play: 
                stock.add_card_to_stock(card)
            self._attempting_to_play.clear()

        else:
            amtTimesDrewDeck = 0
            deck = self._app.get_current_screen().get_deck()
            while (amtTimesDrewDeck < 5 and len(deck.get_cards())) != 0:
                amtTimesDrewDeck += 1
                card = deck.get_cards().pop()

                if card.playable(stock.get_card()):
                    stock.add_card_to_stock(card)
                    break
                else:
                    self.add_to_hand(card)

        if self.is_hand_empty():
            self._app.reset_round(self._app.get_current_turn() - 1)