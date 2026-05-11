from snake_game.core import DifficultyLevel, DifficultyManager
from snake_game.renderer import Renderer
from snake_game.game_engine import GameEngine


def display_menu():
    print("Snake Game - Select Difficulty")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Expert")
    print()


def get_user_choice():
    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if 1 <= choice <= 4:
                return choice
            print("Invalid choice. Please enter 1-4.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    display_menu()
    choice = get_user_choice()

    difficulty_map = {
        1: DifficultyLevel.EASY,
        2: DifficultyLevel.MEDIUM,
        3: DifficultyLevel.HARD,
        4: DifficultyLevel.EXPERT
    }

    difficulty = difficulty_map[choice]
    config = DifficultyManager.get_config(difficulty)

    renderer = Renderer(config.grid_size)
    game_engine = GameEngine(difficulty)
    game_engine.render = renderer

    game_engine.start()

    print(f"\nFinal Score: {game_engine.score}")


if __name__ == "__main__":
    main()
