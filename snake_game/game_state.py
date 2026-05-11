from copy import deepcopy
from snake_game.core import Direction, GameState, DifficultyConfig


class GameStateManager:
    def __init__(self, config: DifficultyConfig):
        self._config = config
        self._reset_state()
    
    def _reset_state(self):
        grid_w, grid_h = self._config.grid_size
        start_len = self._config.starting_length
        
        center_x = grid_w // 2
        center_y = grid_h // 2
        
        snake = [(center_x, center_y - i) for i in range(start_len)]
        
        self._state = GameState(
            snake=snake,
            direction=Direction.UP,
            food=(0, 0),
            score=0,
            game_over=False,
            paused=False
        )
    
    def move_snake(self):
        if self._state.game_over or self._state.paused:
            return False
        
        head = self._state.snake[0]
        direction = self._state.direction
        
        dx, dy = 0, 0
        if direction == Direction.UP:
            dy = -1
        elif direction == Direction.DOWN:
            dy = 1
        elif direction == Direction.LEFT:
            dx = -1
        elif direction == Direction.RIGHT:
            dx = 1
        
        new_head = (head[0] + dx, head[1] + dy)
        
        if self._check_collision(new_head):
            self._state.game_over = True
            return False
        
        new_snake = [new_head] + self._state.snake
        
        if new_head == self._state.food:
            self._state.score += 1
        else:
            new_snake.pop()
        
        self._state.snake = new_snake
        return True
    
    def eat_food(self):
        self._state.score += 1
    
    def get_state(self):
        return deepcopy(self._state)
    
    def reset(self):
        self._reset_state()
    
    def _check_collision(self, position):
        grid_w, grid_h = self._config.grid_size
        
        x, y = position
        if x < 0 or x >= grid_w or y < 0 or y >= grid_h:
            return True
        
        # Check collision with snake body, excluding tail (which will move unless we eat)
        # If we're eating food this turn, the tail won't move so we must check entire body
        body_to_check = self._state.snake if position == self._state.food else self._state.snake[:-1]
        if position in body_to_check:
            return True
        
        return False
