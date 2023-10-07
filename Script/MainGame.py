import pygame
import sys
import CONST
from LevelCtl import FactoryLevel
from WaterPipe import Pipe, PipeManager
import os

# Khởi tạo Pygame
pygame.init()

# Cửa sổ game
screen = pygame.display.set_mode((432, 768))
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('assets/yellowbird-midflap.png')
pygame.display.set_icon(icon)

# Water pipe setup
pipe_surface = pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/pipe-green.png')).convert()
pipe_manager = PipeManager(pipe_surface)
spawnPipeEvent = pygame.USEREVENT
pygame.time.set_timer(spawnPipeEvent, 1200)

# Hình nền màn hình bắt đầu
start_bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())

# Hình nền màn hình kết thúc
end_bg = pygame.image.load('assets/backgroundEmpty.png').convert()

# Nút Start
start_button = pygame.transform.scale(pygame.image.load('assets/startButton.png').convert_alpha(),(200,50))
start_button_hover = pygame.transform.scale(pygame.image.load('assets/startColButton.png').convert_alpha(),(200,50))
start_button_rect = start_button.get_rect(center=(216, 384))

# Nút New Game
new_game_button = pygame.transform.scale(pygame.image.load('assets/newGameButton.png').convert_alpha(),(200,50))
new_game_button_hover = pygame.transform.scale(pygame.image.load('assets/newGameColButton.png').convert_alpha(),(200,50))
new_game_button_rect = new_game_button.get_rect(center=(216, 434))

# Nút Quit
quit_button = pygame.transform.scale(pygame.image.load('assets/quit_button.png').convert_alpha(),(200,50))
quit_button_hover = pygame.transform.scale(pygame.image.load('assets/quit_col_button.png').convert_alpha(),(200,50))
quit_button_rect = quit_button.get_rect(center=(216, 534))

score = pygame.transform.scale(pygame.image.load('assets/text_score.png').convert_alpha(),(150,50))

# Creat Level
level = FactoryLevel.create_level(1, pipe_manager, 5)


# Trạng thái game
game_over = True

def start_screen():
    screen.blit(start_bg, (0, 0))
    

    
    global current_button
    current_button = "start"
    
    global current_button_rect
    current_button_rect = start_button_rect
    
    global current_button_image
    current_button_image = start_button

def end_screen():
    screen.blit(end_bg, (0, 0))
    screen.blit(score,(100,150))


    global current_button
    current_button = "end"
    
    global current_button_rect
    current_button_rect = new_game_button_rect
    
    global current_button_image
    current_button_image = new_game_button

    if hovered and current_button == "quit":
        quit_button_image = quit_button_hover 
    else:
        quit_button_image = quit_button
    screen.blit(quit_button_image, quit_button_rect)

start_screen()

# Trạng thái hover của nút
hovered = False

# Vòng lặp xử lý game 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    
    
    if game_over == False:
        level.update(screen)
    else:
        #UI
        if current_button_rect.collidepoint(pygame.mouse.get_pos()):
            hovered = True
        else:
            hovered = False
        
        if current_button == "start" :
            if hovered:
                current_button_image = start_button_hover
            else:
                current_button_image = start_button
        
        if current_button == "end" :
            if hovered:
                current_button_image = new_game_button_hover
            else:
                current_button_image = new_game_button

        if current_button == "end":
            if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(quit_button_hover, quit_button_rect)
            else:
                screen.blit(quit_button, quit_button_rect)
        
        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()

        screen.blit(current_button_image, current_button_rect)
        
        if hovered and pygame.mouse.get_pressed()[0]:
            if current_button == "start":
                game_over = False
            elif current_button == "end":
                start_screen()

        
    pygame.display.update()
