import os


class Renderer:
    def __init__(self, grid_size):
        self.grid_size = grid_size

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self, game_state):
        self.clear()
        snake = game_state.snake
        food = game_state.food
        grid_width, grid_height = self.grid_size

        print(f"Score: {game_state.score}")
        print()

        for y in range(grid_height):
            row = ""
            for x in range(grid_width):
                if (x, y) == food:
                    row += "* "
                elif (x, y) in snake:
                    if (x, y) == snake[0]:
                        row += "X "
                    else:
                        row += "O "
                else:
                    row += ". "
            print(row)

        print()

    def show_score(self, score):
        print(f"Score: {score}")

    def show_game_over(self, score):
        self.clear()
        print("GAME OVER")
        print(f"Final Score: {score}")
        print()
