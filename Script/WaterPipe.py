import pygame
import random
from CONST import WIDTH, HEIGHT


class Pipe:
    def __init__(self, x, y, image, angle):
        self.x = x
        self.y = y
        self.image = image
        self.image = pygame.transform.rotate(self.image, angle)
        self.width = image.get_width()
        self.height = image.get_height()
        self.pipe_rect = self.image.get_rect(topleft = (self.x,self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class PipeManager:
    def __init__(self, pipe_image):
        self.pipe_image = pipe_image
        self.pipes = []

    def add_pipe(self):
        x = random.choice([-50, -100, -150, -200])
        y = 0
        speed = 5
        new_pipe = Pipe(x, y, self.pipe_image, -90)
        self.pipes.append(new_pipe)
        y = -150
        x = random.choice([WIDTH - 50, WIDTH - 100, WIDTH - 150, WIDTH - 200])
        new_pipe = Pipe(x, y, self.pipe_image, 90)
        self.pipes.append(new_pipe)

    # def move_pipes(self):
    #     for pipe in self.pipes:
    #         pipe.move()

    def remove_offscreen_pipes(self):
        self.pipes = [pipe for pipe in self.pipes if pipe.y < HEIGHT]

    def draw_pipes(self, screen, list_pipe):
        for pipe in list_pipe:
            pipe.draw(screen)
