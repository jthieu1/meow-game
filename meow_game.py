# Authors: Jenny Thieu, Jennifer Tran, and Yu "Dan" Liang
# Start date: 10/26/2021
# Meow Game with PyGame

import pygame
from pygame.locals import *
from pygame import mixer

import random

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# Framerate
clock = pygame.time.Clock()
fps = 60
low_fps = 30

# Window size
screen_width = 864
screen_height = 936

# Colors for fonts
black = (0, 0, 0)
white = (255, 255, 255)
baby_blue = (137, 207, 240)

# Screen display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Meow Game')  # set the window name
font = pygame.font.SysFont('Benton Sans', 60)  # font setting
small_font = pygame.font.SysFont('Benton Sans', 35)

# Game variables
ground_scroll = 0  # speed which ground scrolls
scroll_speed = 4
jumping = False
game_over = False
column_gap = 200
column_frequency = 1500  # how often pipes spawn in milliseconds
ravioli_frequency = 1600
last_column = pygame.time.get_ticks() - column_frequency  # interval between last column
last_ravi = pygame.time.get_ticks() - ravioli_frequency
score = 0
pass_column = False

# Images Section
bg = pygame.image.load('images/bg.png')  # load resources used
ground_img = pygame.image.load('images/terrain.png')
tryHarder_img = pygame.image.load('images/tryagain.png')  # Game over button

# Sound Section
pygame.mixer.music.load('sound/track01.wav')
pygame.mixer.music.play(-1, 0.0, 0)  # music starts immediately at third 0
ravioli_fx = pygame.mixer.Sound('sound/ravioli.wav')
ravioli_fx.set_volume(0.5)


# Text render
def draw_text(text, font, text_clr, x_coord, y_coord):
    """Draws the font to appear on screen"""
    img = font.render(text, True, text_clr)
    screen.blit(img, (x_coord, y_coord))


# Score reset
def reset_game():
    """Resets the score and the game"""
    column_group.empty()
    thickems.rect.x = 100
    thickems.rect.y = int(screen_height / 2)
    score = 0
    return score


# Sprite class for Thickems
class Cat(pygame.sprite.Sprite):
    """Thickems the Cat player sprite class"""

    def __init__(self, x_coord, y_coord):  # construct x and y coordinates
        """Loads the Thickems sprite and sets his speed and rect values"""
        pygame.sprite.Sprite.__init__(self)
        self.images = []  # images used are sorted in a list
        self.index = 0  # start at first image
        self.counter = 0  # control speed of animation
        for num in range(1, 4):  # there are three sprites for thickems, iterate the loop
            img = pygame.image.load(f'images/thickems{num}.png')  # load thickems sprite based on animations in list
            self.images.append(img)  # add image to list
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()  # create rectangle from boundaries of images
        self.rect.center = [x_coord, y_coord]  # center based off coordinates
        self.velocity = 0  # set up velocity
        self.clicking = False

    def update(self):
        """Updates the jumping and game over conditions"""
        if jumping:
            self.velocity += 0.5  # speed Thickems moves
            if self.velocity > 8:
                self.velocity = 8  # reset velocity Thickems will fall so it doesn't keep increasing
            if self.rect.bottom < 768:  # gravity, Thickems will fall down
                self.rect.y += int(self.velocity)

        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicking == False:  # jump button
                self.clicking = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:  # Reset clicking
                self.clicking = False

            self.counter += 1  # increase counter for animation
            tap_cooldown = 5  # after tapping five times, resets the animation so it can replay

            if self.counter > tap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]  # update the image after the reset
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -3)  # affect rotation
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -250)  # rotate 90 degrees


class Column(pygame.sprite.Sprite):
    """Creates column sprite"""
    def __init__(self, x_coord, y_coord, position):
        """Initialize coordinates and load the sprite image"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/column.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)  # position columns upside down
            self.rect.bottomleft = [x_coord, y_coord - int(column_gap / 2)]
        if position == -1:
            self.rect.topleft = [x_coord, y_coord + int(column_gap / 2)]  # position column on ground

    def update(self):
        """Updates to have the columns continuously scroll along with the player's screen"""
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


# Restart button
class Restart():
    """Create restart button"""
    def __init__(self, x_coord, y_coord, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_coord, y_coord)

    def draw(self):
        """Creates the button setting and conditions"""
        click = False

        # Mouse position
        pos = pygame.mouse.get_pos()

        # Checks if user's mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                click = True

        # Draws the button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return click


# Ravioli sprite
class Ravioli(pygame.sprite.Sprite):
    """Creates the ravioli sprite"""
    def __init__(self, x_coord, y_coord):
        """Load the ravioli image at 50% scaled size and draws coordinates"""
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/ravioli.png')
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x_coord, y_coord)

    def update(self):
        """Updates to have ravioli scroll along with player's screen"""
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


# Sprite variables
cat_pack = pygame.sprite.Group()
column_group = pygame.sprite.Group()
ravioli_group = pygame.sprite.Group()

thickems = Cat(100, int(screen_height / 2))

button = Restart(screen_width // 2 - 50, screen_height // 2 - 100, tryHarder_img)

cat_pack.add(thickems)  # add Thickems to our sprite group
score_ravi = Ravioli(75, 75)
ravioli_group.add(score_ravi)

# Run the game in a loop
run_game = True
while run_game:

    clock.tick(fps)

    screen.blit(bg, (0, 0))  # draws the background
    cat_pack.draw(screen)  # draws Thickems the Cat onto screen
    cat_pack.update()  # update Thickems
    column_group.draw(screen)  # draws columns onto screen
    ravioli_group.draw(screen)  # draws ravioli onto screen

    screen.blit(ground_img, (ground_scroll, 768))  # draws the ground and scrolls

    # check score
    if len(column_group) > 0:  # check length of pipe group for scoring
        if cat_pack.sprites()[0].rect.left > column_group.sprites()[0].rect.left \
                and cat_pack.sprites()[0].rect.right < column_group.sprites()[0].rect.right \
                and pass_column == False:
            pass_column = True
        if pass_column:
            if cat_pack.sprites()[0].rect.left > column_group.sprites()[0].rect.right:
                score += 1  # add score when column is passed
                pass_column = False
        if pygame.sprite.spritecollide(thickems, ravioli_group, True):
            score += 1
            ravioli_fx.play()

    draw_text(str(score), font, black, int(screen_width / 2), 20)  # draw the score to be visible

    # collide and game over
    if pygame.sprite.groupcollide(cat_pack, column_group, False, False) or thickems.rect.top < 0:
        game_over = True

    if thickems.rect.bottom > 768:  # if Thickems hit the ground, set condition for GAME OVER
        game_over = True
        jumping = False

    # when game not over spawn columns and ravioli
    if not game_over and jumping:
        time_now = pygame.time.get_ticks()
        time_now2 = pygame.time.get_ticks()
        if time_now - last_column > column_frequency:
            column_height = random.randint(-100, 100)
            btm_column = Column(screen_width, int(screen_height / 2) + column_height, -1)
            top_column = Column(screen_width, int(screen_height / 2) + column_height, 1)
            column_group.add(btm_column)
            column_group.add(top_column)

            last_column = time_now
        if time_now2 - last_ravi > ravioli_frequency:  # affect spawn in milliseconds
            ravioli = Ravioli(random.randint(360, (screen_width - 420)), random.randint(360, (screen_width - 420)))
            ravioli_group.add(ravioli)

            last_ravi = time_now2

        ground_scroll -= scroll_speed  # draws ground and scrolls
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        column_group.update()  # call to update columns
        ravioli_group.update()  # call to update raviolis

# Game over and make restart button selectable to player
    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        if event.type == pygame.MOUSEBUTTONDOWN and jumping == False and game_over == False:
            # player will start with Thickems in air
            jumping = True  # Thickems can jump

    pygame.display.update()

pygame.quit()
