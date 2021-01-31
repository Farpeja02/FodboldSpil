import pygame
#test123
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=6, buffer=2048)
font = pygame.font.Font('freesansbold.ttf', 32)
titleSize = 99
titleFont = pygame.font.Font('freesansbold.ttf', titleSize)


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
inHome = 0
shoppingSpawned = 0
inMenu = 1
inDayCycle = 0
timer = 0
tick = 0
titleGrowing = 1
titlePlaceX = 450
titlePlaceY = 250
screen = pygame.display.set_mode((gameWindowWidth, gameWindowHeight))

playerObject = PlayerClass(screen,xpos=855, ypos=500,terrainCollection=terrain)

Wallet = BallClass(screen, randint(200,gameWindowWidth - 200),randint(200,gameWindowHeight - 200),30,30, playerObject)

Door = BallClass(screen, 825, 960, 100, 40, playerObject)

def collisionChecker(firstGameObject, secondGameObject):
        if firstGameObject.x + firstGameObject.width > secondGameObject.x and firstGameObject.x < secondGameObject.x + secondGameObject.width and firstGameObject.y + firstGameObject.height > secondGameObject.y and firstGameObject.y < secondGameObject.y + secondGameObject.height:
            return True
def createItem():
    items.append(BallClass(screen, randint(200,gameWindowWidth - 200),randint(200,gameWindowHeight - 200),randint(20,30),randint(20,30), playerObject))
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

    terrain.append(TerrainClass(screen, 300, 250,1200, 50))
    terrain.append(TerrainClass(screen, 300, 500,1200, 50))
    terrain.append(TerrainClass(screen, 300, 750,1200, 50))

    for i in range(5):
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

    if collisionChecker(Door, playerObject) and itemsPickedUp == 5:
        terrain.clear()
        inShoppingCenter = 0
        items.clear()
        Wallet.x = randint(200, gameWindowWidth - 50)
        Wallet.y = randint(200,gameWindowHeight - 50)
        shoppingSpawned = 0
        itemsPickedUp = 0
        playerObject.points += 1
        inHome = 1
    if collisionChecker(Door,Wallet):
        inShoppingCenter = 1
        inHome = 0

    if inShoppingCenter == 1 and shoppingSpawned == 0:
        spawnShoppingCenter()
        shoppingSpawned = 1
    if collisionChecker(Door,playerObject) and inMenu == 1:
        inMenu = 0
        inDayCycle = 1
        timer = 120
        inHome = 1

    playerObject.update()
    Wallet.update()

    for item in items:
        if collisionChecker(item , playerObject):
            item.x = playerObject.x
            item.y = playerObject.y
            if item.itemcounted == 0:
                itemsPickedUp += 1
                item.itemcounted = 1

    if tick % 60 == 0 and inDayCycle == 1:
        timer -= 1


        #DRAW GAME OBJECTS:
    screen.fill((0, 0, 40)) #blank screen. (or maybe draw a background)


    playerObject.draw()
    if inHome == 1:
        Wallet.draw()
    for item in items:
        item.draw()
    for walls in terrain:
        walls.draw()
    Door.draw()

    if inShoppingCenter == 1:
        itemtext = font.render('Items Picked Up: ' + str(itemsPickedUp) + '/5', True, (0, 255, 0))
        screen.blit(itemtext, (300, 50))
    if inMenu == 1 and tick % 3 == 0:
        if titleGrowing == 1:
            titleSize += 1
            titlePlaceX -= 4
            titlePlaceY -= 1
            titleFont = pygame.font.Font('freesansbold.ttf', titleSize)
        if titleGrowing == 0:
            titleSize -= 1
            titlePlaceX += 4
            titlePlaceY += 1
            titleFont = pygame.font.Font('freesansbold.ttf', titleSize)
        if titleSize < 100:
            titleGrowing = 1
        if titleSize > 125:
            titleGrowing = 0
    if inMenu == 1:
        title = titleFont.render('From The Distance', True, (160, 55, 0))
        screen.blit(title, (titlePlaceX, titlePlaceY))
        titleGuide = font.render('Go Through the door, and your first day in isolation starts', True, (55, 150, 0))
        screen.blit(titleGuide, (460, 400))
    if inDayCycle == 1:
        text = font.render('Time Left: ' + str(timer), True, (0, 0, 255))
        screen.blit(text, (600, 0))
        text = font.render('SCORE: ' + str(playerObject.points), True, (0, 255, 0))
        screen.blit(text, (300, 0))
    text = font.render('Highscore: ' + str(highScore), True,(60, 55, 0))
    screen.blit(text, (0,0))

    pygame.display.flip()
    clock.tick(60)
    if playerObject.points > highScore:
        highScore = playerObject.points
    if inDayCycle == 1 or inMenu == 1:
        tick += 1
#When done is false the while loop above exits, and this code is run:
with open('highScoreFile', 'w') as file:
    print("Saving highscore to file:", highScore)
    file.write(str(highScore))
