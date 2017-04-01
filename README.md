# PyTilemap
A simple tilemap engine for PyGame.

PyTilemap makes making tilemaps with PyGame much easier. Just a few lines of code and you can create a beautiful map.

Here's a really simple map I created using PyTilemap:

![A simple map](m654z.github.io/tilemap.PNG)

And here's the code:

    import pygame
    import sys
    from tilemap import Tilemap

    pygame.init()

    tilemap = Tilemap({
        # Load the textures
        0: pygame.image.load("dirt.png"),
        1: pygame.image.load("grass.png"),
        2: pygame.image.load("forest.png")},
                      
        38, # Tile size
        10, # Width
        10, # Height
        2) # Border size (default is 0)

    DISPLAYSURF = pygame.display.set_mode(tilemap.window_size)
    tilemap.fill(1) # Fill the map with 1 (grass)
    tilemap.fill_row(0, 2) # Fill row 2 with 0 (dirt)
    tilemap.fill_col(0, 2) # Fill column 2 with 0 (dirt)
    tilemap.fill_row(2, 3, skip=[0]) # Fill row 3 with 2 (forest), skipping dirt
    tilemap.fill_row(2, 1, skip=[0]) # Etc.
    tilemap.fill_col(2, 3, skip=[0])
    tilemap.fill_col(2, 1, skip=[0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tilemap.draw(DISPLAYSURF) # Draw the map
        pygame.display.update()
