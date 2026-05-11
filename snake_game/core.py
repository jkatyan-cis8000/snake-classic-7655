from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass
class GameState:
    snake: list[tuple[int, int]]
    direction: Direction
    food: tuple[int, int]
    score: int
    game_over: bool
    paused: bool


class DifficultyLevel(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"


@dataclass
class DifficultyConfig:
    initial_speed: int
    speed_increment: int
    grid_size: tuple[int, int]
    starting_length: int
    initial_direction: Direction = Direction.RIGHT
    initial_direction: str


class DifficultyManager:
    @staticmethod
    def get_config(level: DifficultyLevel) -> DifficultyConfig:
        configs = {
            DifficultyLevel.EASY: DifficultyConfig(
                initial_speed=200,
                speed_increment=0,
                grid_size=(20, 20),
                starting_length=3,
                initial_direction='RIGHT'
            ),
            DifficultyLevel.MEDIUM: DifficultyConfig(
                initial_speed=150,
                speed_increment=-10,
                grid_size=(25, 25),
                starting_length=3,
                initial_direction='RIGHT'
            ),
            DifficultyLevel.HARD: DifficultyConfig(
                initial_speed=100,
                speed_increment=-15,
                grid_size=(30, 30),
                starting_length=3,
                initial_direction='RIGHT'
            ),
            DifficultyLevel.EXPERT: DifficultyConfig(
                initial_speed=70,
                speed_increment=-20,
                grid_size=(35, 35),
                starting_length=2,
                initial_direction='RIGHT'
            ),
        }
        return configs[level]

    @staticmethod
    def get_available_difficulties() -> list[DifficultyLevel]:
        return list(DifficultyLevel)
