import sys, pygame
import itertools

front_file = './p1_walk/p1_front.png'
jump_file = './p1_walk/p1_jump.png'

walk_files = [
    './p1_walk/p1_walk01.png',
    './p1_walk/p1_walk02.png',
    './p1_walk/p1_walk03.png',
    './p1_walk/p1_walk04.png',
    './p1_walk/p1_walk05.png',
    './p1_walk/p1_walk06.png',
    './p1_walk/p1_walk07.png',
    './p1_walk/p1_walk08.png',
    './p1_walk/p1_walk09.png',
    './p1_walk/p1_walk10.png',
    './p1_walk/p1_walk11.png'
]

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)

front_image = pygame.image.load(front_file)
jump_image = pygame.image.load(jump_file)
right_walk_images = [pygame.image.load(filename) for filename in walk_files]
left_walk_images = [pygame.transform.flip(image, True, False) for image in right_walk_images]

def right_player_iterator():
    return itertools.cycle(right_walk_images)

def left_player_iterator():
    return itertools.cycle(left_walk_images)

stationary_iterator = itertools.repeat(front_image)
jump_iterator = itertools.repeat(jump_image)
player_iterator = stationary_iterator

image = next(player_iterator)
x = 0
y = 0
y_vect = 0

pygame.time.set_timer(pygame.USEREVENT, 16)

travelling_left = False
travelling_right = False
in_air = False

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

            if go_up and not in_air:
                in_air = True
                travelling_left = False
                travelling_right = False
                player_iterator = jump_iterator
                y_vect = 15

            if in_air:
                y += y_vect
                y_vect -= 1
                if y < 0:
                    y = 0
                    in_air = False
            else:
                if go_left and travelling_left:
                    x -= 5
                elif go_right and travelling_right:
                    x += 5
                else:
                    travelling_left = False
                    travelling_right = False

                    if go_left:
                        travelling_left = True
                        player_iterator = left_player_iterator()
                    elif go_right:
                        travelling_right = True
                        player_iterator = right_player_iterator()
                    else:
                        player_iterator = stationary_iterator

            image = next(player_iterator)

    screen.fill(black)
    rect = image.get_rect()
    rect.bottom = 600 - y
    rect.x = x
    screen.blit(image, rect)
    pygame.display.flip()
