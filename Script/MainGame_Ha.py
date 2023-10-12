import pygame
import sys

# Khởi tạo Pygame
pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)
pygame.init()

# Cửa sổ game
screen = pygame.display.set_mode((432, 768))
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('assets/yellowbird-midflap.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',35)
# Hình nền màn hình bắt đầu
start_bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())

# Hình nền màn hình kết thúc
end_bg = pygame.image.load('assets/backgroundEmpty.png').convert()

#Âm thanh
click_sound = pygame.mixer.Sound('sound/sfx_click_button.wav')
hover_sound = pygame.mixer.Sound('sound/sfx_hover.wav')
ui_background_music = pygame.mixer.Sound('sound/sfx_ui.wav')
main_background_music = pygame.mixer.Sound('sound/sfx_maingame.wav')
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

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

# Trạng thái game
game_over = False

def start_screen():
    screen.blit(start_bg, (0, 0))
    
    global game_over
    game_over = False

    main_background_music.stop()
    ui_background_music.play()
    
    global current_button
    current_button = "start"
    
    global current_button_rect
    current_button_rect = start_button_rect
    
    global current_button_image
    current_button_image = start_button

    if hovered and current_button == "play":
        hover_sound.play()
        play_button_image = play_button_hover 
    else:
        play_button_image = play_button
    screen.blit(play_button_image, play_button_rect)

def end_screen():
    screen.blit(end_bg, (0, 0))
    screen.blit(score,(100,150))

    main_background_music.stop()
    ui_background_music.play()

    global game_over
    game_over = True

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

# Trạng thái hover của nút
hovered = False

# Vòng lặp xử lý game 
start_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if current_button_rect.collidepoint(pygame.mouse.get_pos()):
        hovered = True
        hover_sound.play()
    else:
        hovered = False
    
    if current_button == "start":
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
    if current_button == "end":
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
            end_screen()   #chuyển đến option 1
        elif current_button == "end":
            start_screen()
    
    pygame.display.update()
    clock.tick(120)