
import StandardRules
from random import randint
from ShoppingCenter import shoppingcenter
import Util
class LevelClass:
    def __init__(self,surface,CircularCordinateBuffer,Door,Wallet,HighScore,playerObject,terrain,timer):
        self.timer = timer
        self.whatDay = 1
        self.inHome = 0  # Is true if in home
        self.inMenu = 1  # Is true if in menu
        self.inDayCycle = 0  # Is true if in day Cycle
        self.pickedup = 0  # Variable to measure if wallet is picked up
        self.surface = surface
        self.highScore = 1
        self.CircularCordinateBuffer = CircularCordinateBuffer

        self.Door = Door
        self.Wallet = Wallet
        self.HighScore = HighScore
        self.terrain = terrain
        self.shoppingCenter =shoppingcenter(surface,playerObject, CircularCordinateBuffer, Door, Wallet,terrain)

    def update(self,playerObject):

        self.CircularCordinateBuffer.enqueue((playerObject.x,playerObject.y))



        self.shoppingCenter.update()

        self.Wallet.update(playerObject)

        if Util.collisionChecker(self.Door, self.Wallet):
            self.inShoppingCenter = 1
            self.inHome = 0


        if self.timer < 1 and self.inDayCycle == 1:
            self.inDayCycle = 0
            if playerObject.points >= self.whatDay:
                self.whatDay += 1
            else:
                self.whatDay = 1
            playerObject.points = 0
            self.terrain.clear()
            self.inShoppingCenter = 0
            self.shoppingCenter.items.clear()
            self.Wallet.x = randint(200, StandardRules.gameWidth - 50)
            self.Wallet.y = randint(200, StandardRules.gameHeight - 50)
            self.shoppingSpawned = 0
            self.itemsPickedUp = 0
            self.inMenu = 1

        if Util.collisionChecker(self.Door, playerObject) and self.inMenu == 1:
            self.inMenu = 0
            self.inDayCycle = 1
            self.inHome = 1

    def DrawText(self,playerObject,timer):
        if self.shoppingCenter.inShoppingCenter == 1:
            itemtext = StandardRules.font.render('Items Picked Up: ' + str(self.shoppingCenter.itemsPickedUp) + '/' + str(StandardRules.MAXITEMSPICKEDUPBYPLAYER), True,
                                   (0, 255, 0))
            self.surface.blit(itemtext, (300, 50))

        if self.inDayCycle == 1:
            text = StandardRules.font.render('Time Left: ' + str(timer), True, (0, 0, 255))
            self.surface.blit(text, (600, 0))
            text = StandardRules.font.render('SCORE: ' + str(playerObject.points), True, (0, 255, 0))
            self.surface.blit(text, (300, 0))
    def draw(self):
        if self.inDayCycle == 1:
            self.Wallet.draw()
        for item in self.shoppingCenter.items:
            item.draw()
        for walls in self.terrain:
            walls.draw()
        self.Door.draw()


class MenuClass(LevelClass):
    def DrawText(self,playerObject,timer):
        title = StandardRules.titleFont.render('From The Distance', True, (160, 55, 0))
        self.surface.blit(title, (StandardRules.titlePlaceX, StandardRules.titlePlaceY))
        titleGuide = StandardRules.font.render('Go Through the door, and your first day in isolation starts', True, (55, 150, 0))
        self.surface.blit(titleGuide, (460, 400))
        text = StandardRules.font.render('Highscore: ' + str(self.highScore), True, (60, 55, 0))
        self.surface.blit(text, (780, 440))
        text = StandardRules.font.render('You are about to start day: ' + str(self.whatDay), True, (200, 55, 0))
        self.surface.blit(text, (670, 480))
    def update(self,playerObject):
        pass