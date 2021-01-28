import pygame
import random

class BallClass:

    def __init__(self,screen,_x,_y,_width,_height, playerobejct):
        self.theScreen=screen
        self.x=_x
        self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        self.playerObject = playerobejct
        self.pickup = 0
        self.y=_y
        self.itemcounted = 0
        self.width = _width
        self.height = _height

        self.screenWidth = self.theScreen.get_size()[0] #
        self.screenHeight = self.theScreen.get_size()[1]
    def update(self):
        if self.pickup == 1:
            self.x = self.playerObject.x
            self.y = self.playerObject.y
    def draw(self):
        pygame.draw.rect(self.theScreen,self.color, pygame.Rect(self.x,self.y, self.width,self.height))
