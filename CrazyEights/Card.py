import pygame
class Card: # Base class card to lean more on object oriented programming
    def __init__(self, rank, suit, app):
        self._rank = rank
        self._suit = suit
        self._image = pygame.image.load("./" + suit + "/" + str(rank) + ".png").convert()
        self.app = app

    def get_points(self):
        if self._rank == 'Ace':
            return 1
        if self._rank == '8':
            return 50
        if self._rank == 'King' or self._rank == 'Queen' or self._rank == 'Jack':
            return 10
        return int(self._rank)
    
    def __eq__(self, otherCard):
        return self._rank == otherCard.get_rank() and self._suit == otherCard.get_suit()
    
    def playable(self,otherCard):
        return self._rank == otherCard.get_rank() or self._suit == otherCard.get_suit() or self._rank == '8'

    def __str__(self):
        return (str(self._rank) + " " + self._suit)
    
    def is_same_rank(self,otherCard):
        return self._rank == otherCard.get_rank()
    
    def get_rank(self):
        return self._rank
    
    def get_suit(self):
        return self._suit
    
    def set_card_image(self, direciton):
        if direciton.__eq__("Cover"):
            self._image = pygame.image.load("Cover.jpg").convert()
        if direciton.__eq__("Not Cover"):
            self._image = pygame.image.load("./" + self._suit + "/" + str(self._rank) + ".png").convert()

    def get_image(self):
        return self._image