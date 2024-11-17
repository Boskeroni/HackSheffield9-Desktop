import pygame
import pygame.freetype
from settings import *

class AddTasks():
    def __init__(self):
        self.plus_font = pygame.font.SysFont("Source Code Pro", 90)
        self.text_font = pygame.font.SysFont("Source Code Pro", 30)

        self.max_task_name = 30
        self.is_adding_task = False
        self.new_task_text = ""
        self.new_task_diff = ""
        self.selected_text = True

    def render(self, screen):
        if self.is_adding_task: self.render_task_input(screen)
        else: self.render_add_button(screen)

    def render_add_button(self, screen):
        add_button = pygame.rect.Rect(
            ADD_BUTTON_LOCATION_X, 
            ADD_BUTTON_LOCATION_Y, 
            ADD_BUTTON_SIZE, 
            ADD_BUTTON_SIZE
        )
        pygame.draw.rect(screen, ADD_BUTTON_BG_COLOR, add_button, 0, 8)

        text = self.plus_font.render("+", True, ADD_BUTTON_TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH - 53, SCREEN_HEIGHT - 70))

    def render_task_input(self, screen):
        if self.selected_text:
            text_color = (127, 127, 127)
            diff_color = (255, 255, 255)
        else:
            text_color = (255, 255, 255)
            diff_color = (127, 127, 127)

        text_block = pygame.rect.Rect(
            TOTAL_TASKBAR_WIDTH+3, 
            3, 
            ADD_TASK_TEXT_LENGTH, 
            ADD_TASK_HEIGHT
        )
        pygame.draw.rect(screen, text_color, text_block, 0, 5)
        text = self.text_font.render(self.new_task_text, True, COLOR_BLACK)
        screen.blit(text, (TOTAL_TASKBAR_WIDTH+6, 10))

        difficulty_block = pygame.rect.Rect(
            TOTAL_TASKBAR_WIDTH+ADD_TASK_TEXT_LENGTH + 6,
            3,
            ADD_TASK_PRIORITY_LENGTH,
            ADD_TASK_HEIGHT
        )
        pygame.draw.rect(screen, diff_color, difficulty_block, 0, 5)
        text = self.text_font.render(self.new_task_diff, True, COLOR_BLACK)
        screen.blit(text, (TOTAL_TASKBAR_WIDTH+ADD_TASK_TEXT_LENGTH+9, 10))
        

    def handle_click(self, pos):
        # this will instead now check for which input text we will add to
        if self.is_adding_task:
            loc_x = pos[0] - TOTAL_TASKBAR_WIDTH
            loc_y = pos[1]

            if loc_x < 0: return
            if loc_y > ADD_TASK_HEIGHT: return

            self.selected_text = loc_x < ADD_TASK_TEXT_LENGTH
            return

        loc_x = pos[0] - ADD_BUTTON_LOCATION_X
        loc_y = pos[1] - ADD_BUTTON_LOCATION_Y
        if not (loc_x > 0 and loc_x < ADD_BUTTON_SIZE):
            return
        if not (loc_y > 0 and loc_y < ADD_BUTTON_SIZE):
            return

        self.is_adding_task = True
        self.selected_text = True
        # signifies a mode change
        return True

    def handle_text_input(self, letter):
        if not self.is_adding_task:
            return
        
        # this updates the second block of text
        if not self.selected_text:
            if letter.isnumeric() and len(self.new_task_diff) < 2:
                self.new_task_diff += letter
                return
            elif letter == "backspace":
                if len(self.new_task_diff) != 0:
                    self.new_task_diff = self.new_task_diff[:-1]
        else:
            if len(letter) == 1 and len(self.new_task_text) < self.max_task_name:
                self.new_task_text += letter
                return
            elif letter == "space":
                self.new_task_text += " "
            elif letter == "backspace": 
                if len(self.new_task_text) != 0:
                    self.new_task_text = self.new_task_text[:-1]

        if letter == "escape":
            self.is_adding_task = False
            self.new_task_text = ""
            self.new_task_diff = ""

        elif letter == "return":
            if len(self.new_task_diff) == 0:
                return
            
            returned_text = self.new_task_text
            returned_diff = self.new_task_diff

            self.new_task_text = ""
            self.new_task_diff = ""
            self.is_adding_task = False

            return (returned_text, int(returned_diff))

        elif letter == "tab":
            self.selected_text = not self.selected_text

 
        