import sys, pygame
import itertools
import player

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)

p1 = player.Player()

pygame.time.set_timer(pygame.USEREVENT, 16)
clock = pygame.time.Clock()

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
    rect = p1.image.get_rect()
    rect.bottom = 600 - p1.y
    rect.x = p1.x
    screen.blit(p1.image, rect)
    pygame.display.flip()

    clock.tick(50)
