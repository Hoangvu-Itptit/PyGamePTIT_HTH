import pygame
import sys
import CONST
from LevelCtl import FactoryLevel
from WaterPipe import Pipe, PipeManager
import os

# Khởi tạo Pygame
pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)
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

clock = pygame.time.Clock()

# Hình nền màn hình kết thúc
end_bg = pygame.image.load('assets/backgroundEmpty.png').convert()


# Nút Start
start_button = pygame.transform.scale(pygame.image.load('assets/options_button.png').convert_alpha(),(200,50))
start_button_hover = pygame.transform.scale(pygame.image.load('assets/options_col_button.png').convert_alpha(),(200,50))
start_button_rect = start_button.get_rect(center=(216, 384))

# Nút Start2
play_button = pygame.transform.scale(pygame.image.load('assets/options_button.png').convert_alpha(),(200,50))
play_button_hover = pygame.transform.scale(pygame.image.load('assets/options_col_button.png').convert_alpha(),(200,50))
play_button_rect = play_button.get_rect(center=(216, 484))

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


#Bird
def move_bird(bird):
    bird.centerx += direction
    return bird
def check_collision():
    global direction
    # for pipe in pipes:
    #     if bird_rect.colliderect(pipe):
    #         hit_sound.play()
    #         return False
    if bird_rect.left <= 0 or bird_rect.right >= 432:
            direction *= -1
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return True    
    return False 


def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
	return new_bird
def bird_animation(bird):
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (bird.centerx,bird_rect.centery))
    global direction
    new_bird = pygame.transform.flip(new_bird,False if direction < 0 else True,False)
    return new_bird, new_bird_rect


#Tạo các biến cho trò chơi
game_over = True
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0
direction = 3
floor_x_pos = 0

#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
#bird= pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))

#tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)

#Chèn âm thanh
click_sound = pygame.mixer.Sound('sound/sfx_click_button.wav')
hover_sound = pygame.mixer.Sound('sound/sfx_hover.wav')
ui_background_music = pygame.mixer.Sound('sound/sfx_ui.wav')
main_background_music = pygame.mixer.Sound('sound/sfx_maingame.wav')
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

def start_screen():
    screen.blit(start_bg, (0, 0))

    ui_background_music.play()
    
    global current_button
    current_button = "start"
    
    global current_button_rect
    current_button_rect = start_button_rect
    
    global current_button_image
    current_button_image = start_button

def end_screen():
    screen.blit(end_bg, (0, 0))
    screen.blit(score,(100,150))

    ui_background_music.play()

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
        
    
        if event.type == spawnPipeEvent:
            pipe_manager.add_pipe()
            
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over == False:
                bird_movement = 0
                bird_movement =-7
                flap_sound.play()
        
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0 
            bird, bird_rect = bird_animation(bird_rect)    
            
            
    if game_over == False:
        screen.blit(start_bg, (0, 0))
        level.update(screen)
        
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)       
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_over= check_collision()
        bird_rect.centerx -= direction
    else:
        #UI
        if current_button_rect.collidepoint(pygame.mouse.get_pos()):
            hovered = True
            hover_sound.play()
        else:
            hovered = False
        
        if current_button == "start" :
            if hovered:
                current_button_image = start_button_hover
            else:
                current_button_image = start_button

        if current_button == "start":
            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(play_button_hover, play_button_rect)
                hover_sound.play()
            else:
                screen.blit(play_button, play_button_rect)    

        if play_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                end_screen()         #chuyển đến màn hình option 2 ở đây
                hover_sound.stop()
                click_sound.play()
        
        if current_button == "end" :
            if hovered:
                current_button_image = new_game_button_hover
            else:
                current_button_image = new_game_button

        if current_button == "end":
            if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(quit_button_hover, quit_button_rect)
                hover_sound.play()
            else:
                screen.blit(quit_button, quit_button_rect)
        
        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()

        screen.blit(current_button_image, current_button_rect)
        
        if hovered and pygame.mouse.get_pressed()[0]:
            hover_sound.stop()
            click_sound.play()
            if current_button == "start":
                bird_rect = bird.get_rect(center = (100,384))
                bird_movement = 0
                game_over = False
                
            elif current_button == "end":
                start_screen()


    pygame.display.update()
    clock.tick(60)