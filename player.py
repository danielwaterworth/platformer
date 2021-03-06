import sys
import itertools
import pygame
import shapes

flip_image = lambda image: pygame.transform.flip(image, True, False)

duck_file = './sprites/p1_duck.png'
front_file = './sprites/p1_front.png'
jump_file = './sprites/p1_jump.png'

walk_files = [
    './sprites/p1_walk01.png',
    './sprites/p1_walk02.png',
    './sprites/p1_walk03.png',
    './sprites/p1_walk04.png',
    './sprites/p1_walk05.png',
    './sprites/p1_walk06.png',
    './sprites/p1_walk07.png',
    './sprites/p1_walk08.png',
    './sprites/p1_walk09.png',
    './sprites/p1_walk10.png',
    './sprites/p1_walk11.png'
]

front_image = pygame.image.load(front_file)
jump_right_image = pygame.image.load(jump_file)
jump_left_image = flip_image(jump_right_image)
duck_right_image = pygame.image.load(duck_file)
duck_left_image = flip_image(duck_right_image)

right_walk_images = [pygame.image.load(filename) for filename in walk_files]
left_walk_images = [flip_image(image) for image in right_walk_images]

def right_player_iterator():
    return itertools.cycle(right_walk_images)

def left_player_iterator():
    return itertools.cycle(left_walk_images)

stationary_iterator = itertools.repeat(front_image)
jump_right_iterator = itertools.repeat(jump_right_image)
jump_left_iterator = itertools.repeat(jump_left_image)
duck_right_iterator = itertools.repeat(duck_right_image)
duck_left_iterator = itertools.repeat(duck_left_image)

jump_sound_file = './sounds/jump.ogg'

jump_sound = pygame.mixer.Sound(jump_sound_file)

class Player(object):
    def __init__(self, level):
        self.level = level
        self.player_iterator = stationary_iterator

        self.image = next(self.player_iterator)
        self.before_x = 0
        self.before_y = 0
        self.x = 0
        self.y = 0

        self.x_vect = 0
        self.y_vect = 0

        self.in_air = False
        self.crounching = False

    @property
    def width(self):
        return self.image.get_rect().width

    def step(self, go_up, go_down, go_left, go_right):
        self.before_x = self.x
        self.before_y = self.y

        self.x += self.x_vect
        self.y += self.y_vect

        if go_up and not self.in_air:
            jump_sound.play()
            self.in_air = True
            if self.x_vect < 0:
                self.player_iterator = jump_left_iterator
            else:
                self.player_iterator = jump_right_iterator
            self.y_vect = 15
        elif self.in_air:
            self.y_vect -= 1

            if self.y_vect < 0:
                collision_parallelogram = shapes.HParallelogram(self.before_x, self.x, self.width, self.before_y, self.y)
                for hline in self.level.platforms():
                    if collision_parallelogram.collide_hline(hline):
                        self.y = hline.y
                        self.y_vect = 0
                        self.in_air = False
                        if go_left:
                            self.player_iterator = left_player_iterator()
                        elif go_right:
                            self.player_iterator = right_player_iterator()
                        else:
                            self.player_iterator = stationary_iterator
                        break
                else:
                    if self.y < 0:
                        self.y = 0
                        self.y_vect = 0
                        self.in_air = False
                        if go_left:
                            self.player_iterator = left_player_iterator()
                        elif go_right:
                            self.player_iterator = right_player_iterator()
                        else:
                            self.player_iterator = stationary_iterator
        else:
            if go_down and not self.ducking:
                self.ducking = True
                if self.x_vect < 0:
                    self.player_iterator = duck_left_iterator
                else:
                    self.player_iterator = duck_right_iterator
                self.x_vect = 0
            elif not go_down:
                self.ducking = False
                if go_left and self.x_vect >= 0:
                    self.x_vect = -5
                    self.player_iterator = left_player_iterator()
                elif go_right and self.x_vect <= 0:
                    self.x_vect = 5
                    self.player_iterator = right_player_iterator()
                elif not go_left and not go_right:
                    self.x_vect = 0
                    self.player_iterator = stationary_iterator

        self.image = next(self.player_iterator)
