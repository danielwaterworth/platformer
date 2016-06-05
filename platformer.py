import sys
import itertools
import pygame

pygame.init()

import player
import level
import shapes

size = width, height = 700, 700
black = 0, 0, 0

screen = pygame.display.set_mode(size)

pygame.time.set_timer(pygame.USEREVENT, 16)
clock = pygame.time.Clock()

grid = [
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, True,  False, False, False, False],
    [False, False, False, True,  False, False, False, False, False, False],
    [False, True,  True, False,  False, False, False, False, False, False]
]

l1 = level.Level(10, 10, grid)
p1 = player.Player(l1)

def world_to_screen(p):
    x, y = p
    return (x, 700 - y)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.USEREVENT:
            keys = pygame.key.get_pressed()

            left_pressed = keys[pygame.K_LEFT] == 1
            right_pressed = keys[pygame.K_RIGHT] == 1
            up_pressed = keys[pygame.K_UP] == 1
            down_pressed = keys[pygame.K_DOWN] == 1

            go_left = left_pressed and not right_pressed
            go_right = right_pressed and not left_pressed
            go_up = up_pressed and not down_pressed
            go_down = down_pressed and not up_pressed

            p1.step(go_up, go_down, go_left, go_right)

    screen.fill(black)

    # Render level
    for image, rect in l1.rects():
        rect.y = 700 - rect.y
        screen.blit(image, rect)

    # Render player
    rect = p1.image.get_rect()
    rect.bottom = 700 - p1.y
    rect.x = p1.x
    screen.blit(p1.image, rect)

    pygame.display.flip()

    clock.tick(50)
