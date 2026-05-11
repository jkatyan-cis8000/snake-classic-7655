from snake_game.core import Direction


class CollisionDetector:
    def check_boundary_collision(self, snake_head, grid_size):
        x, y = snake_head
        if x < 0 or x >= grid_size[0]:
            return True
        if y < 0 or y >= grid_size[1]:
            return True
        return False

    def check_self_collision(self, snake):
        head = snake[0]
        body = snake[1:]
        return head in body

    def check_food_collision(self, snake_head, food):
        return snake_head == food
