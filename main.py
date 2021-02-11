import pygame

from circular_buffer import CircularBuffer

#test123
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=6, buffer=2048)
font = pygame.font.Font('freesansbold.ttf', 32)
titleSize = 99
titleFont = pygame.font.Font('freesansbold.ttf', titleSize)

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
from Player import PlayerClass
from Terrain import TerrainClass
from Ball import BallClass
from random import randint
clock = pygame.time.Clock()
gameHeight=1080
gameWidth=1920
terrain=[]
items = []
highScore=0
pickedup = 0
MAXITEMSPICKEDUPBYPLAYER = 5
ITEMTALESPACE = 10
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
surface = pygame.Surface((gameWidth, gameHeight))
screen = pygame.display.set_mode((width,height))
rx =  CircularBuffer(MAXITEMSPICKEDUPBYPLAYER * ITEMTALESPACE)
ry =  CircularBuffer(MAXITEMSPICKEDUPBYPLAYER * ITEMTALESPACE)
playerObject = PlayerClass(surface,xpos=855, ypos=500,terrainCollection=terrain)

Wallet = BallClass(surface, randint(200, gameWidth - 200), randint(200, gameHeight - 200), 30, 30, playerObject)

Door = BallClass(surface, 825, 960, 100, 40, playerObject)

def collisionChecker(firstGameObject, secondGameObject):
        if firstGameObject.x + firstGameObject.width > secondGameObject.x and firstGameObject.x < secondGameObject.x + secondGameObject.width and firstGameObject.y + firstGameObject.height > secondGameObject.y and firstGameObject.y < secondGameObject.y + secondGameObject.height:
            return True
def createItem():
    items.append(BallClass(surface, randint(200, gameWidth - 200), randint(200, gameHeight - 200), randint(20, 30), randint(20, 30), playerObject))
    for tile in terrain:
        if collisionChecker(tile, items[-1]):
            items.pop()
            createItem()
def createTerrain():
    terrain.append(TerrainClass(surface, randint(-200, gameWidth + 200), randint(-200, gameHeight + 200), randint(10, 200), randint(10, 200)))
    if collisionChecker(playerObject, terrain[-1]):
        terrain.pop()
        createTerrain()
def spawnShoppingCenter():

    terrain.append(TerrainClass(surface, 300, 250,1200, 50))
    terrain.append(TerrainClass(surface, 300, 500,1200, 50))
    terrain.append(TerrainClass(surface, 300, 750,1200, 50))

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

    if rx.is_full():
        rx.dequeue()
    if ry.is_full():
        ry.dequeue()

    if collisionChecker(Door, playerObject) and itemsPickedUp == MAXITEMSPICKEDUPBYPLAYER:
        terrain.clear()
        inShoppingCenter = 0
        items.clear()
        Wallet.x = randint(200, gameWidth - 50)
        Wallet.y = randint(200, gameHeight - 50)
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
        timer = 60
        inHome = 1

    rx.enqueue(playerObject.x)
    ry.enqueue(playerObject.y)
    playerObject.update()
    Wallet.update()
    itemcounter = 0
    for item in items:
        if collisionChecker(item , playerObject):
            if item.itemcounted == 0:
                itemsPickedUp += 1
                item.itemcounted = 1

        if item.itemcounted == 1 :
            itemcounter += 1
            item.x = rx.frontOffSet(itemcounter * ITEMTALESPACE)
            item.y = ry.frontOffSet(itemcounter * ITEMTALESPACE)
    if tick % 60 == 0 and inDayCycle == 1:
        timer -= 1

    if timer < 1 and inDayCycle == 1:
        inDayCycle = 0
        with open('highScoreFile', 'w') as file:
            print("Saving highscore to file:", highScore)
            file.write(str(highScore))
        terrain.clear()
        inShoppingCenter = 0
        items.clear()
        Wallet.x = randint(200, gameWidth - 50)
        Wallet.y = randint(200, gameHeight - 50)
        shoppingSpawned = 0
        itemsPickedUp = 0
        inMenu = 1

        #DRAW GAME OBJECTS:
    surface.fill((0, 0, 40)) #blank screen. (or maybe draw a background)


    playerObject.draw()
    if inHome == 1:
        Wallet.draw()
    for item in items:
        item.draw()
    for walls in terrain:
        walls.draw()
    Door.draw()

    if inShoppingCenter == 1:
        itemtext = font.render('Items Picked Up: ' + str(itemsPickedUp) + '/' + str(MAXITEMSPICKEDUPBYPLAYER), True, (0, 255, 0))
        surface.blit(itemtext, (300, 50))
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

    if inMenu == 1:
        title = titleFont.render('From The Distance', True, (160, 55, 0))
        surface.blit(title, (titlePlaceX, titlePlaceY))
        titleGuide = font.render('Go Through the door, and your first day in isolation starts', True, (55, 150, 0))
        surface.blit(titleGuide, (460, 400))
        text = font.render('Highscore: ' + str(highScore), True, (60, 55, 0))
        surface.blit(text, (780, 440))
    if inDayCycle == 1:
        text = font.render('Time Left: ' + str(timer), True, (0, 0, 255))
        surface.blit(text, (600, 0))
        text = font.render('SCORE: ' + str(playerObject.points), True, (0, 255, 0))
        surface.blit(text, (300, 0))


    screen.blit(pygame.transform.scale(surface,(width, height)), (0, 0))
    pygame.display.update()
    clock.tick(60)
    if playerObject.points > highScore:
        highScore = playerObject.points
    if inDayCycle == 1 or inMenu == 1:
        tick += 1
#When done is false the while loop above exits, and this code is run:
with open('highScoreFile', 'w') as file:
    print("Saving highscore to file:", highScore)
    file.write(str(highScore))
