# Snake Game Architecture

## Overview

This document describes the architecture of the classic Snake game, designed with clean separation of concerns, modularity, and extensibility in mind.

## Core Modules

### 1. Game Engine (`game_engine.py`)

**Responsibilities:**
- Main game loop orchestration
- Game state management (running, paused, over)
- Loop timing and frame rate control
- Coordination between input, logic, and rendering modules

**Classes/Interfaces:**
- `GameEngine`: Main orchestrator with `start()`, `stop()`, `pause()`, `resume()` methods
- `GameLoop`: Handles the timing and execution of game updates

**Interactions:**
- Receives input from `InputHandler`
- Updates game state via `GameStateManager`
- Calls `Renderer` to draw frames
- Monitors `CollisionDetector` for game-over conditions

---

### 2. Game State Manager (`game_state.py`)

**Responsibilities:**
- Store and manage game state (snake position, food, score, direction)
- Provide state snapshots for rendering
- Handle state transitions (eat food, move snake)

**Classes/Interfaces:**
- `GameState`: Data class holding all mutable game data
  - `snake`: List of coordinate tuples representing snake body
  - `direction`: Current movement direction (UP, DOWN, LEFT, RIGHT)
  - `food`: Coordinate of current food position
  - `score`: Current score value
  - `game_over`: Boolean indicating game status
  - `paused`: Boolean indicating pause status
- `GameStateManager`: Manages state and provides state-modifying methods

**Data Flow:**
- Input module reads direction changes from `GameState`
- Collision detector reads snake position and direction
- Renderer reads entire `GameState` for rendering

---

### 3. Input Handler (`input_handler.py`)

**Responsibilities:**
- Capture user input (keyboard events)
- Translate input into direction changes
- Handle pause/start/quit commands
- Prevent contradictory direction changes (e.g., immediate 180° turn)

**Classes/Interfaces:**
- `InputHandler`: Processes input events with methods:
  - `handle_input(event)`: Process input event and update game state
  - `get_next_direction()`: Return requested direction change
- `Direction` enum: UP, DOWN, LEFT, RIGHT

**Interactions:**
- Reads current direction from `GameState`
- Updates `GameState` with new direction
- Communicates with `GameEngine` for game control commands

---

### 4. Collision Detector (`collision_detector.py`)

**Responsibilities:**
- Detect collisions with boundaries
- Detect collisions with self
- Detect food consumption
- Report game-over conditions

**Classes/Interfaces:**
- `CollisionDetector`: Core collision detection logic
  - `check_boundary_collision(snake_head, grid_size)`: Returns True if out of bounds
  - `check_self_collision(snake)`: Returns True if head overlaps body
  - `check_food_collision(snake_head, food)`: Returns True if eating food

**Interactions:**
- Receives `GameState` snapshot from `GameEngine`
- Returns collision results to `GameEngine`
- Does not modify state directly

---

### 5. Food Spawner (`food_spawner.py`)

**Responsibilities:**
- Generate food at random valid positions
- Ensure food doesn't spawn on snake body
- Support configurable spawn area

**Classes/Interfaces:**
- `FoodSpawner`: Handles food generation
  - `spawn_food(grid_size, snake_body)`: Returns valid food coordinate
  - `set_spawn_area(x_range, y_range)`: Configure spawn boundaries

**Interactions:**
- Called by `GameEngine` after food consumption
- Receives `GameState` to avoid spawning on snake

---

### 6. Renderer (`renderer.py`)

**Responsibilities:**
- Render game state to display
- Draw snake, food, score, game-over screen
- Handle display updates

**Classes/Interfaces:**
- `Renderer`: Rendering interface
  - `render(game_state)`: Draw current game state
  - `show_game_over(score)`: Display game-over screen
  - `show_score(score)`: Update score display
  - `clear()`: Clear screen for next frame

**Interactions:**
- Receives `GameState` from `GameEngine`
- No state modification, read-only access

---

### 7. Difficulty Config (`difficulty.py`)

**Responsibilities:**
- Define difficulty levels and their parameters
- Provide configuration lookup by difficulty
- Enable easy addition of new difficulty levels

**Classes/Interfaces:**
- `DifficultyLevel` enum: EASY, MEDIUM, HARD, EXPERT
- `DifficultyConfig`: Data class with:
  - `initial_speed`: Starting game speed (ms per frame)
  - `speed_increment`: Speed increase per food eaten
  - `grid_size`: Game board dimensions (width, height)
  - `starting_length`: Initial snake length
- `DifficultyManager`: Configuration manager with methods:
  - `get_config(difficulty)`: Returns configuration for level
  - `get_available_difficulties()`: List all difficulty levels

**Configuration Approach:**
- Centralized configuration file/lookup
- Difficulty levels defined as constant configurations
- Easy to add new levels by adding to configuration
- Passed to `GameEngine` on initialization

---

## Module Interactions Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Game Engine                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Orchestrates: Loop, State, Input, Render, Collision   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
         ▼         ▼         ▼
┌─────────────┐ ┌──────────┐ ┌──────────────┐
│  Game State │ │  Input   │ │ Collision    │
│  Manager    │ │ Handler  │ │ Detector     │
│             │ │          │ │              │
│ - snake     │ │ - read   │ │ - snake      │
│ - direction │ │ - update │ │ - food       │
│ - food      │ │ direction│ │ - boundary   │
│ - score     │ │ - commands││ - collision  │
│ - game_over │ │          │ │ - report     │
└──────┬──────┘ └──────────┘ └──────┬───────┘
       │                            │
       │        ┌──────────┐        │
       └───────▶│ Food     │◀───────┘
                │ Spawner  │
                │          │
                │ - spawn  │
                │ food     │
                └──────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Renderer    │
                  │              │
                  │ - draw game  │
                  │ - show score │
                  │ - game over  │
                  └──────────────┘
                         ▲
                         │
                  ┌──────────────┐
                  │ Difficulty   │
                  │ Config       │
                  │              │
                  │ - levels     │
                  │ - settings   │
                  └──────────────┘
```

## Data Flow

1. **Initialization:**
   - `DifficultyManager` provides `DifficultyConfig` to `GameEngine`
   - `GameEngine` initializes `GameStateManager` with starting state
   - `FoodSpawner` creates initial food position

2. **Game Loop (each frame):**
   - `InputHandler` processes input → updates `GameState.direction`
   - `GameEngine` calls `GameStateManager.move_snake()` → updates state
   - `CollisionDetector` checks collisions → returns results to `GameEngine`
   - If food eaten: `FoodSpawner` generates new food
   - `Renderer` draws current `GameState`

3. **Input Flow:**
   - User input → `InputHandler` → validate → update `GameState.direction`

4. **Collision Flow:**
   - `GameEngine` reads `GameState` → `CollisionDetector` checks conditions → return collision type → `GameEngine` handles (game over or score update)

## Configuration Flow

```
DifficultyLevel (EASY/MEDIUM/HARD/EXPERT)
    ↓
DifficultyManager.get_config()
    ↓
DifficultyConfig (speed, grid_size, starting_length)
    ↓
GameEngine initialization
    ↓
GameStateManager configured with starting state
    ↓
Game begins
```

## Extensibility Points

- **New difficulty levels**: Add to `DifficultyConfig` lookup
- **New input methods**: Implement new `InputHandler` variant
- **New rendering systems**: Implement `Renderer` interface (console, GUI, web)
- **New game modes**: Extend `GameState` and `CollisionDetector`
