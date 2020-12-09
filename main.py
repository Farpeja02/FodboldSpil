import pygame

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=6, buffer=2048)
font = pygame.font.Font('freesansbold.ttf', 32)



from Player import PlayerClass
from Terrain import TerrainClass
from random import randint
clock = pygame.time.Clock()
gameWindowHeight=800
gameWindowWidth=1200


terrain=[]


highScore=0




screen = pygame.display.set_mode((gameWindowWidth, gameWindowHeight))


def collisionChecker(firstGameObject, secondGameObject):
        if firstGameObject.x + firstGameObject.width > secondGameObject.x and firstGameObject.x < secondGameObject.x + secondGameObject.width and firstGameObject.y + firstGameObject.height > secondGameObject.y and firstGameObject.y < secondGameObject.y + secondGameObject.height:
            return True

playerObject = PlayerClass(screen,xpos=590, ypos=100,terrainCollection=terrain)


def createTerrain():
    terrain.append(TerrainClass(screen, randint(-200,gameWindowWidth + 200),randint(-200,gameWindowHeight + 200),randint(10,200),randint(10,200)))
    if collisionChecker(playerObject, terrain[-1]):
        terrain.pop()
        createTerrain()



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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                playerObject.ySpeed += playerObject.maxSpeed
            if event.key == pygame.K_DOWN:
                playerObject.ySpeed -= playerObject.maxSpeed
            if event.key == pygame.K_LEFT:
                playerObject.xSpeed += playerObject.maxSpeed
            if event.key == pygame.K_RIGHT:
                playerObject.xSpeed -= playerObject.maxSpeed

    playerObject.update()

        #DRAW GAME OBJECTS:
    screen.fill((0, 0, 20)) #blank screen. (or maybe draw a background)


    playerObject.draw()


    text = font.render('SCORE: ' + str(playerObject.points), True,(0, 255, 0))
    screen.blit(text,(0,0))

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
