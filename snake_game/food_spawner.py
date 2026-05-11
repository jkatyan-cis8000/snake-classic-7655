import random

from snake_game.core import Direction


class FoodSpawner:
    def spawn_food(self, grid_size, snake_body):
        while True:
            x = random.randint(0, grid_size[0] - 1)
            y = random.randint(0, grid_size[1] - 1)
            position = (x, y)
            if position not in snake_body:
                return position
