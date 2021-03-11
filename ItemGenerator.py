import pygame
import random
class ItemGeneratorClass:

    def __init__(self,screen,_x,_y,_width,_height):
        self.theScreen=screen
        self.x=_x
        self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        self.pickup = 0
        self.y=_y
        self.itemcounted = 0
        self.width = _width
        self.height = _height

        self.screenWidth = self.theScreen.get_size()[0] #
        self.screenHeight = self.theScreen.get_size()[1]
    def update(self,playerObject):
        if self.pickup == 1:
            self.x = playerObject.x
            self.y = playerObject.y
    def draw(self):
        pygame.draw.rect(self.theScreen,self.color, pygame.Rect(self.x,self.y, self.width,self.height))

class Door(ItemGeneratorClass):
    def update(self,playerObject):
        pass

