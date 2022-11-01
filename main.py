# content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
# from platform import platform
# Andrew :OOOOOO
'''
Patch Notes 2.25
add player vs player
player collision
preset platforms
'''
import pygame as pg
from pygame.sprite import Sprite
import random
import math 

vec = pg.math.Vector2

# game settings 
WIDTH = 1280
HEIGHT = 720
FPS = 30

# player settings
PLAYER_GRAVITY = 0.8

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RANDOMCOLOR = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

# score
SCORE = 0
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# sprites...
class Player(Sprite):
    def __init__(self):
        # defines player sprite parameters
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        #Player spawn location
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    # what happens when a key gets pressed: horizontal movement
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -2.5
        if keys[pg.K_RIGHT]:
            self.acc.x = 2.5
    # vertical jump
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -40
    # updating all movement and acceleration and gravity
    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        self.controls()
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        # if hits:
        #     print("platcollision")
        playerhits = pg.sprite.spritecollide(self, all_sprites, False)
        if playerhits:
            print("playercollision")
        # friction
        self.acc.x += self.vel.x * -0.1
        self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.rect.midbottom = self.pos
        #border
        if self.rect.x < 0:
            self.vel.x *= -1
            self.acc.x *= -1
        if self.rect.x > WIDTH - 50:
            self.vel.x *= -1
            self.acc.x *= -1
#2nd Player 
class Player2(Sprite):
    def __init__(self):
        # defines player sprite parameters
        Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    # what happens when a key gets pressed: horizontal movement
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -2.5
        if keys[pg.K_d]:
            self.acc.x = 2.5
    # vertical jump
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -40
    # updating all movement and acceleration and gravity
    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        self.controls()
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        # if hits:
        #     print("collision")
        # friction
        self.acc.x += self.vel.x * -0.1
        self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.rect.midbottom = self.pos
        #border
        if self.rect.x < 0:
            self.vel.x *= -1
            self.acc.x *= -1
        if self.rect.x > WIDTH - 50:
            self.vel.x *= -1
            self.acc.x *= -1

# creates platform class
# platforms is sublass of sprite
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    # new feature in update 23 (TELEPORT PLATFORMS WHEN ENEMY DIES)
    def update(self):
        enemyhits = pg.sprite.spritecollide(player, enemies, False)
        if enemyhits:
            self.rect.x = random.randint(0,WIDTH-100)
            self.rect.y = random.randint(50,HEIGHT-70)
        #for 2nd player
        enemyhits2 = pg.sprite.spritecollide(player2, enemies, False)
        if enemyhits2:
            self.rect.x = random.randint(0,WIDTH-100)
            self.rect.y = random.randint(50,HEIGHT-70)

class GroundPlatform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
# enemy is subclass of sprite
class Enemy(Sprite):
    def __init__(self, x, y, color, w, h, movex, movey):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.h = h
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.movex = movex
        self.movey = movey
    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey
        #border
        if self.rect.x < 0:
            self.movex *= -1
        if self.rect.x > WIDTH - self.w:
            self.movex *= -1
        if self.rect.y < 0:
            self.movey *= -1  
        if self.rect.y > HEIGHT - 50 - 25/2:
            self.movey *= -1
        
        

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Bitcoin Miner >:)")
clock = pg.time.Clock()
  
# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
enemies = pg.sprite.Group()


# instantiate the player class
player = Player()
player2 = Player2()
# enemy1 = Enemy(100, 200, RED, 25, 25)
def platY():
    return random.randint(100,250)
def platX():
    return random.randint(100,700)
groundplat = GroundPlatform(0, HEIGHT-35, WIDTH, 35)
plat = Platform(platX(), HEIGHT/2 + platY(), 100, 35)
plat2 = Platform(platX(), HEIGHT/2 + platY(), 100, 35)
plat3 = Platform(platX(), HEIGHT/2 + platY(), 100, 35)
plat4 = Platform(platX(), HEIGHT/2 + platY(), 100, 35)

#random number generator for colors
def colormaker():
    return random.randint(5,255)

#creates # of enemies with random starting pos, velo, and color
for i in range(20):
    
    x = random.randint(50, WIDTH - 51)
    y = random.randint(50, HEIGHT - 51)
    movex = random.randint(-2, 2)
    if movex == 0:
        movex = 2
    movey = random.randint(-2, 2)
    if movey == 0:
        movey = 2

    e = Enemy(x, y, (colormaker(), colormaker(), colormaker()), 25, 25, movex, movey)
    all_sprites.add(e)
    enemies.add(e)
    print(e)

# add player to all sprites group
all_sprites.add(player, player2, groundplat, plat, plat2, plat3, plat4)
all_platforms.add(groundplat, plat, plat2, plat3, plat4)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                player.jump()
        #for 2nd player
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player2.jump()
    #kill enemy and add score
    hits = pg.sprite.spritecollide(player, enemies, True)
    if hits:
        SCORE += 1
    #for 2nd player
    hits = pg.sprite.spritecollide(player2, enemies, True)
    if hits:
        SCORE += 1
    ############ Update ##############
    # update all sprites
    all_sprites.update()
    all_platforms.update()
    if player.vel.y > 0:
        hits = pg.sprite.spritecollide(player, all_platforms, False)
        if hits:
            player.pos.y = hits[0].rect.top
            player.vel.y = 0
    #still teleports to top
    if player.vel.y < 0:
        hits = pg.sprite.spritecollide(player, all_platforms, False)
        if hits:
            player.rect.top = hits[0].rect.bottom
            player.vel.y = 10
    #for 2nd player
    if player2.vel.y > 0:
        hits = pg.sprite.spritecollide(player2, all_platforms, False)
        if hits:
            player2.pos.y = hits[0].rect.top
            player2.vel.y = 0
    #still teleports to top
    if player2.vel.y < 0:
        hits = pg.sprite.spritecollide(player2, all_platforms, False)
        if hits:
            player2.rect.top = hits[0].rect.bottom
            player2.vel.y = 10
    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    #WIN Condition
    if SCORE == 20:
        draw_text("WE WIN ", 40, GREEN, WIDTH / 2, HEIGHT / 2)
    # draw all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()
