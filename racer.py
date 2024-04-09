#Importing nesessary modules
import pygame, sys
from pygame.locals import *
import random, time

#Initializing pygame
pygame.init()
pygame.mixer.init()

#Frames per second
FPS = 60
FramePerSec = pygame.time.Clock()
#colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(128, 128, 128)
red = pygame.Color(255, 0, 0)

#Creating a Display screen
SCREEN_WIDTH = 570
SCREEN_HEIGHT = 800
SPEED = 5
SCORE = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)
 
background = pygame.image.load("R.png")

DISPLAYSURF = pygame.display.set_mode((570, 800))
DISPLAYSURF.fill(black)
pygame.display.set_caption("Racer")

pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)  # Play background music on loop

#Creating enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 870):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 540), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#Creating first coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 530), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 870):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 540), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#creating second coin class
class Coin2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 530), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 870):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 540), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#Creating player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (240, 700)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -SPEED)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, SPEED)
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-SPEED, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(SPEED, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

P1 = Player()
E1 = Enemy()
C1 = Coin()
C2 = Coin2()
#Creating Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()  # Group for coins
coins.add(C1)
coins.add(C2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
all_sprites.add(C2)

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(white)
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, white)
    DISPLAYSURF.blit(scores, (20,20))


    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
  
    # Instead of immediately removing collided coins, check their type first
    collided_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collided_coins:
        if isinstance(coin, Coin):
            SCORE += 1  # Increase score for Coin
            coin.kill()  # Remove the collected coin
            new_C1 = Coin()  # Spawn a new Coin
            coins.add(new_C1)
            all_sprites.add(new_C1)
            
        elif isinstance(coin, Coin2):
            SCORE -= 1  # Decrease score for Coin2
            coin.kill()  # Remove the collected coin
            new_C2 = Coin2()  # Spawn a new Coin2
            coins.add(new_C2)
            all_sprites.add(new_C2)
           
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(red)
        DISPLAYSURF.blit(game_over, (30,250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)   
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
