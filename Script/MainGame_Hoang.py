import os
import pygame
import sys
import CONST
from Script.LevelCtl import FactoryLevel
from WaterPipe import Pipe, PipeManager

pygame.init()

# Screen setup
screen = pygame.display.set_mode((CONST.WIDTH, CONST.HEIGHT))

# Clock setup
clock = pygame.time.Clock()

# Background setup
bg = pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/background-night.png')).convert()
bg = pygame.transform.scale(bg, (CONST.WIDTH, CONST.HEIGHT))

# Floor setup
floor = pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/floor.png')).convert()
floor = pygame.transform.scale(floor, (CONST.WIDTH, 100))

# Water pipe setup
pipe_surface = pygame.image.load(os.path.join(CONST.GAME_PATH, 'assets/pipe-green.png')).convert()
pipe_manager = PipeManager(pipe_surface)
spawnPipeEvent = pygame.USEREVENT
pygame.time.set_timer(spawnPipeEvent, 1200)

# Creat Level
level = FactoryLevel.create_level(1, pipe_manager, 5)


def DrawObject(obj, desk):
    screen.blit(obj, desk)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == spawnPipeEvent:
            pipe_manager.add_pipe()

    DrawObject(bg, (0, 0))
    level.update(screen)
    DrawObject(floor, (0, CONST.HEIGHT - 100))

    pygame.display.update()
    clock.tick(CONST.FPS)
