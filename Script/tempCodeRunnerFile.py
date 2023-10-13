bird_rect = bird.get_rect(center=(100, 384))
                bird_movement = 0
                game_over = False
                direction = 3
                level.pipe_manager.pipes = []
                level = FactoryLevel.create_level(2, pipe_manager, 5)
                score = 0        #chuyển đến màn hình option 2 ở đây