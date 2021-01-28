import pygame
#test123
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=6, buffer=2048)
font = pygame.font.Font('freesansbold.ttf', 32)



from Player import PlayerClass
from Terrain import TerrainClass
from Ball import BallClass
from random import randint
clock = pygame.time.Clock()
gameWindowHeight=1000
gameWindowWidth=1800
terrain=[]
items = []
highScore=0
pickedup = 0
itemsPickedUp = 0
inShoppingCenter = 0
shoppingSpawned = 0

screen = pygame.display.set_mode((gameWindowWidth, gameWindowHeight))

playerObject = PlayerClass(screen,xpos=590, ypos=100,terrainCollection=terrain)

Wallet = BallClass(screen, 400, 200, 30, 30, playerObject)

Door = BallClass(screen, 825, 960, 100, 40, playerObject)

def collisionChecker(firstGameObject, secondGameObject):
        if firstGameObject.x + firstGameObject.width > secondGameObject.x and firstGameObject.x < secondGameObject.x + secondGameObject.width and firstGameObject.y + firstGameObject.height > secondGameObject.y and firstGameObject.y < secondGameObject.y + secondGameObject.height:
            return True
def createItem():
    items.append(BallClass(screen, randint(0,gameWindowWidth),randint(0,gameWindowHeight),randint(20,30),randint(20,30), playerObject))
    for tile in terrain:
        if collisionChecker(tile, items[-1]):
            items.pop()
            createItem()
def createTerrain():
    terrain.append(TerrainClass(screen, randint(-200,gameWindowWidth + 200),randint(-200,gameWindowHeight + 200),randint(10,200),randint(10,200)))
    if collisionChecker(playerObject, terrain[-1]):
        terrain.pop()
        createTerrain()
def spawnShoppingCenter():
    terrain.append(TerrainClass(screen, 300, 100,1200, 50))
    terrain.append(TerrainClass(screen, 300, 350,1200, 50))
    terrain.append(TerrainClass(screen, 300, 600,1200, 50))
    terrain.append(TerrainClass(screen, 300, 850,1200, 50))
    terrain.append(TerrainClass(screen, 850, 100,50, 750))
    for i in range(8):
        createItem()



done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True


        #KEY PRESSES:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerObject.ySpeed -= playerObject.maxSpeed
            if event.key == pygame.K_DOWN:
                playerObject.ySpeed += playerObject.maxSpeed
            if event.key == pygame.K_LEFT:
                playerObject.xSpeed -= playerObject.maxSpeed
            if event.key == pygame.K_RIGHT:
                playerObject.xSpeed += playerObject.maxSpeed
            if collisionChecker(playerObject, Wallet) and event.key == pygame.K_SPACE:
                Wallet.pickup = 1



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                playerObject.ySpeed += playerObject.maxSpeed
            if event.key == pygame.K_DOWN:
                playerObject.ySpeed -= playerObject.maxSpeed
            if event.key == pygame.K_LEFT:
                playerObject.xSpeed += playerObject.maxSpeed
            if event.key == pygame.K_RIGHT:
                playerObject.xSpeed -= playerObject.maxSpeed
            if collisionChecker(playerObject, Wallet) and event.key == pygame.K_SPACE:
                Wallet.pickup = 0

    if collisionChecker(Door, playerObject) and itemsPickedUp == 1:
        terrain.clear()
        inShoppingCenter = 0
        items.clear()
        Wallet.x = 300
        Wallet.y = 300
        shoppingSpawned = 0
        itemsPickedUp = 0
    if collisionChecker(Door,Wallet):
        inShoppingCenter = 1

    if inShoppingCenter == 1 and shoppingSpawned == 0:
        spawnShoppingCenter()
        shoppingSpawned = 1


    playerObject.update()
    Wallet.update()

    for item in items:
        if collisionChecker(item , playerObject):
            item.x = playerObject.x
            item.y = playerObject.y
            if item.itemcounted == 0:
                itemsPickedUp += 1
                item.itemcounted = 1



        #DRAW GAME OBJECTS:
    screen.fill((0, 0, 40)) #blank screen. (or maybe draw a background)


    playerObject.draw()
    Wallet.draw()
    for item in items:
        item.draw()
    for walls in terrain:
        walls.draw()
    Door.draw()
    text = font.render('SCORE: ' + str(playerObject.points), True,(0, 255, 0))
    screen.blit(text,(0,0))
    if inShoppingCenter == 1:
        itemtext = font.render('Items Picked Up: ' + str(itemsPickedUp) + '/8', True, (0, 255, 0))
        screen.blit(itemtext, (300, 50))
    text = font.render('HIGHSCORE: ' + str(highScore), True, (255, 0, 0))
    screen.blit(text, (300,0))

    pygame.display.flip()
    clock.tick(60)
    if playerObject.points > highScore:
        highScore = playerObject.points

#When done is false the while loop above exits, and this code is run:
with open('highScoreFile', 'w') as file:
    print("Saving highscore to file:", highScore)
    file.write(str(highScore))
