import pygame
from settings import *

BASE_64_CONV = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+="

class Garden:
    def __init__(self, height, width, layout, available_plots=0):
        self.font = pygame.font.SysFont("Source Code Pro", 26)
        self.scroll_x = 0
        self.scroll_y = 0

        self.available_plots = available_plots
        self.height = height
        self.width = width

        # stored as a string for DB purposes
        self.grid = layout
        self.images = [pygame.image.load(f"images/{i}").convert_alpha() for i in AVAILABLE_TILES]
        self.adding_image = 0
        self.current_rotation = 0

    def rotate_selected(self):
        self.current_rotation += 1
        self.current_rotation %= 4

    def change_tile(self, tile_index):
        self.adding_image = tile_index
        self.current_rotation = 0

    def _get_tile_from_screen_pos(self, pos):
        # adjusts from the scroll
        x = (pos[0] - TOTAL_TASKBAR_WIDTH - 50 + self.scroll_x) // GARDEN_TILE_SIZE
        y = (pos[1] - 50 + self.scroll_y) // GARDEN_TILE_SIZE
        return (x, y)

    def _adjust_pos_to_offset(self, pos):
        x = (pos[0] - self.scroll_x)
        y = (pos[1] - self.scroll_y)
        return (x, y)

    # these two functions deal with rotation.
    # rotation is only done for the two river tiles
    # indexes 0, 1, 2, 3, 4, 5 represent the non-rotations
    # rest are rotations

    # this one converts index in image list to previous representation
    def _convert_out_index_to_rotation(index):
        if index <= 5:
            return index
        
        index -= 6
        index *= 4 # for the 4 rotations
        index += 6
        return index


    # this one converts previous representation into index in image list and rotation
    def _convert_rotated_index_to_img(index):
        if index <= 5:
            return (index, 0)
        index -= 6
        return ((index // 4) + 6, (index % 4) * 90)


    def render_garden(self, screen, mouse_pos, is_adding_task):
        # drawing stuff over it
        for i in range(self.height):
            base_index = i * self.width

            for j in range(self.width):
                x = GARDEN_TILE_SIZE * j + 50 + TOTAL_TASKBAR_WIDTH
                y = (GARDEN_TILE_SIZE * i) + 50
                
                adjusted = self._adjust_pos_to_offset((x, y))
                screen.blit(self.images[0], adjusted)

                tile = BASE_64_CONV.find(self.grid[base_index + j])
                if tile == 0:
                    continue

                (img_tile, rotation) = Garden._convert_rotated_index_to_img(tile)
                image = pygame.transform.rotate(self.images[img_tile], rotation)

                screen.blit(image, adjusted)
                
        #calculate (if any) which tile the mouse is on
        (highlighted_x, highlighted_y) = self._get_tile_from_screen_pos(mouse_pos)

        if not is_adding_task:
            if highlighted_x >= 0 and highlighted_x < self.width:
                if highlighted_y >= 0 and highlighted_y < self.height:
                    x = GARDEN_TILE_SIZE * highlighted_x + 50 + TOTAL_TASKBAR_WIDTH
                    y = (GARDEN_TILE_SIZE * highlighted_y) + 50

                    adjusted = self._adjust_pos_to_offset((x, y))
                    rect = pygame.rect.Rect(adjusted[0], adjusted[1], GARDEN_TILE_SIZE, GARDEN_TILE_SIZE)
                    pygame.draw.rect(screen, (0, 127, 0), rect)
        
    def render_info(self, screen):
        # render the number of plots left
        background_rect = pygame.Rect(0, TOTAL_TASKBAR_HEIGHT, TASK_RECT_WIDTH+10, 50)
        pygame.draw.rect(screen, SELECTED_GRAY, background_rect, 0, 5)

        text_value = f"number of plots left: {self.available_plots}"
        text = self.font.render(text_value, True, COLOR_BLACK)
        screen.blit(text, (6, TOTAL_TASKBAR_HEIGHT+10))

    def handle_click(self, pos):
        (tile_x, tile_y) = self._get_tile_from_screen_pos(pos)

        #the click doesnt click a tile
        if not (tile_x >= 0 and tile_x < self.width): return
        if not (tile_y >= 0 and tile_y < self.height): return

        # don't have plots available or already have the same tile on there
        # (prevents weird double click glitch)
        if self.available_plots == 0:
            return
        string_index = (tile_y * self.width) + tile_x
        if self.grid[string_index] == str(self.adding_image):
            return
        
        # I do not have enough numbers to represent everything in one char
        # so I swapped to base64 to fit everything
        correct_tile = BASE_64_CONV[Garden._convert_out_index_to_rotation(self.adding_image) + self.current_rotation]
        self.grid = self.grid[:string_index] + correct_tile[-1] + self.grid[string_index+1:]
        self.available_plots -= 1

        # so the DB knows to update the plot availability
        return True

    def handle_scroll(self, scroll, mouse_pos):
        # its not for the taskbar
        if mouse_pos[0] < TOTAL_TASKBAR_WIDTH:
            return

        # since height is backwards, need to subtract it
        # also multiply by 2 to make it quicker
        self.scroll_x += scroll[0] * 2
        self.scroll_y -= scroll[1] * 2
