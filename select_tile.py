from settings import *
import pygame

class TileSelector:
    def __init__(self):
        self.selected_tile = 0
        self.images = [pygame.image.load(f"images/{i}").convert_alpha() for i in AVAILABLE_TILES]
        self.rotation_amount = 0

    def render(self, screen):
        for (i, tile) in enumerate(AVAILABLE_TILES):
            image = self.images[i]
            image_size = (GARDEN_TILE_SIZE*TILE_SELECTOR_SCALE, GARDEN_TILE_SIZE*TILE_SELECTOR_SCALE)
            image = pygame.transform.scale(image, image_size)

            image_rect = image.get_rect()
            
            y = TILE_SELECTOR_Y + (i%TOOLBAR_HEIGHT)*GARDEN_TILE_SIZE*TILE_SELECTOR_SCALE
            x = TILE_SELECTOR_X - (i//TOOLBAR_HEIGHT)*GARDEN_TILE_SIZE*TILE_SELECTOR_SCALE
            if i == self.selected_tile:
                image = pygame.transform.rotate(image, self.rotation_amount)

            screen.blit(image, (x, y))
            
            image_rect.left = x
            image_rect.top = y

            if i == self.selected_tile: color = (90, 90, 255)
            else: color = SELECTED_GRAY
            pygame.draw.rect(screen, color, image_rect, 2)
    
    def handle_click(self, pos):
        pos_x = pos[0]
        pos_y = pos[1]

        useful_pos = pos_x - (TILE_SELECTOR_X - (GARDEN_TILE_SIZE*TILE_SELECTOR_SCALE))

        if useful_pos < 0:
            return
        if pos_y - TILE_SELECTOR_Y >= (GARDEN_TILE_SIZE*TILE_SELECTOR_SCALE*len(AVAILABLE_TILES)//2):
            return

        tile = (pos_y - TILE_SELECTOR_Y) // (GARDEN_TILE_SIZE*TILE_SELECTOR_SCALE)
        if useful_pos <= GARDEN_TILE_SIZE*TILE_SELECTOR_SCALE:
            tile += 6
        self.selected_tile = tile
        self.rotation_amount = 0
        return tile

    def handle_text_input(self, letter):
        if letter == 'r' and self.selected_tile >= 6:
            self.rotation_amount += 90
            self.rotation_amount %= 360
            return True
