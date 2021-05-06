import pygame
import random
class ItemGeneratorClass:

    def __init__(self,screen,_x,_y,whatItem):
        self.theScreen=screen
        self.x=_x
        self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        self.pickup = 0
        self.y=_y
        self.itemcounted = 0
        self.whatItem = whatItem

        self.screenWidth = self.theScreen.get_size()[0] #
        self.screenHeight = self.theScreen.get_size()[1]
        self.whatSprite = random.randint(1,5)
        if self.whatItem == 1:
            if self.whatSprite == 1:
                self.itemIMG = pygame.image.load('Item1.png')
            if self.whatSprite == 2:
                self.itemIMG = pygame.image.load('Item2.png')
            if self.whatSprite == 3:
                self.itemIMG = pygame.image.load('Item3.png')
            if self.whatSprite == 4:
                self.itemIMG = pygame.image.load('Item4.png')
            if self.whatSprite == 5:
                self.itemIMG = pygame.image.load('Item5.png')
        if self.whatItem == 2:
            self.itemIMG = pygame.image.load('Wallet.png')
        if self.whatItem == 3:
            self.itemIMG = pygame.image.load('Door.png')
        self.width = self.itemIMG.get_size()[0]
        self.height = self.itemIMG.get_size()[1]

    def update(self,playerObject):
        if self.pickup == 1:
            self.x = playerObject.x
            self.y = playerObject.y
    def draw(self):

        self.theScreen.blit(self.itemIMG, (self.x, self.y))

class Door(ItemGeneratorClass):
    def update(self,playerObject):
        pass

