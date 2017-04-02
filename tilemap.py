import pygame
import random
import json
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
        self.mapsize = [self.width, self.height]

    def generate_random(self, exclude=[]):
        """Generate a random tilemap"""
        allowed = list(range(len(self.textures)))
        for texture in exclude:
            allowed.remove(texture)
        self.tilemap = [[random.choice(allowed) for e in range(
        self.width)] for e in range(self.height)]

    def generate(self, number, life, tile):
        """Generate 'blobs' of textures using 'ants'"""
        ants = []
        for i in range(number):
            ants.append(Ant([random.randint(0, self.width-1),
             random.randint(0, self.height-1)], life, self.mapsize,
             self, tile))

        for ant in ants:
            while ant.life > 1:
                ant.move()
                try:
                    self.tilemap[ant.position[0]][ant.position[1]] = ant.tile
                except IndexError:
                    ant.position[0] += 1
                    ant.position[1] += 1
            ants.remove(ant)

    def fill(self, texture):
        """Fill the entire tilemap with a certain texture"""
        self.tilemap = [[texture for e in range(self.width)] for e in range(
        self.height)]

    def fill_row(self, texture, row, freq=0, skip=[], pos=[0, None]):
        """Place a texture in a row"""
        if pos[1] == None:
            pos[1] = self.width
        for i in range(pos[0], pos[1]):
            if random.randint(0, freq) == freq:
                if self.tilemap[row][i] in skip:
                    pass
                else:
                    self.tilemap[row][i] = texture

    def fill_col(self, texture, col, freq=0, skip=[], pos=[0, None]):
        """Place a texture in a column"""
        if pos[1] == None:
            pos[1] = self.width
        for i in range(pos[0], pos[1]):
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

    def remove_single(self, tiles, replacement):
        """Remove single tiles"""
        for tile in tiles:
            for row in range(self.height):
                for column in range(self.width):
                    if self.tilemap[row][column] == tile:
                        if not self.next_to([row, column], tile):
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

    def json_dump(self, file_name):
        """Save the tilemap as a JSON file"""
        with open(file_name, 'w') as f:
            dumped = json.dumps(self.tilemap)
            f.write(dumped)

    def json_load(self, file_name):
        """Load a JSON file"""
        with open(file_name, 'r') as f:
            self.tilemap = json.load(f.read())

    def draw(self, display):
        """Draw the tilemap"""
        for row in range(self.height):
            for column in range(self.width):
                display.blit(self.textures[self.tilemap[row][column]],
                                    (column*self.tilesize,
                                    row*self.tilesize))

class Ant:
    # Ant idea from http://stackoverflow.com/a/4800633/5198106... Thank you!
    """Moves around randomly, creating 'realistic' blobs of textures"""
    def __init__(self, position, life, mapsize, tilemap, tile):
        self.position = position
        self.life = life
        self.mapsize = mapsize
        self.tilemap = tilemap
        self.tile = tile

    def move(self):
        """Move in a random direction"""
        direction = random.randint(0, 3)
        if direction == 0: self.position[0] += 1
        elif direction == 1: self.position[0] -= 1
        elif direction == 2: self.position[1] += 1
        elif direction == 3: self.position[1] -= 1
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[0] > self.mapsize[0]:
            self.position[0] = self.mapsize[0]
        if self.position[1] < 0:
            self.position[1] = 1
        if self.position[1] > self.mapsize[1]:
            self.position[1] = self.mapsize[1]
        self.life -= 1
        if not self.tilemap.next_to(self.position, self.tile):
            self.move()
