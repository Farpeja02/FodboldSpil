import pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=6, buffer=2048)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h


from circular_buffer import CircularBuffer
from Player import PlayerClass
from ItemGenerator import ItemGeneratorClass
from ItemGenerator import Door
from LevelController import LevelClass
from LevelController import MenuClass
from random import randint
import StandardRules
import Util


clock = pygame.time.Clock() #Clock makes sure the game always runs on 60 ticks per second
timer = 60 #Number of ticks in game by seconds left
tick = 0 #Tick counter
terrain = []  # List of terrain objects
highScore=1


surface = pygame.Surface((StandardRules.gameWidth, StandardRules.gameHeight)) #Surface is where we draw objects and then scale them onto screen,
screen = pygame.display.set_mode((width,height))
CircularCordinateBuffer =  CircularBuffer(StandardRules.MAXITEMSPICKEDUPBYPLAYER * StandardRules.ITEMTALESPACE) #Class for circular X cord lists for making items follow player



Wallet = ItemGeneratorClass(surface, randint(200, StandardRules.gameWidth - 200), randint(200, StandardRules.gameHeight - 200), 2)

Door = Door(surface, 825, 960, 3)


playerObject = PlayerClass(surface,xpos=855, ypos=600,terrainCollection=terrain)
level = LevelClass(surface, CircularCordinateBuffer, Door, Wallet, highScore, playerObject, terrain, timer)
menu = MenuClass(surface, CircularCordinateBuffer, Door, Wallet, highScore, playerObject, terrain, timer)


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
            if Util.collisionChecker(playerObject, Wallet) and event.key == pygame.K_SPACE:
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
            if Util.collisionChecker(playerObject, Wallet) and event.key == pygame.K_SPACE:
                Wallet.pickup = 0

    playerObject.update()


    if Util.collisionChecker(Door,playerObject) and level.inMenu == 1:
        level.inMenu = 0
        level.inDayCycle = 1
        timer = 60
        inHome = 1


    if tick % 60 == 0 and level.inMenu == 0:
        timer -= 1

    level.update(playerObject)
        #DRAW GAME OBJECTS:
    surface.fill((0, 0, 40)) #blank screen. (or maybe draw a background)

    level.draw()
    playerObject.draw()
    level.DrawText(playerObject,timer)

    if level.inMenu == 1:
        menu.DrawText(playerObject,timer)


    screen.blit(pygame.transform.scale(surface,(width, height)), (0, 0))
    pygame.display.update()
    clock.tick(60)
    if playerObject.points > highScore:
        highScore = playerObject.points
    if level.inMenu == 0:
        tick += 1

with open('highScoreFile', 'w') as file:
    print("Saving highscore to file:", highScore)
    file.write(str(highScore))
