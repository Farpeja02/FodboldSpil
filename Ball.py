import pygame


class BallClass:
    color=( 117, 119,117)

    def __init__(self,screen,_x,_y,_width,_height):
        self.theScreen=screen
        self.x=_x
        self.y=_y
        self.width = _width
        self.height = _height
        self.ballX = 0
        self.ballY = 0
        self.screenWidth = self.theScreen.get_size()[0] #
        self.screenHeight = self.theScreen.get_size()[1]
    def update(self):
        if self.x + self.width > self.screenWidth:
            self.ballX *= -1
        if self.y + self.height > self.screenHeight:
            self.ballY *= -1
        if self.x < 0:
            self.ballX *= -1
        if self.y < 0:
            self.ballY *= -1
    def draw(self):
        pygame.draw.rect(self.theScreen,self.color, pygame.Rect(self.x,self.y, 20,20))
