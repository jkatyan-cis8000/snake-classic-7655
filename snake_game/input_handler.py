from enum import Enum
from snake_game.core import Direction


class InputHandler:
    def __init__(self):
        self._direction = Direction.UP
        self._paused = False
        self._quit = False

    def handle_input(self, event):
        direction_map = {
            'up': Direction.UP,
            'down': Direction.DOWN,
            'left': Direction.LEFT,
            'right': Direction.RIGHT
        }
        
        if event in direction_map:
            new_direction = direction_map[event]
            if self._cannot_reverse(new_direction):
                return None
            self._direction = new_direction
            return self._direction
        
        return None

    def get_direction(self):
        return self._direction

    def handle_command(self, cmd):
        if cmd == 'pause':
            self._paused = not self._paused
            return 'pause'
        elif cmd == 'quit':
            self._quit = True
            return 'quit'
        elif cmd == 'start':
            self._paused = False
            return 'start'
        return None

    def _cannot_reverse(self, new_direction):
        reverse_map = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return reverse_map.get(new_direction) == self._direction
