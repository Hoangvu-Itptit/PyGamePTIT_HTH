import random

import CONST
from WaterPipe import Pipe


class FactoryLevel:
    @staticmethod
    def create_level(level_type, pipe_manager, speed):
        match level_type:
            case 1:
                return Level1(pipe_manager, speed)
            case 2:
                return Level2(pipe_manager)


class LevelCtl:
    def __init__(self, pipe_manager, is_create_new_pipe):
        self.pipe_manager = pipe_manager
        self.is_create_new_pipe = is_create_new_pipe
        pass

    def update(self, screen):
        pass

    def set_pile_in_screen(self):
        pass


class Level1(LevelCtl):
    def __init__(self, pipe_manager, speed):
        super().__init__(pipe_manager, True)
        self.pipeSpeed = speed

    def update(self, screen):
        self.set_pile_in_screen()
        self.pipe_manager.remove_offscreen_pipes()
        self.pipe_manager.draw_pipes(screen, self.pipe_manager.pipes)

    def set_pile_in_screen(self):
        for pipe in self.pipe_manager.pipes:
            self.move_pile(pipe)

    def move_pile(self, pipe: Pipe):
        pipe.y += self.pipeSpeed
        pipe.pipe_rect.centery += self.pipeSpeed


class Level2(LevelCtl):
    def __init__(self, pipe_manager):
        super().__init__(pipe_manager, False)
        for i in range(5):
            new_pipe = Pipe(-100, 100 + i * 200, pipe_manager.pipe_image, -90)
            new_pipe.x = -(new_pipe.height - 50)
            new_pipe.pipe_rect.centerx = -(new_pipe.height - 50)
            self.pipe_manager.pipes.append(new_pipe)
        self.pipe_item = 0
        self.set_pile_in_screen()

    def update(self, screen):
        self.pipe_manager.draw_pipes(screen, self.pipe_manager.pipes)

    def set_pile_in_screen(self):
        self.pipe_manager.pipes = self.instance_pipe_left() if self.pipe_item == 0 else self.instance_pipe_right()
        self.pipe_item = 1 if self.pipe_item == 0 else 0
        pass

    def instance_pipe_left(self) -> []:
        posY = [i * 100 for i in range(1, 10)]
        kq = []
        for i in range(5):
            y = random.choice(posY)
            posY.remove(y)
            new_pipe = Pipe(CONST.WIDTH - 50, y, self.pipe_manager.pipe_image, 90)
            kq.append(new_pipe)
        return kq

    def instance_pipe_right(self) -> []:
        posX = [i * 100 for i in range(1, 10)]
        kq = []
        for i in range(5):
            x = random.choice(posX)
            posX.remove(x)
            new_pipe = Pipe(-100, 100 + i * 200, self.pipe_manager.pipe_image, -90)
            new_pipe.x = -(new_pipe.height - 50)
            new_pipe.pipe_rect.centerx = -(new_pipe.height - 50)
            kq.append(new_pipe)
        return kq
