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

clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',50)

# Hiện điểm
def score_display(game_state):
    global high_score
    global score
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score if score >=0 else 0)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(205,133,63))
        score_rect = score_surface.get_rect(center = (220,177))
        screen.blit(score_surface,score_rect)

        if high_score < score:
            high_score = score
        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(205,133,63))
        high_score_rect = high_score_surface.get_rect(center = (216,330))
        screen.blit(high_score_surface,high_score_rect)


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


# Creat Level
level = FactoryLevel.create_level(1, pipe_manager, 5)


#Bird
def move_bird(bird):
    bird.centerx += direction
    return bird

def flip_bird():
    global direction
    direction *= -1 

def check_collision(pipes):
    global direction
    global current_level
    if bird_rect.left <= 0 or bird_rect.right >= 432:
            if current_level == 2:
                flip_bird()
            else:
                return True
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return True    
    for pipe in pipes:
        if bird_rect.colliderect(pipe.pipe_rect):
            print("Hit")
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
current_level = 1

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
    score_display("game_over")


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


#Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

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
                if current_level == 1:
                    flip_bird() 
                else:
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
        if current_level == 1:
            #bird_movement += gravity
            rotated_bird = rotate_bird(bird)       
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird,bird_rect)
            game_over= check_collision(level.pipe_manager.pipes)
            bird_rect.centerx -= direction
            score += 0.02
            score_display('main game')
        else:
            bird_movement += gravity
            rotated_bird = rotate_bird(bird)       
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird,bird_rect)
            game_over= check_collision(level.pipe_manager.pipes)
            bird_rect.centerx -= direction
            score += 0.01
        if (game_over == True):
            end_screen()
    else:
        #UI
        if current_button_rect.collidepoint(pygame.mouse.get_pos()):
            hovered = True
        else:
            hovered = False
        
        if current_button == "start":
            if hovered:
                current_button_image = start_button_hover
            else:
                current_button_image = start_button
        
        if current_button == "end":
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
                if current_level == 1:
                    bird_rect = bird.get_rect(center = (216,484))
                    bird_movement = 0
                    game_over = False
                    level.pipe_manager.pipes = []
                    level = FactoryLevel.create_level(1, pipe_manager, 5)
                    score = -1.5
                else:
                    bird_rect = bird.get_rect(center = (100,384))
                    bird_movement = 0
                    game_over = False
                    level.pipe_manager.pipes = []
                    level = FactoryLevel.create_level(2, pipe_manager, 5)
               
                
            elif current_button == "end":
                start_screen()

        
    pygame.display.update()
    clock.tick(60)