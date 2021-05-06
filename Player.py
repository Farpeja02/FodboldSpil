import pygame

class PlayerClass:

    xSpeed=0
    ySpeed=0
    maxSpeed=6
    points=0
    color = (255,0,0)

    def __init__(self,screen,xpos,ypos,terrainCollection):
        self.x=xpos
        self.y=ypos


        self.theScreen=screen
        self.screenWidth = self.theScreen.get_size()[0] #
        self.screenHeight = self.theScreen.get_size()[1]
        self.terrainCollection=terrainCollection
        self.playerIMG = pygame.image.load('Player.png')
        self.width = self.playerIMG.get_size()[0]
        self.height = self.playerIMG.get_size()[1]


    def update(self):
        self.futureX=self.x+self.xSpeed
        self.futureY=self.y+self.ySpeed
        xWillCollide = False
        yWillCollide = False
        for tile in self.terrainCollection:
            #if the player is within the x coordinates of a wall tile, and future Y coordinate is inside the wall:
            if self.x + self.width > tile.x and self.x < tile.x + tile.width and self.futureY + self.height > tile.y and self.futureY < tile.y + tile.height:

                yWillCollide=True
            # if the player is within the Y coordinates of a wall tile, and future X coordinate is inside the wall:
            if self.y + self.height > tile.y and self.y < tile.y + tile.height and self.futureX + self.width > tile.x and self.futureX < tile.x + tile.width:
                xWillCollide=True

        if not xWillCollide:
            self.x = self.futureX
        if not yWillCollide:
            self.y = self.futureY

        #safety to prevent overshoot:
        if self.x+self.width > self.screenWidth:
            self.x = self.screenWidth-self.width
        if self.y+self.height > self.screenHeight:
            self.y = self.screenHeight-self.height
        if self.x<0:
            self.x=0
        if self.y<0:
            self.y=0


    def draw(self):
        rotationAngle = 0

        if self.xSpeed / self.maxSpeed * 180 > 0:
            tempFish = pygame.transform.flip(self.playerIMG, True,False)
        else:
            tempFish = pygame.transform.rotate(self.playerIMG, rotationAngle)

        self.theScreen.blit(tempFish,(self.x,self.y))
