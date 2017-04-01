import pygame
import random
from pygame.locals import *

class Tilemap:
    tilemap = [] # The actual tilemap

    def __init__(self, textures, tilesize, width, height, borders=0):
        self.textures = textures # List of textures in dictionary format
        self.tilesize = tilesize + borders # The size of a tile
        self.width = width # How many tiles wide the map is
        self.height = height # How many tile high the map is
        self.window_size = [self.tilesize*self.width-borders,
                            self.tilesize*self.height-borders]

    def generate_random(self):
        """Generate a random tilemap"""
        self.tilemap = [[random.randint(0, len(self.textures)-1) for e in range(
        self.width)] for e in range(self.height)]

    def fill(self, texture):
        """Fill the entire tilemap with a certain texture"""
        self.tilemap = [[texture for e in range(self.width)] for e in range(
        self.height)]

    def fill_row(self, texture, row, freq=0, skip=[]):
        """Randomly place a texture in a column"""
        for i in range(0, self.width):
            if random.randint(0, freq) == freq:
                if self.tilemap[row][i] in skip:
                    pass
                else:
                    self.tilemap[row][i] = texture

    def fill_col(self, texture, col, freq=0, skip=[]):
        """Randomly place a texture in a row"""
        for i in range(0, self.height):
            if random.randint(0, freq) == freq:
                if self.tilemap[i][col] in skip:
                    pass
                else:
                    self.tilemap[i][col] = texture

    def replace(self, textures, replacement):
        """Replace every instance of a texture with another one"""
        for row in range(self.height):
            for column in range(self.width):
                if self.tilemap[row][column] in textures:
                    self.tilemap[row][column] = replacement

    def next_to(self, position, tile):
        """Check if a tile is next to another one"""
        try:
            if self.tilemap[position[0]][position[1]+1] == tile:
                return True
        except IndexError: pass
        try:
            if self.tilemap[position[0]][position[1]-1] == tile:
                return True
        except IndexError: pass
        try:
            if self.tilemap[position[0]+1][position[1]] == tile:
                return True
        except IndexError: pass
        try:
            if self.tilemap[position[0]-1][position[1]] == tile:
                return True
        except IndexError: pass
        return False
    def get_tile(self, position, tiles):
        """Check if a tilemap position contains a certain tile"""
        if self.tilemap[position[0]][position[1]] in tiles:
            return True
        else:
            return False

    def draw(self, display):
        """Draw the tilemap"""
        for row in range(self.height):
            for column in range(self.width):
                display.blit(self.textures[self.tilemap[row][column]],
                                    (column*self.tilesize,
                                     row*self.tilesize))
