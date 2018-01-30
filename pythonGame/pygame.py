
import pygame
from pygame.locals import *
import random

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.mixer.init()
clock = pygame.time.Clock()
FPS = 25

keys = [False, False]

alicePosition = [width / 2, height - 100]
badBalls = []
goodBalls = []
bombs = []

health = 3
score = 0
badTimer = 50
goodTimer = 0
creationTimerForGood = 90
creationTimerForBad = 80
speed = 3
level = 5

changeLevelPointer = 5
changeLevelCounter = changeLevelPointer

giveLife = 10
giveLifeCounter = giveLife

#images
bad = pygame.image.load("resources/bomb.png")
good = pygame.image.load("resources/flower.png")
bomb = pygame.image.load("resources/explosion.png")
heart = pygame.image.load("resources/heart.png")
alice = pygame.image.load("resources/alice.png")
# aliceDead = pygame.image.load("resources/aliceDead.png")
cover = pygame.image.load("resources/cover.png")
startImg = pygame.image.load("resources/start.png")
gameOverImg = pygame.image.load("resources/gameover.png")
#sounds
explosion = pygame.mixer.Sound("resources/explosion.wav")
# point = pygame.mixer.Sound("resources/point.wav")
explosion.set_volume(0.15)
# point.set_volume(0.15)
pygame.mixer.music.load('resources/KellySweet Dinosaur.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.20)

grammiRect = pygame.Rect(alice.get_rect())
goodRect = pygame.Rect(good.get_rect())
badRect = pygame.Rect(bad.get_rect())
heartRect = pygame.Rect(heart.get_rect())

ews = width/goodRect.w

font = pygame.font.SysFont("comicsansms", 25)


def drawScene():
    # global score
    screen.fill(0)
    screen.blit(cover, (0, 0))
    for badBall in badBalls:
        screen.blit(bad, badBall)
    for goodBall in goodBalls:
        screen.blit(good, goodBall)
    for myBomb in bombs:
        screen.blit(bomb, myBomb)
    screen.blit(alice, (alicePosition[0], alicePosition[1]))
    text = font.render("Score: "+str(score), True, (0, 0, 0))
    screen.blit(text, [0, 0])
    for i in range(1, health + 1):
        screen.blit(heart, [width - heartRect.w * i, 0])
    pygame.display.flip()


def moveObjects():
    if keys[0]:
        alicePosition[0] = max(alicePosition[0] - 15, 0)
    elif keys[1]:
        alicePosition[0] = min(alicePosition[0] + 15, width - grammiRect.w)
    index = 0
    for badBall in badBalls:
        badBall[1] += speed
        index += 1
    index = 0
    for goodBall in goodBalls:
        goodBall[1] += speed
        index += 1
    index = 0
    for myBomb in bombs:
        myBomb[1] += speed
        index += 1
    index = 0
    for badBall in badBalls[:]:
        if badBall[1] > height:
            badBalls.pop(index)
        else:
            index += 1
    index = 0
    for goodBall in goodBalls[:]:
        if goodBall[1] > height:
            goodBalls.pop(index)
        else:
            index += 1
    index = 0
    for myBomb in bombs[:]:
        if myBomb[1] > height:
            bombs.pop(index)
        else:
            index += 1


def createObjects():
    global badTimer, goodTimer
    if badTimer == 0:
        badBalls.append([random.randint(0, ews) * goodRect.w, 25])
        badTimer = creationTimerForBad
    if goodTimer == 0:
        goodBalls.append([random.randint(0, ews) * goodRect.w, 25])
        goodTimer = creationTimerForGood
    badTimer -= 1
    goodTimer -= 1


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                exit(0)
            if event.key == K_LEFT:
                keys[0] = True
            elif event.key == K_RIGHT:
                keys[1] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[0] = False
            elif event.key == pygame.K_RIGHT:
                keys[1] = False


def checkCollision():
    global score, health, giveLifeCounter, changeLevelCounter
    grammirectTemp=grammiRect
    grammirectTemp.left=alicePosition[0]
    grammirectTemp.top=alicePosition[1]
    index = 0
    for badBall in badBalls[:]:
        badrectTemp = badRect
        badrectTemp.left = badBall[0]
        badrectTemp.top = badBall[1]
        if grammirectTemp.colliderect(badrectTemp):
            explosion.play()
            health -= 1
            if health == 0:
                gameOver()
            bombs.append(badBalls.pop(index))
        else:
            index += 1
    index = 0
    for goodBall in goodBalls[:]:
        goodrectTemp = goodRect
        goodrectTemp.left = goodBall[0]
        goodrectTemp.top = goodBall[1]
        if grammirectTemp.colliderect(goodrectTemp):
            # point.play()
            score += 1
            goodBalls.pop(index)
            if giveLifeCounter == 0:
                health += 1
                giveLifeCounter = giveLife
            changeLevelCounter -= 1
            giveLifeCounter -= 1

        else:
            index += 1


def gameOver():
    drawScene()
    screen.blit(gameOverImg, [0, 0])
    text = font.render("Score: "+str(score), True, (0, 0, 0))
    screen.blit(text, [screen.get_rect().centerx - 50, screen.get_rect().centery+24])
    # diff = (pygame.Rect(aliceDead.get_rect()).w - pygame.Rect(alice.get_rect()).w)/2
    # screen.blit(aliceDead, (alicePosition[0] - diff, alicePosition[1]))
    pygame.display.flip()
    while 1 == 1:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit(0)


def intro():
    screen.blit(startImg, [0, 0])
    pygame.display.flip()
    while 1 == 1:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


intro()
while 1 == 1:
    checkEvents()
    drawScene()
    moveObjects()
    createObjects()
    checkCollision()
    if changeLevelCounter == 0:
        changeLevelCounter = changeLevelPointer
        if level >= 0:
            level -= 1
            creationTimerForGood -= 20
            creationTimerForBad -= 20
            speed += 1
    clock.tick(FPS)
