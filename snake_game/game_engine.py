import time
import threading
from snake_game.core import DifficultyLevel, DifficultyManager, Direction


class GameEngine:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.config = DifficultyManager.get_config(difficulty)
        self.snake = []
        self.direction = None
        self.food = None
        self.score = 0
        self.game_over = False
        self.paused = False
        self.running = False
        self.render = None
        self.input_handler = None

    def start(self):
        self.running = True
        self._initialize_game()
        self._game_loop()

    def stop(self):
        self.running = False
        self.game_over = True

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def _initialize_game(self):
        grid_width, grid_height = self.config.grid_size
        start_x = grid_width // 2
        start_y = grid_height // 2
        self.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = self.config.initial_direction
        self.food = self._spawn_food()
        self.score = 0
        self.game_over = False
        self.paused = False

    def _spawn_food(self):
        grid_width, grid_height = self.config.grid_size
        while True:
            import random
            food = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
            if food not in self.snake:
                return food

    def _handle_input(self):
        if self.input_handler:
            new_direction = self.input_handler.get_direction()
            if new_direction:
                self.direction = new_direction

    def _update_state(self):
        head_x, head_y = self.snake[0]
        if self.direction == Direction.UP:
            head_y -= 1
        elif self.direction == Direction.DOWN:
            head_y += 1
        elif self.direction == Direction.LEFT:
            head_x -= 1
        elif self.direction == Direction.RIGHT:
            head_x += 1

        new_head = (head_x, head_y)

        if self._check_collision(new_head):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self._spawn_food()
        else:
            self.snake.pop()

    def _check_collision(self, position):
        grid_width, grid_height = self.config.grid_size
        x, y = position

        if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
            return True

        if position in self.snake[1:]:
            return True

        return False

    def _render(self):
        if self.render:
            from snake_game.core import GameState, Direction
            gs = GameState(
                snake=self.snake,
                direction=Direction[self.direction],
                food=self.food,
                score=self.score,
                game_over=self.game_over,
                paused=self.paused
            )
            self.render.render(gs)

    def _game_loop(self):
        speed = self.config.initial_speed

        while self.running and not self.game_over:
            if not self.paused:
                self._handle_input()
                self._update_state()
                self._render()

                if self.config.speed_increment:
                    speed = max(50, speed + self.config.speed_increment)

                time.sleep(speed / 1000.0)
            else:
                time.sleep(0.1)

        if self.render:
            self.render.show_game_over(self.score)
