import pygame, sys, random
#Tạo hàm cho trò chơi
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
            return False
    return True 


def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
	return new_bird
def bird_animation(bird):
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (bird.centerx,bird_rect.centery))
    global direction
    new_bird = pygame.transform.flip(new_bird,False if direction < 0 else True,False)
    return new_bird, new_bird_rect


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',35)


#Tạo các biến cho trò chơi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
direction = 3
floor_x_pos = 0
 
#chèn background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)


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
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
#while loop của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement =-7
                flap_sound.play()
        
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0 
            bird, bird_rect = bird_animation(bird_rect)    
       
    screen.blit(bg,(0,0))       
    if game_active:
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)       
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active= check_collision()
        bird_rect.centerx -= direction
     
    
    pygame.display.update()
    clock.tick(100)
