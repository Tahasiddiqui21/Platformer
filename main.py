import pygame
from pygame import mixer
import random

pygame.init()

# const variables, that load images
APPLE = pygame.image.load('apple.png')
ENEMY = pygame.image.load('enemy.png')
HEART = pygame.image.load('heart.png')

clock = pygame.time.Clock()

# setting the width and the height of the screen
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))

# map grid
tile_size = 50


# player class
class Player:
    def __init__(self):
        self.hearts = 3  # player lives
        self.img = pygame.transform.scale2x(pygame.image.load('tile000.png'))  # loading the img
        self.rect = self.img.get_rect(center=(width / 2, height / 2))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.speed = 5
        self.vel_x = 0
        self.vel_y = 5
        self.is_on_ground = False

    # draw the player func
    def draw(self, window):
        window.blit(self.img, self.rect)

    # update function
    def update(self):
        # setting x and y velocity
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
        elif keys[pygame.K_d]:
            self.vel_x = self.speed
        else:
            self.vel_x = 0

        # checking if is on ground
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                self.is_on_ground = True
                break
        is_on_any_tile = False
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect):
                is_on_any_tile = True

        if not is_on_any_tile:
            self.is_on_ground = False

        # checking for collision
        for tile in world.tile_list:
            # checking in x direction
            if tile[1].colliderect(self.rect.x + self.vel_x, self.rect.y + 2, self.width, self.height - 4):
                self.vel_x = 0

            # checking in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + self.vel_y, self.width, self.height):
                self.vel_y = 0

        # gravity and jumping
        if self.vel_y < 10:
            self.vel_y += 0.2
        if self.vel_y <= -10:
            self.vel_y = -10

        # moving the player left or right and up or down
        self.rect.centery += self.vel_y
        self.rect.centerx += self.vel_x


# enemy class
class Enemies:
    def __init__(self):
        self.x = width + 100
        self.y = random.randint(70, height - 70)
        self.img = ENEMY
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.speed = 2

    # draw enemy func
    def draw(self, window):
        window.blit(self.img, self.rect)

    # update func
    def update(self):
        self.rect.centerx -= self.speed  # moving enemy left


# apple class
class Apple:
    def __init__(self):
        self.x = random.randint(70, width - 70)
        self.y = 100
        self.img = APPLE
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.fall_speed = 3
        self.counter = 0
        self.timer = 0

    # drawing the apple
    def draw(self, window):
        window.blit(self.img, self.rect)

    # update func
    def update(self):
        self.rect.centery += self.fall_speed  # moving apple down

        # checking for collision with tiles
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + self.fall_speed, self.width, self.height):
                self.rect.bottom = tile[1].top

        # setting the timer
        self.counter += 1
        if self.counter >= 144:
            self.timer += 1
            self.counter = 0


# world class
class World:
    def __init__(self, data):
        # loading dirt and grass images
        dirt = pygame.image.load('Dirt.png')
        grass = pygame.image.load('Grass.png')
        # storing all the tiles
        self.tile_list = []
        row_count = 0
        # going through all the tiles
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt, (tile_size, tile_size))  # scaling the image to the tile size
                    img_rect = img.get_rect(topleft=(col_count * tile_size, row_count * tile_size))
                    tile = (img, img_rect)
                    self.tile_list.append(tile)  # adding the tile to the tile list
                if tile == 2:
                    img = pygame.transform.scale(grass, (tile_size, tile_size))
                    img_rect = img.get_rect(topleft=(col_count * tile_size, row_count * tile_size))
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    # drawing all the tiles from the tile list
    def draw(self, window):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])


# the tile map
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)
player = Player()


# creating the write func that will display text on the screen
def write(size, x, y, text, color):
    bird_font = pygame.font.Font('font.ttf', size)
    font_surf = bird_font.render(text, True, color)
    font_rect = font_surf.get_rect(center=(x, y))
    screen.blit(font_surf, font_rect)


# the main function
def main():
    run = True
    score = 0  # setting the score
    APPLESPAWN = pygame.USEREVENT + 1  # creating the apple spawn event
    pygame.time.set_timer(APPLESPAWN, 1000)  # calling the event every 1000 ms
    apple_group = []  # creating an empty apple group
    ENEMYSPAWN = pygame.USEREVENT + 2  # creating a second event called enemy spawn
    pygame.time.set_timer(ENEMYSPAWN, 2000)  # calling the event every 2000 ms
    enemy_group = []  # creating an empty enemy group
    game_state = 'game'

    # function called in the main loop that contains everything drawn to the screen
    def redraw_window():
        screen.fill((84, 230, 226))  # background color
        if game_state == 'game':
            world.draw(screen)
            player.draw(screen)
            player.update()
            write(20, width / 2, 80, f"score: {score}", (255, 255, 255))
            for apple in apple_group:
                apple.draw(screen)
                apple.update()
                write(20, apple.rect.centerx, apple.rect.centery, f"{3 - apple.timer}", (255, 255, 255))
            for enemy in enemy_group:
                enemy.draw(screen)
                enemy.update()
            for i in range(player.hearts):
                screen.blit(HEART, (40 * i + 80, 80))
            write(20, 800, 80, "press c to show controls", (255, 255, 255))

        if game_state == 'controls':
            write(50, width / 2, height / 2 - 100, "a - go left", (255, 255, 255))
            write(50, width / 2, height / 2, "d - go right", (255, 255, 255))
            write(50, width / 2, height / 2 + 100, "space - jump", (255, 255, 255))
            write(20, 880, 30, "press c to play", (255, 255, 255))
            write(30, width / 2, 80, "goal - reach score 100", (255, 255, 255))

        pygame.display.update()

    # the main loop
    while run:
        redraw_window()  # calling the redraw func
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # jumping and jump sound effect
                if event.key == pygame.K_SPACE and player.is_on_ground:
                    player.vel_y = -20
                    jump_sound = mixer.Sound('sounds/jump.wav')
                    jump_sound.set_volume(0.05)
                    jump_sound.play()
                # control screen
                if event.key == pygame.K_c and game_state == 'game':
                    game_state = 'controls'
                elif event.key == pygame.K_c and game_state == 'controls':
                    game_state = 'game'
            # adding an apple to the apple group everytime apple spawn event is called
            if event.type == APPLESPAWN and game_state == 'game':
                apple_group.append(Apple())
            # adding an enemy to the enemy group everytime enemy spawn event is called
            if event.type == ENEMYSPAWN and game_state == 'game':
                enemy_group.append(Enemies())

        for apple in apple_group:
            # checking for apple collision with player and adding sound
            if apple.rect.colliderect(player.rect):
                apple_group.remove(apple)
                score += 1
                apple_sound = mixer.Sound('sounds/apple.wav')
                apple_sound.set_volume(0.01)
                apple_sound.play()
            # removing apple sound after 3 seconds
            if apple.timer >= 3:
                apple_group.remove(apple)

        # checking for enemy collision with the player and adding sound
        for enemy in enemy_group:
            if enemy.rect.colliderect(player.rect):
                enemy_group.remove(enemy)
                player.hearts -= 1
                hit_sound = mixer.Sound('sounds/hit.wav')
                hit_sound.set_volume(0.05)
                hit_sound.play()

        # setting lose condition
        if player.hearts <= 0:
            run = False
            main_menu('loss')

        # setting win condition
        if score >= 100:
            run = False
            main_menu('win')

        # setting the frame rate
        clock.tick(144)


# the main menu func
def main_menu(type):
    menu_run = True

    def redraw_window():
        screen.fill((39, 168, 164))
        if type == 'main_menu':
            write(50, width / 2, height / 2, "Press mouse button to play", (0, 0, 255))
        if type == 'loss':
            write(50, width / 2, height / 2, "You lost", (0, 0, 255))
            write(30, width / 2, height / 2 + 200, "Press mouse button to play again", (0, 0, 255))
        if type == 'win':
            write(50, width / 2, height / 2, "Thank You for playing!", (0, 0, 255))
            write(30, width / 2, height / 2 + 200, "Press mouse button to play again", (0, 0, 255))
        pygame.display.update()

    while menu_run:
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_run = False
                player.hearts = 3
                player.rect.center = (width / 2, height / 2)
                main()


main_menu('main_menu')
