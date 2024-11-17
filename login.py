import pygame
from settings import *
from db import DBHandler

LOGIN_TEXT_X = 189
LOGIN_TEXT_Y = 30

USERNAME_BOX_X = 150
USERNAME_BOX_Y = 100
USERNAME_BOX_HEIGHT = 50
USERNAME_BOX_WIDTH = 350

PASSWORD_BOX_Y = 170

LOGIN_BUTTON_Y = 250
LOGIN_BUTTON_WIDTH = USERNAME_BOX_WIDTH // 3

SIGNUP_BUTTON_X = USERNAME_BOX_X + LOGIN_BUTTON_WIDTH*2

def login_page(screen, clock, db):
    login_font = pygame.font.SysFont("Source Code Pro", 60)
    other_font = pygame.font.SysFont("Source Code Pro", 40)

    username_selected = True
    username_inputted = ""
    password_inputted = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                value = pygame.key.name(event.key)
                letter = event.unicode
                if len(value) == 1:
                    if username_selected: username_inputted += letter
                    else: password_inputted += letter
                    continue
                
                if value == "backspace":
                    if username_selected and len(username_inputted) > 0: 
                        username_inputted = username_inputted[:-1]
                    elif not username_selected and len(password_inputted) > 0:
                        password_inputted = password_inputted[:-1]

                elif value == "tab":
                    username_selected = not username_selected
                
                elif value == "space":
                    if username_selected: username_inputted += " "
                    else: password_inputted += " "
                
                elif value == "return" and not username_selected:
                    valid = db.checkPassword(username_inputted, password_inputted)
                    if valid:
                        return username_inputted
                    
                    username_inputted = ""
                    password_inputted = ""

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                pos_x = mouse_pos[0]
                pos_y= mouse_pos[1]

                #check if it clicked username
                #check if it clicked password
                if not (pos_x > USERNAME_BOX_X and pos_y <= USERNAME_BOX_X+USERNAME_BOX_WIDTH):
                    continue
                if (pos_y > USERNAME_BOX_Y and pos_y <= USERNAME_BOX_Y + USERNAME_BOX_HEIGHT):
                    username_selected = True
                if (pos_y > PASSWORD_BOX_Y and pos_y <= PASSWORD_BOX_Y + USERNAME_BOX_HEIGHT):
                    username_selected = False

                #check if it clicked login
                #check if it clicked signup
                if (pos_y > LOGIN_BUTTON_Y and pos_y <= LOGIN_BUTTON_Y + USERNAME_BOX_HEIGHT):
                    adjust_x = pos_x - USERNAME_BOX_X
                    fraction = adjust_x // LOGIN_BUTTON_WIDTH

                    if fraction == 0: 
                        # this is a login attemp
                        valid = db.checkPassword(username_inputted, password_inputted)
                        if valid:
                            return username_inputted
                        
                    elif fraction == 2: 
                        # this is a signup attempt
                        db.createUser(username_inputted, password_inputted)
                        return username_inputted
                    else:
                        continue

                    username_inputted = ""
                    password_inputted = ""


        # the rendering 
        screen.fill((200, 200, 200))

        # the login text
        text = login_font.render("Please Log in", True, COLOR_BLACK)
        screen.blit(text, (LOGIN_TEXT_X, LOGIN_TEXT_Y))  

        if username_selected:
            username_block_color = SELECTED_GRAY
            password_block_color = (255, 255, 255)
        else:
            username_block_color = (255, 255, 255)
            password_block_color = SELECTED_GRAY

        #the username box
        username_block = pygame.rect.Rect(
            USERNAME_BOX_X,
            USERNAME_BOX_Y,
            USERNAME_BOX_WIDTH,
            USERNAME_BOX_HEIGHT
        )
        pygame.draw.rect(screen, username_block_color, username_block, 0, 5)
        text = other_font.render(username_inputted, True, COLOR_BLACK)
        adjusted_x = USERNAME_BOX_X - max(text.get_width() - USERNAME_BOX_WIDTH + 10, 0)
        screen.blit(text, (adjusted_x + 5, USERNAME_BOX_Y+10))

        #the password box
        password_block = pygame.rect.Rect(
            USERNAME_BOX_X,
            PASSWORD_BOX_Y,
            USERNAME_BOX_WIDTH,
            USERNAME_BOX_HEIGHT
        )
        pygame.draw.rect(screen, password_block_color, password_block, 0, 5)
        text = other_font.render("*" * len(password_inputted), True, COLOR_BLACK)
        adjusted_x = USERNAME_BOX_X - max(text.get_width() - USERNAME_BOX_WIDTH + 10, 0)
        screen.blit(text, (adjusted_x + 5, PASSWORD_BOX_Y + 10))

        #the login button
        login_button = pygame.rect.Rect(
            USERNAME_BOX_X,
            LOGIN_BUTTON_Y,
            LOGIN_BUTTON_WIDTH,
            USERNAME_BOX_HEIGHT
        )
        pygame.draw.rect(screen, (255, 255, 255), login_button, 0, 5)
        text = other_font.render("login", True, COLOR_BLACK)
        screen.blit(text, (USERNAME_BOX_X+10, LOGIN_BUTTON_Y+10))

        #the login button
        signup_button = pygame.rect.Rect(
            SIGNUP_BUTTON_X,
            LOGIN_BUTTON_Y,
            LOGIN_BUTTON_WIDTH,
            USERNAME_BOX_HEIGHT
        )
        pygame.draw.rect(screen, (255, 255, 255), signup_button, 0, 5)
        text = other_font.render("sign up", True, COLOR_BLACK)
        screen.blit(text, (SIGNUP_BUTTON_X+10, LOGIN_BUTTON_Y+10))

        # add a block to the front for the scrolling of username/password
        # It was the first solution I could think of
        left_block = pygame.rect.Rect(
            0,
            0,
            USERNAME_BOX_X,
            SCREEN_HEIGHT
        )
        # give it same color as background so it matches
        pygame.draw.rect(screen, (200, 200, 200), left_block)

        pygame.display.update()
        clock.tick(60)