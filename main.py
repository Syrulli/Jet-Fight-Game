import math
import random

import pygame

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('bg.jpg')

# Caption and Icon
pygame.display.set_caption("Tangina mo")
icon = pygame.image.load('jet.png')
pygame.display.set_icon(icon)

# Player
jetImg = pygame.image.load('jet.png')
jetX = 370
jetY = 480
jetX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
missileImg = pygame.image.load('missile.png')
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 30
missile_state = "ready"

# Score


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def jet(x, y):
    screen.blit(jetImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt(math.pow(enemyX - missileX, 2) + (math.pow(enemyY - missileY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jetX_change = -5
            if event.key == pygame.K_RIGHT:

                jetX_change = 5
            if event.key == pygame.K_SPACE:
                if missile_state is "ready":

                    missileX = jetX
                    fire_missile(missileX, missileY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jetX_change = 0

    jetX += jetX_change
    if jetX <= 0:
        jetX = 0
    elif jetX >= 736:
        jetX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            missileY = 480
            missile_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Missile Movement
    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    if missile_state is "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change

    jet(jetX, jetY)
    show_score(textX, testY)

    pygame.display.update()
