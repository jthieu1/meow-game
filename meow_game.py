# Authors: Jenny Thieu, Jennifer Tran, and Yu "Dan" Liang
# Start date: 10/26/2021
# Meow Game with PyGame

import pygame       # import pygame package to create working game
from pygame.locals import *
from pygame import mixer    # import ability to play sound
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()     # set framerate of game
fps = 60

screen_width = 864          # set game window size
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))     # display the window
pygame.display.set_caption('Meow Game')         # set the window name

ground_scroll = 0   # speed which ground scrolls
scroll_speed = 4
jumping = False
game_over = False
column_gap = 200
column_frequency = 1500     # how often pipes spawn in milliseconds
last_column = pygame.time.get_ticks() - column_frequency    # interval between last column

bg = pygame.image.load('images/bg.png')        # load resources used
ground_img = pygame.image.load('images/terrain.png')

pygame.mixer.music.load('sound/track01.wav')
pygame.mixer.music.play(-1, 0.0, 0)     # music starts immediately at third 0


class Cat(pygame.sprite.Sprite):        # class for our player sprite, Thickems the Cat
    def __init__(self, x_coord, y_coord):           # construct x and y coordinates
        pygame.sprite.Sprite.__init__(self)
        self.images = []        # images used are sorted in a list
        self.index = 0          # start at first image
        self.counter = 0        # control speed of animation
        for num in range(1, 4):         # there are three sprites for thickems, iterate the loop
            img = pygame.image.load(f'images/thickems{num}.png')    # load thickems sprite based on animations in list
            self.images.append(img)     # add image to list
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()       # create rectangle from boundaries of images
        self.rect.center = [x_coord, y_coord]   # center based off coordinates
        self.velocity = 0       # set up velocity
        self.clicking = False

    def update(self):

        if jumping:
            self.velocity += 0.5        # speed Thickems moves
            if self.velocity > 8:
                self.velocity = 8       # reset velocity Thickems will fall so it doesn't keep increasing
            if self.rect.bottom < 768:      # gravity, Thickems will fall down
                self.rect.y += int(self.velocity)

        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicking == False:   # jump button
                self.clicking = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:  # Reset clicking
                self.clicking = False

            self.counter += 1       # increase counter for animation
            tap_cooldown = 5    # after tapping five times, resets the animation so it can replay

            if self.counter > tap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]    # update the image after the reset
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -3)   # affect rotation
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -250)  # rotate 90 degrees


class Column(pygame.sprite.Sprite):     # create class for column sprite
    def __init__(self, x_coord, y_coord, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/column.png')     # load the column image
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)     # position columns upside down
            self.rect.bottomleft = [x_coord, y_coord - int(column_gap / 2)]
        if position == -1:
            self.rect.topleft = [x_coord, y_coord + int(column_gap / 2)]    # position column on ground

    def update(self):       # have columns scroll along in the game with player
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Coin(pygame.sprite.Sprite):      # class for our coin sprite, using thickems3.png as the placeholder atm.
    def __init__(self, x_coord, y_coord):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/thickems3.png')  # Replace thickems3 once we find a coin
        self.image = pygame.transform.scale(img, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (x_coord, y_coord)

    def update(self):       # have columns scroll along in the game with player
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


cat_pack = pygame.sprite.Group()    # variable for sprites
column_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

thickems = Cat(100, int(screen_height / 2))

cat_pack.add(thickems)     # add Thickems to our sprite group

run_game = True
while run_game:      # run game loop

    clock.tick(fps)

    screen.blit(bg, (0, 0))     # draws the background
    cat_pack.draw(screen)      # draws Thickems the Cat onto screen
    cat_pack.update()          # update Thickems
    column_group.draw(screen)  # draws columns onto screen
    coin_group.draw(screen)    # draws coins onto screen

    screen.blit(ground_img, (ground_scroll, 768))   # draws the ground and scrolls

    if pygame.sprite.groupcollide(cat_pack, column_group, False, False) or thickems.rect.top < 0:   # for collision
        game_over = True

    if thickems.rect.bottom > 768:  # if Thickems hit the ground, set condition for GAME OVER
        game_over = True
        jumping = False

    if not game_over:   # condition for game to generate columns when not game over
        time_now = pygame.time.get_ticks()
        if time_now - last_column > column_frequency:
            column_height = random.randint(-100, 100)
            btm_column = Column(screen_width, int(screen_height / 2) + column_height, -1)
            top_column = Column(screen_width, int(screen_height / 2) + column_height, 1)
            coins = Coin(500, 500)
            column_group.add(btm_column)
            column_group.add(top_column)
            coin_group.add(coins)

            last_column = time_now

        ground_scroll -= scroll_speed   # draws ground and scrolls
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        column_group.update()       # call to update columns
        coin_group.update()

    for event in pygame.event.get():        # press X on window to exit game
        if event.type == pygame.QUIT:
            run_game = False
        if event.type == pygame.MOUSEBUTTONDOWN and jumping == False and game_over == False:
            # player will start with Thickems in air
            jumping = True  # Thickems can jump

    pygame.display.update()

pygame.quit()
