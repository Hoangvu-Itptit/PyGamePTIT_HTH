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
icon = pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/yellowbird-midflap.png'))
pygame.display.set_icon(icon)

# Water pipe setup
pipe_surface = pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/pipe-green.png')).convert()
pipe_manager = PipeManager(pipe_surface)
spawnPipeEvent = pygame.USEREVENT
pygame.time.set_timer(spawnPipeEvent, 1200)

# Hình nền màn hình bắt đầu
start_bg = pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/backgroundCastles.png')).convert()

clock = pygame.time.Clock()
game_font = pygame.font.Font(os.path.join(CONST.GAME_PATH, '04B_19.TTF'), 50)
font = pygame.font.Font(None, 36)


# Hiện điểm
def score_display(game_state):
    global high_score
    global score
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score if score >= 0 else 0)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        if score < 0:
            score = 0
        score_surface = game_font.render(f'Score: {int(score)}', True, (205, 133, 63))
        score_rect = score_surface.get_rect(center=(220, 177))
        screen.blit(score_surface, score_rect)

        if high_score < score:
            high_score = score
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (205, 133, 63))
        high_score_rect = high_score_surface.get_rect(center=(216, 330))
        screen.blit(high_score_surface, high_score_rect)


# Hình nền màn hình kết thúc
end_bg = pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/backgroundEmpty.png')).convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 90, 0)

# Nút Start
mode1_button_surface = pygame.transform.scale(pygame.image.load('assets/grey_button01.png').convert_alpha(),(200,50))
mode1_button_hover = pygame.transform.scale(pygame.image.load('assets/red_button01.png').convert_alpha(),(200,50))
mode1_button_rect = mode1_button_surface.get_rect(center=(216, 384))
mode1_text = font.render("Classic Mode", True, RED)
mode1_text_hover = font.render("Classic Mode", True, WHITE)
mode1_text_rect = mode1_text.get_rect(center=(216, 384))
# Nút Start2
mode2_button_surface = pygame.transform.scale(pygame.image.load('assets/grey_button01.png').convert_alpha(),(200,50))
mode2_button_hover = pygame.transform.scale(pygame.image.load('assets/red_button01.png').convert_alpha(),(200,50))
mode2_button_rect = mode2_button_surface.get_rect(center=(216, 484))
mode2_text = font.render("Special Mode", True, RED)
mode2_text_hover = font.render("Special Mode", True, WHITE)
mode2_text_rect = mode2_text.get_rect(center=(216, 484))
# Nút Quit
quit_button_surface = pygame.transform.scale(pygame.image.load('assets/quit_button.png').convert_alpha(),(200,50))
quit_button_hover = pygame.transform.scale(pygame.image.load('assets/quit_col_button.png').convert_alpha(),(200,50))
quit_button_rect = quit_button_surface.get_rect(center=(216, 534))

# Nút New Game
new_game_button_surface = pygame.transform.scale(pygame.image.load('assets/newGameButton.png').convert_alpha(),(200,50))
new_game_button_hover = pygame.transform.scale(pygame.image.load('assets/newGameColButton.png').convert_alpha(),(200,50))
new_game_button_rect = new_game_button_surface.get_rect(center=(216, 434))

# Creat Level
level = FactoryLevel.create_level(1, pipe_manager, 5)

# Tạo các biến cho trò chơi
game_over = True
gravity = 0.35
bird_movement = 0
score = 0
high_score = 0
direction = 3
floor_x_pos = 0
current_level = 2

# tạo chim
bird_down = pygame.transform.scale(
    pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/planeRed1.png')).convert_alpha(), (80, 50))
bird_mid = pygame.transform.scale(
    pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/planeRed2.png')).convert_alpha(), (80, 50))
bird_up = pygame.transform.scale(
    pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/planeRed3.png')).convert_alpha(), (80, 50))
bird_list = [bird_down, bird_mid, bird_up]  # 0 1 2
bird_index = 0
bird = bird_list[bird_index]
# bird= pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 384))

# tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# Trạng thái hover của nút
hovered = False

# Âm thanh
click_sound = pygame.mixer.Sound(os.path.join(CONST.GAME_PATH, 'sound/sfx_click_button.wav'))
hover_sound = pygame.mixer.Sound(os.path.join(CONST.GAME_PATH, 'sound/sfx_hover.wav'))
ui_background_music = pygame.mixer.Sound(os.path.join(CONST.GAME_PATH, 'sound/sfx_ui.wav'))
main_background_music = pygame.mixer.Sound(os.path.join(CONST.GAME_PATH, 'sound/sfx_maingame.wav'))
flap_sound = pygame.mixer.Sound(os.path.join(CONST.GAME_PATH, 'sound/sfx_wing.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(CONST.GAME_PATH, 'sound/sfx_hit.wav'))
score_sound = pygame.mixer.Sound(os.path.join(CONST.GAME_PATH, 'sound/sfx_point.wav'))


# Bird
def move_bird(bird):
    bird.centerx += direction
    return bird


def flip_bird():
    global direction
    direction *= -1


def check_collision(pipes):
    global direction
    global current_level
    global score
    if bird_rect.left <= 0 or bird_rect.right >= 432:
        if current_level == 2:
            score += 1
            flip_bird()
            level.set_pile_in_screen()
        else:  
            return True
    if current_level == 1:
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return True
    elif current_level == 2:
        if bird_rect.top <= -85 or bird_rect.bottom >= 750:
            return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe.pipe_rect):
            return True
    return False


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird


def bird_animation(bird):
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(bird.centerx, bird_rect.centery))
    global direction
    new_bird = pygame.transform.flip(new_bird, False if direction < 0 else True, False)
    return new_bird, new_bird_rect


def start_screen():
    screen.blit(start_bg, (0, 0))
    
    global current_button
    current_button = "start"
    
    global current_button_rect
    current_button_rect = mode1_button_rect
    
    global current_button_image
    current_button_image = mode1_button_surface

    global current_mode1_text
    current_mode1_text = mode1_text


def end_screen():
    screen.blit(end_bg, (0, 0))
    score_display("game_over")

    global current_button
    current_button = "end"
    
    global current_button_rect
    current_button_rect = new_game_button_rect
    
    global current_button_image
    current_button_image = new_game_button_surface

    if hovered and current_button == "quit":
        quit_button_image = quit_button_hover 
    else:
        quit_button_image = quit_button_surface
    screen.blit(quit_button_image, quit_button_rect)


start_screen()

main_background_music.stop()
ui_background_music.play()

# Vòng lặp xử lý game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == spawnPipeEvent:
            if level.is_create_new_pipe:
                pipe_manager.add_pipe()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over == False:
                bird_movement = 0
                flap_sound.play()
                if current_level == 1:
                    flip_bird()
                else:
                    bird_movement = -7
                flap_sound.play()

        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation(bird_rect)

    if game_over == False:
        screen.blit(start_bg, (0, 0))
        level.update(screen)

        # chim
        if current_level == 1:
            # bird_movement += gravity
            rotated_bird = rotate_bird(bird)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_over = check_collision(level.pipe_manager.pipes)
            bird_rect.centerx -= direction
            score += 0.028
            score_display('main game')
        else:
            bird_movement += gravity
            rotated_bird = rotate_bird(bird)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_over = check_collision(level.pipe_manager.pipes)
            bird_rect.centerx -= direction
            score_display('main game')
        if (game_over == True):
            end_screen()
    else:
        if current_button_rect.collidepoint(pygame.mouse.get_pos()):
            hovered = True
            hover_sound.play()
        else:
            hovered = False
        screen.blit(current_button_image, current_button_rect)
        if current_button == "start" :
            
            if hovered:
                current_button_image = mode1_button_hover
                current_mode1_text = mode1_text_hover
            else:
                current_button_image = mode1_button_surface
                current_mode1_text = mode1_text
            screen.blit(current_mode1_text, mode1_text_rect)
        
        if current_button == "start":
            if mode2_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(mode2_button_hover, mode2_button_rect)
                screen.blit(mode2_text_hover, mode2_text_rect)
                hover_sound.play()
            else:
                screen.blit(mode2_button_surface, mode2_button_rect)
                screen.blit(mode2_text, mode2_text_rect)
                
        if mode2_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                current_level = 2
                bird_rect = bird.get_rect(center=(100, 384))
                bird_movement = 0
                game_over = False
                direction = 3
                level.pipe_manager.pipes = []
                level = FactoryLevel.create_level(2, pipe_manager, 5)
                score = 0        #chuyển đến màn hình option 2 ở đây
                hover_sound.stop()
                click_sound.play()
        if current_button == "end" :
            if hovered:
                current_button_image = new_game_button_hover
            else:
                current_button_image = new_game_button_surface

        if current_button == "end":
            if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(quit_button_hover, quit_button_rect)
                hover_sound.play()
            else:
                screen.blit(quit_button_surface, quit_button_rect)
        
        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()
        
        if hovered and pygame.mouse.get_pressed()[0]:
            hover_sound.stop()
            click_sound.play()
            if current_button == "start":
                current_level = 1
                bird_rect = bird.get_rect(center=(216, 484))
                bird_movement = 0
                game_over = False
                level.pipe_manager.pipes = []
                level = FactoryLevel.create_level(1, pipe_manager, 5)
                score = -2.8
                
            elif current_button == "end":
                start_screen()

        #screen.blit(current_mode1_text, mode1_text_rect)
        # UI
        # if current_button_rect.collidepoint(pygame.mouse.get_pos()):
        #     hovered = True
        # else:
        #     hovered = False

        # if current_button == "start" :
        #     if hovered:
        #         current_mode1_text = mode1_text_hover
        #         current_button_image = mode1_button_hover
        #     else:
        #         current_button_image = mode1_button_surface
        #         current_mode1_text = mode1_text
                

        # if current_button == "start":
        #     if mode2_button_rect.collidepoint(pygame.mouse.get_pos()):
        #         current_mode2_text = mode2_text_hover
        #         screen.blit(mode2_button_hover, mode2_button_rect)
        #         screen.blit(mode2_text_hover, mode2_text_rect)
        #         hover_sound.play()
        #     else:
        #         current_mode2_text = mode2_text
        #         screen.blit(mode2_button_surface, mode2_button_rect)
        #         screen.blit(mode2_text, mode2_text_rect)

        # if current_button == "end":
        #     if hovered:
        #         current_button_image = new_game_button_hover
        #     else:
        #         current_button_image = new_game_button

        # if current_button == "end":
        #     if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
        #         screen.blit(quit_button_hover, quit_button_rect)
        #     else:
        #         screen.blit(quit_button, quit_button_rect)

        # if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
        #     if pygame.mouse.get_pressed()[0]:
        #         pygame.quit()
        #         sys.exit()

        # screen.blit(current_button_image, current_button_rect)

        # if hovered and pygame.mouse.get_pressed()[0]:
        #     if current_button == "start":
        #         current_level = 1
        #         bird_rect = bird.get_rect(center=(216, 484))
        #         bird_movement = 0
        #         game_over = False
        #         level.pipe_manager.pipes = []
        #         level = FactoryLevel.create_level(1, pipe_manager, 5)
        #         score = -1.5
        #     elif current_button == "end":
        #         start_screen()


                
        # if mode2_button_rect.collidepoint(pygame.mouse.get_pos()):
        #     if pygame.mouse.get_pressed()[0]:   
        #         current_level = 2
        #         bird_rect = bird.get_rect(center=(100, 384))
        #         bird_movement = 0
        #         game_over = False
        #         direction = 3
        #         level.pipe_manager.pipes = []
        #         level = FactoryLevel.create_level(2, pipe_manager, 5)
        #         score = 0
            

            
        # screen.blit(current_mode1_text, mode1_text_rect)
    pygame.display.update()
    clock.tick(60)
