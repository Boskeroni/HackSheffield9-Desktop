import pygame
import garden as gd
import tasksbar
import add_tasks as at
from select_tile import TileSelector
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font()
running = True

# sets up the login page
# returns the username (email of the valid sign in attempt)
import login
from db import DBHandler

db_handler = DBHandler()
user_email = login.login_page(screen, clock, db_handler)

garden_data = db_handler.getLayout(user_email)
garden_layout = garden_data["layout"]
garden_height = garden_data["height"]
garden_width = garden_data["width"]
available_plots = db_handler.getAvailablePlots(user_email)

# The time to update my version of tasks with DB's version
pygame.time.set_timer(pygame.USEREVENT, 10000)

tile_selector = TileSelector()
garden = gd.Garden(garden_height, garden_width, garden_layout, available_plots)
taskbar = tasksbar.Tasksbar(db_handler.getTasks(user_email))
add_tasks = at.AddTasks()

while running:
    screen.fill((0, 120, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # updating the tasks from db
        if event.type == pygame.USEREVENT:
            db_tasks = db_handler.getTasks(user_email)
            taskbar = tasksbar.Tasksbar(db_tasks)
                            

        # check for mouse clicks
        if add_tasks.is_adding_task:
            if event.type == pygame.KEYDOWN:
                # I only really want numbers and characters
                letter = pygame.key.name(event.key)
                if not letter.isalnum():
                    continue
                
                possible_task = add_tasks.handle_text_input(letter)
                if possible_task is not None:
                    db_id = db_handler.createTask(possible_task[0], user_email, possible_task[1])
                    taskbar.add_task(possible_task, db_id)
                    continue

            has_clicked = pygame.mouse.get_pressed()[0]
            if has_clicked:
                add_tasks.handle_click(pygame.mouse.get_pos())
            continue

        if event.type == pygame.KEYDOWN:
            letter = pygame.key.name(event.key)
            possible_rotate = tile_selector.handle_text_input(letter)
            if possible_rotate is not None:
                garden.rotate_selected()
                pass

        has_clicked = pygame.mouse.get_pressed()[0]
        if has_clicked:
            pos = pygame.mouse.get_pos()

            possible_tile_change = tile_selector.handle_click(pos)
            if possible_tile_change is not None:
                garden.change_tile(possible_tile_change)
                continue

            possible_data = taskbar.handle_click(pos)
            if possible_data is not None:
                (possible_plots, task_id) = possible_data
                if possible_plots != -1:
                    garden.available_plots += possible_plots
                db_handler.updateAvailablePlots(user_email, garden.available_plots)
                db_handler.deleteSpecificTask(task_id)
                continue

            # prevents pressing the button from changing the mode
            mode_change = add_tasks.handle_click(pos)
            if mode_change:
                continue
            
            plot_added = garden.handle_click(pos)
            if plot_added is not None:
                db_handler.updateAvailablePlots(user_email, garden.available_plots)

        
        if event.type == pygame.MOUSEWHEEL:
            pos = pygame.mouse.get_pos()

            taskbar.handle_scroll(event.y, pos)
            garden.handle_scroll((event.x, event.y), pos)

    garden.render_garden(screen, pygame.mouse.get_pos(), add_tasks.is_adding_task)
    taskbar.render(screen)

    #I want this to have priority over everything else so it is at the bottom
    add_tasks.render(screen)
    tile_selector.render(screen)
    garden.render_info(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# update all the database stuff
db_handler.updateLayout(user_email, garden.grid)