# GAME MADE BY "MrHoss" github:https://github.com/MrHoss
# My first and simple Python project
# This game is not finished, if you want to modify the game feel free, please share any problem with the code with me.



import pygame
import math
import random
import sys
from random import uniform
from pygame import mixer

pygame.init()

# screen parameters
winX = 1024
winY = 768
window = pygame.display.set_mode((winX, winY),pygame.FULLSCREEN, vsync=60)
pygame.display.set_caption("SkyRise")

# visual parameters
background = pygame.image.load('gfx/bg/background4:3.png')
background = pygame.transform.scale(background, (winX, winY))
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)

# player parameters
playerShip1 = pygame.image.load('gfx/ships/ship.png')
playerShip2 = pygame.image.load('gfx/ships/ship1.png')


# object parameters
ASTER1 = pygame.image.load('gfx/asteroids/Asteroid.png')
ASTER2 = pygame.image.load('gfx/asteroids/Asteroid2.png')
ASTER3 = pygame.image.load('gfx/asteroids/Asteroid3.png')
objectImg = []
objectX = []
objectY = []
objectX_move = []
objectY_move = []
maxObject_display = 6

# Object generation
for i in range(maxObject_display):
    objectImg.append(random.choice([ASTER1, ASTER2, ASTER3]))
    objectX.append(random.uniform(0, winX))
    objectY.append(random.uniform(0-300,winY-3000))
    objectX_move.append(0)
    objectY_move.append(15)
#Player start position function
def player(x, y):
    window.blit(playerShip, (x, y))
#object start position function
def objects(x, y, i):
    window.blit(objectImg[i], (x, y))
#player and object collision function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 100: #if Player is 100 px near the object is True
        return True
    else:
        return False

# pause screen function
def paused():
    Pause = GOfont.render("GAME PAUSED", True, (255, 255, 255))
    pause = True
    window.blit(Pause, (winX / 2 - 250, winY / 2 - 300))
    while pause:
        window.blit(Pause, (winX+2, winY+2))
        window.blit(text, (50, 40))
        window.blit(textlvl, (50, 75))
        window.blit(textlife, (50, 110))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
            pygame.display.update()


def Startscreen():
    StartLogo = pygame.image.load('Logo.png')
    StartLogo = pygame.transform.scale(StartLogo, (int(winX / 2), int(winY / 2)))
    Start = True
    while Start:
        pygame.time.delay(50)
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        window.blit(StartLogo, (winX/2-250, winY/2-300))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ShipSelection()
                    Start = False


        pygame.display.update()

def ShipSelection():
    global playerShip
    Select = True
    mouse_over = (170, 170, 170)
    mouse_out = (100, 100, 100)
    selectedc = (120, 120, 120)
    bposX = 100
    bposY = 100
    bsizeX = 144
    bsizeY = 144
    selected1 = False
    selected2 = False
    playerShip = []
    while Select:
        pygame.time.delay(50)
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Startscreen()
                    Select = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (playerShip == playerShip1 or playerShip == playerShip2):
                    GamingScreen()
                    Select = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bposX <= mouse[0] <= bposX + bsizeX and bposY <= mouse[1] <= bposY + bsizeY:
                    playerShip = playerShip1
                    selected1 = True
                    selected2 = False
                if bposX+160 <= mouse[0] <= bposX+160 + bsizeX and bposY <= mouse[1] <= bposY + bsizeY:
                    playerShip = playerShip2
                    selected2 = True
                    selected1 = False


        if selected1:
            pygame.draw.rect(window, selectedc, [bposX, bposY, bsizeX, bsizeY])
        elif bposX <= mouse[0] <= bposX + bsizeX and bposY <= mouse[1] <= bposY + bsizeY:
            pygame.draw.rect(window, mouse_over, [bposX, bposY, bsizeX, bsizeY])
        else:
            pygame.draw.rect(window, mouse_out, [bposX, bposY, bsizeX, bsizeY])
        if selected2:
            pygame.draw.rect(window, selectedc, [bposX+160, bposY, bsizeX, bsizeY])
        elif bposX+160 <= mouse[0] <= bposX+160 + bsizeX and bposY <= mouse[1] <= bposY + bsizeY:
            pygame.draw.rect(window, mouse_over, [bposX+160, bposY, bsizeX, bsizeY])
        else:
            pygame.draw.rect(window, mouse_out, [bposX+160, bposY, bsizeX, bsizeY])

        window.blit(playerShip1, (bposX , bposY))
        window.blit(playerShip2, (bposX+180, bposY))


        pygame.display.update()


def GamingScreen():

    global text
    global textlvl
    global textlife
    mixer.music.load("sfx/background.wav")
    mixer.music.play(-1)
    HUD = pygame.image.load('gfx/HUD.png')
    playerX = winX / 2 - 50
    playerY = winY / 2 + 150
    speed = 10
    lvl = 0
    lvlCount = 1
    timer = 0
    life = 3
    clockSec = 0
    textlife = font.render("Life: " + str(life), True, (255, 255, 255), (None))
    text = font.render("Score: " + str(clockSec), True, (255, 255, 255), (None))
    textlvl = font.render("Level: " + str(lvlCount), True, (255, 255, 255), (None))
    Run = True
    while Run :

        pygame.time.delay(50)
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keybind = pygame.key.get_pressed()

        if (keybind[pygame.K_UP] or keybind[pygame.K_w]) and playerY >= 0:
            playerY -= speed
        if (keybind[pygame.K_DOWN] or keybind[pygame.K_s]) and playerY <= winY - 150:
            playerY += speed
        if (keybind[pygame.K_RIGHT] or keybind[pygame.K_d]) and playerX <= winX - 100:
            playerX += speed
        if (keybind[pygame.K_LEFT] or keybind[pygame.K_a]) and playerX >= 10:
            playerX -= speed
        if (keybind[pygame.K_ESCAPE]):

            paused()

        # Enemy Movement
        for i in range(maxObject_display):

            if (objectY[i] >= 900):
                objectY[i] = uniform(-800, -1000)
                objectX[i] = uniform(0, winX)

            objectY[i] += objectY_move[i]+lvlCount

            # Collision
            collision = isCollision(objectX[i], objectY[i], playerX, playerY)
            if collision:
                explosionSound = mixer.Sound("sfx/explosion.wav")
                explosionSound.play()
                objectX[i] = random.uniform(0, winX)
                objectY[i] = random.uniform(-2200, -3000)
                life -= 1
                textlife = font.render("Life: " + str(life), True, (255, 255, 255), (None))
                playerX = winX/2-50
                playerY = winY/2+150
                if life == 0:
                    GameoverScreen()
                    Run = False
            objects(objectX[i], objectY[i], i)

        if (timer <20):
            timer +=1
        else:
            clockSec +=10
            text = font.render("Score: "+str(clockSec), True, (255, 255, 255), (None))
            timer = 0

        if (lvl <200):
            lvl +=1
        else:
            lvlCount +=1
            textlvl = font.render("Level: "+str(lvlCount), True, (255, 255, 255), (None))
            lvl = 0

        player(playerX, playerY)
        window.blit(HUD, (0, 0))
        window.blit(text, (50,40))
        window.blit(textlvl, (50,75))
        window.blit(textlife, (50, 110))
        pygame.display.update()

def GameoverScreen():
    GOtext = GOfont.render("GAME OVER", True, (255, 255, 255))
    GOscreen = True
    while GOscreen :
        pygame.time.delay(50)
        window.fill((0,0,0))
        window.blit(background,(0,0))

        window.blit(text, (winX/2-50,winY/2-100))
        window.blit(textlvl, (winX/2-50,winY/2-135))
        window.blit(GOtext, (winX / 2 - 200, winY / 2 - 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ShipSelection()
                    GOscreen = False

        for i in range(maxObject_display):


            if (objectY[i] >= winY+200):
                objectY[i] = uniform(-800, -1000)
                objectX[i] = uniform(0, winX)

            objectY[i] += objectY_move[i]
            objects(objectX[i], objectY[i], i)

        pygame.display.update()

while True:
    font = pygame.font.SysFont('freesans', 40, True)
    GOfont = pygame.font.SysFont('freesans', 64, True)
    Startscreen()
