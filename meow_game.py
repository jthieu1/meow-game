# Authors: Jenny Thieu and Jennifer Tran
# Start date: 10/26/2022
# Meow Game with PyGame

import pygame       # import pygame package to create working game
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864          # set game window size
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))     # display the window
pygame.display.set_caption('Meow Game')         # set the window name

ground_scroll = 0   # speed which ground scrolls
scroll_speed = 4

bg = pygame.image.load('images/bg.png')        # load resources used
ground_img = pygame.image.load('images/terrain.png')


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

    def update(self):

        self.counter += 1       # increase counter for animation
        tap_cooldown = 5    # after tapping five times, resets the animation so it can replay

        if self.counter > tap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]    # update the image after the reset


cat_pack = pygame.sprite.Group()

thickems = Cat(100, int(screen_height / 2))

cat_pack.add(thickems)     # add Thickems to our sprite group

run_game = True
while run_game:      # run game loop

    clock.tick(fps)

    screen.blit(bg, (0, 0))     # draws the background
    cat_pack.draw(screen)      # draws Thickems the Cat onto screen
    cat_pack.update()          # update Thickems

    screen.blit(ground_img, (ground_scroll, 768))   # draws the ground and scrolls
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():        # press X on window to exit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
