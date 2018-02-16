import pygame
import shapes

def load_tile(filename):
    image = pygame.image.load(filename)
    rect = image.get_rect()
    assert rect.width == 70
    assert rect.height == 70
    return image

background_filename = './sprites/background.png'
grass_filename = './sprites/grass.png'
grass_mid_filename = './sprites/grassMid.png'
grass_center_filename = './sprites/grassCenter.png'
grass_left_filename = './sprites/grassLeft.png'
grass_right_filename = './sprites/grassRight.png'

background_image = pygame.image.load(background_filename)
grass_image = load_tile(grass_filename)
grass_mid_image = load_tile(grass_mid_filename)
grass_center_image = load_tile(grass_center_filename)
grass_left_image = load_tile(grass_left_filename)
grass_right_image = load_tile(grass_right_filename)

class Level(object):
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.grid = grid
        grid.reverse()

    def is_filled(self, i, j):
        if i < 0:
            return True
        if j < 0:
            return True
        if i >= self.width:
            return True
        if j >= self.height:
            return True
        return self.grid[j][i]

    def rects(self):
        for i in xrange(self.width):
            for j in xrange(self.height):
                if self.is_filled(i, j):
                    rect = grass_mid_image.get_rect().move(i*70, (j+1)*70)

                    filled_above = self.is_filled(i, j+1)
                    filled_left = self.is_filled(i-1, j)
                    filled_right = self.is_filled(i+1, j)

                    if filled_above:
                        yield (grass_center_image, rect)
                    elif filled_left and filled_right:
                        yield (grass_mid_image, rect)
                    elif filled_left:
                        yield (grass_right_image, rect)
                    elif filled_right:
                        yield (grass_left_image, rect)
                    else:
                        yield (grass_image, rect)

    def platforms(self):
        for i in xrange(self.width):
            for j in xrange(self.height):
                if self.is_filled(i, j):
                    filled_above = self.is_filled(i, j+1)
                    if not filled_above:
                        yield shapes.HLine(i*70, (i+1)*70, (j+1)*70)
