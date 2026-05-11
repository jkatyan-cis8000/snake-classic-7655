# Food Spawner Design Doc

## Overview
The `FoodSpawner` module handles the generation of food at random valid positions on the game grid.

## Implementation Details

### FoodSpawner Class
**Location:** `snake_game/food_spawner.py`

**Method:** `spawn_food(grid_size, snake_body)`

**Parameters:**
- `grid_size`: Tuple (width, height) representing the game grid dimensions
- `snake_body`: List of (x, y) tuples representing current snake positions

**Returns:** Valid (x, y) tuple position for food

**Algorithm:**
1. Generate random x and y coordinates within grid bounds (0 to grid_size - 1)
2. Check if the generated position overlaps with any snake body segment
3. If position is valid (not on snake), return it
4. If position is invalid (on snake), repeat the process

**Constraints:**
- Valid position must be within grid bounds
- Valid position must not overlap with snake body
- Uses `random.randint()` for spawning
- Infinite loop protection is implicit (snake cannot occupy all grid positions in a playable game)

## Module Interactions
- Called by `GameEngine` after food consumption
- Receives `GameState` to avoid spawning on snake
- Does not modify game state directly
- Only reads from `snake_body` to determine valid positions
