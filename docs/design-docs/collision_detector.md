# Collision Detector Design Doc

## Overview
The `CollisionDetector` module handles detection of all collision types in the Snake game: boundary collisions, self-collisions, and food collisions.

## Implementation Details

### CollisionDetector Class
**Location:** `snake_game/collision_detector.py`

#### Methods

##### `check_boundary_collision(snake_head, grid_size)`
**Purpose:** Determine if the snake head is out of bounds

**Parameters:**
- `snake_head`: Tuple (x, y) representing the head position
- `grid_size`: Tuple (width, height) representing the game grid dimensions

**Returns:** `True` if head is out of bounds, `False` otherwise

**Algorithm:**
1. Extract x and y coordinates from snake_head
2. Check if x < 0 or x >= grid_size[0] (left or right boundary)
3. Check if y < 0 or y >= grid_size[1] (top or bottom boundary)
4. Return `True` if any boundary check fails

##### `check_self_collision(snake)`
**Purpose:** Determine if the snake head overlaps with any body segment

**Parameters:**
- `snake`: List of (x, y) tuples representing the entire snake (head at index 0)

**Returns:** `True` if head overlaps with body, `False` otherwise

**Algorithm:**
1. Extract head position (first element of snake list)
2. Extract body segments (all elements except the head)
3. Check if head position exists in body segment list
4. Return `True` if overlap found

##### `check_food_collision(snake_head, food)`
**Purpose:** Determine if the snake head is at the same position as food

**Parameters:**
- `snake_head`: Tuple (x, y) representing the head position
- `food`: Tuple (x, y) representing the food position

**Returns:** `True` if head position matches food position, `False` otherwise

**Algorithm:**
1. Compare snake_head and food tuples for equality
2. Return `True` if they match

## Module Interactions
- Receives `GameState` snapshot from `GameEngine`
- Returns collision results to `GameEngine`
- Does not modify state directly
- Uses only basic types (tuples, lists) and imports from `snake_game.core` for `Direction` (not used in current implementation but available for future use)

## Design Decisions
- All methods are stateless and take explicit parameters for clarity
- Returns boolean values for easy integration with conditional logic
- Boundary checks include zero and exclusive upper bound for standard grid indexing
- Self-collision excludes the head from comparison with itself (compares head against body only)
