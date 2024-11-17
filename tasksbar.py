import pygame
from settings import *

class Tasksbar:
    def __init__(self, saved_tasks=[]):
        self.scroll_offset = 0
        self.font = pygame.font.SysFont("Source Code Pro", 20)
        self.tasks = []
        self.selected_index = None

        for task in saved_tasks:
            self.tasks.append(Task(task[0], task[1], task[2]))

    # for now have clicking the entire thing mean you have
    # completed it
    def handle_click(self, pos):
        # the click should be handled by the garden
        if pos[0] > TASK_RECT_WIDTH:
            return
        
        clicked_task = (pos[1] + self.scroll_offset) // (TASK_RECT_HEIGHT+TASK_PADDING)
        if clicked_task >= len(self.tasks):
            return

        if self.selected_index != clicked_task:
            self.selected_index = clicked_task
            return

        if not (pos[0] > TASK_RECT_WIDTH - 20):
            return

        # have to handle if the deletion should make it scroll down
        if self.scroll_offset > 0:
            self.scroll_offset = max(self.scroll_offset - TASK_RECT_HEIGHT+TASK_PADDING, 0)


        new_plots = self.tasks[clicked_task].plots_value
        task_id = self.tasks[clicked_task].db_id
        self.selected_index = None
        del self.tasks[clicked_task]

        if (pos[1] + self.scroll_offset) % (TASK_RECT_HEIGHT+TASK_PADDING) < (TASK_RECT_HEIGHT//2):
            return (new_plots, task_id)
        return (-1, task_id)

    # handle scrolling in case we need it
    def handle_scroll(self, amount, mouse_pos):
        if mouse_pos[0] >= TOTAL_TASKBAR_WIDTH:
            return

        amount = -amount
        total_height = len(self.tasks) * (TASK_RECT_HEIGHT+TASK_PADDING)

        # not enough amount to want a scroll
        if total_height <= TOTAL_TASKBAR_HEIGHT:
            return
        
        # at the bottom going down or at the top going up
        top_of_scroll = total_height - TOTAL_TASKBAR_HEIGHT
        if (self.scroll_offset < 0 and amount < 0) or (self.scroll_offset > top_of_scroll and amount > 0):
            return

        self.scroll_offset += amount*2

    def render(self, screen):
        background_rect = pygame.Rect(0, 0, TASK_RECT_WIDTH+10, TOTAL_TASKBAR_HEIGHT)
        pygame.draw.rect(screen, (127, 127, 127), background_rect, 0, 5)

        for (i, task) in enumerate(self.tasks):
            position = (TASK_RECT_HEIGHT + TASK_PADDING) * i - self.scroll_offset + TASK_PADDING

            if i == self.selected_index:
                task.render_selected_task_block(position, screen, self.font)
                continue
            task.render_task_block(position, screen, self.font)
    
    def add_task(self, new_task, db_id):
        self.tasks.append(Task(new_task[0], new_task[1], db_id))

class Task:
    def __init__(self, name, value, db_id):
        self.name = name
        self.plots_value = value
        self.db_id = db_id
    
    # position is number of pixels from the top
    def render_task_block(self, position, screen, font):
        block = pygame.Rect(5, position, TASK_RECT_WIDTH, TASK_RECT_HEIGHT)
        text = font.render(self.name, True, COLOR_BLACK)

        pygame.draw.rect(screen, (255, 255, 255), block, 0, 2)
        screen.blit(text, (14, position + 10))

        value_text = f"number of plots: {self.plots_value}"
        text = font.render(value_text, True, SELECTED_GRAY)
        screen.blit(text, (14, position+30))

    def render_selected_task_block(self, position, screen, font):
        self.render_task_block(position, screen, font)

        button_x = (5 + TASK_RECT_WIDTH) - 20;
        
        tick_box = pygame.rect.Rect(
            button_x,
            position,
            20,
            TASK_RECT_HEIGHT//2
        )
        pygame.draw.rect(screen, (0, 255, 0), tick_box, 0, 2)

        cross_box = pygame.rect.Rect(
            button_x,
            position + TASK_RECT_HEIGHT//2,
            20,
            TASK_RECT_HEIGHT//2
        )
        pygame.draw.rect(screen, (255, 0, 0), cross_box, 0, 1)
