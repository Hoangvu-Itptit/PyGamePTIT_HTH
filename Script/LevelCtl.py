from Script.WaterPipe import Pipe


class FactoryLevel:
    @staticmethod
    def create_level(level_type, pipe_manager, speed):
        match level_type:
            case 1:
                return Level1(pipe_manager, speed)
            case 2:
                return Level2(pipe_manager)


class LevelCtl:
    def __init__(self, pipe_manager):
        self.pipe_manager = pipe_manager
        pass

    def update(self, screen):
        pass

    def set_pile_in_screen(self):
        pass


class Level1(LevelCtl):
    def __init__(self, pipe_manager, speed):
        super().__init__(pipe_manager)
        self.pipeSpeed = speed

    def update(self, screen):
        self.set_pile_in_screen()
        self.pipe_manager.remove_offscreen_pipes()
        self.pipe_manager.draw_pipes(screen)

    def set_pile_in_screen(self):
        for pipe in self.pipe_manager.pipes:
            self.move_pile(pipe)

    def move_pile(self, pipe: Pipe):
        pipe.y += self.pipeSpeed
        pipe.rect.x = pipe.x


class Level2(LevelCtl):
    def __init__(self, pipe_manager):
        super().__init__(pipe_manager)

    def update(self, screen):
        self.set_pile_in_screen()
        self.pipe_manager.remove_offscreen_pipes()
        self.pipe_manager.draw_pipes(screen)

    def set_pile_in_screen(self):
        pass
