import StandardRules
from random import randint
from ItemGenerator import ItemGeneratorClass
import Util
from Terrain import TerrainClass

class shoppingcenter():
    def __init__(self, surface, playerObject, CircularCordinateBuffer, Door, Wallet, terrain):
        self.inShoppingCenter = 0  # Is true if in shopping center
        self.itemsPickedUp = 0  # How many item the player has pickeed up
        self.items = []  # List of item objects
        self.shoppingSpawned = 0  # Determen if shopping center has spawned

        self.surface = surface
        self.itemcounter = 0
        self.playerObject = playerObject
        self.CircularCordinateBuffer = CircularCordinateBuffer
        self.Door = Door
        self.Wallet = Wallet
        self.terrain = terrain





    def createItem(self,surface,terrain):
        self.items.append(ItemGeneratorClass(surface, randint(200, StandardRules.gameWidth - 200), randint(200, StandardRules.gameHeight - 200),1))
        for tile in self.terrain:
            if Util.collisionChecker(tile, self.items[-1]):
                self.items.pop()
                self.createItem(surface,self.terrain)

    def spawnShoppingCenter(self,surface,terrain):
        terrain.append(TerrainClass(surface, 300, 250, 1200, 50))
        terrain.append(TerrainClass(surface, 300, 500, 1200, 50))
        terrain.append(TerrainClass(surface, 300, 750, 1200, 50))

        for i in range(5):
            self.createItem(surface,self.terrain)

    def update(self):
        if self.CircularCordinateBuffer.is_full():
            self.CircularCordinateBuffer.dequeue()


        if Util.collisionChecker(self.Door, self.playerObject) and self.itemsPickedUp == StandardRules.MAXITEMSPICKEDUPBYPLAYER:
            self.terrain.clear()
            self.inShoppingCenter = 0
            self.items.clear()
            self.Wallet.x = randint(200, StandardRules.gameWidth - 50)
            self.Wallet.y = randint(200, StandardRules.gameHeight - 50)
            self.shoppingSpawned = 0
            self.itemsPickedUp = 0
            self.playerObject.points += 1
            self.inHome = 1
        if Util.collisionChecker(self.Door, self.Wallet):
            self.inShoppingCenter = 1
            self.inHome = 0


        if self.inShoppingCenter == 1 and self.shoppingSpawned == 0:
            self.spawnShoppingCenter(self.surface,self.terrain)
            self.shoppingSpawned = 1

        self.itemFollower()
    def itemFollower(self):
        itemcounter = 0
        for item in self.items:
            if Util.collisionChecker(item, self.playerObject):
                if item.itemcounted == 0:
                    self.itemsPickedUp += 1
                    item.itemcounted = 1


            if item.itemcounted == 1:
                itemcounter += 1
                item.x,item.y = self.CircularCordinateBuffer.frontOffSet(itemcounter * StandardRules.ITEMTALESPACE)
