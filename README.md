# Space Invaders 🛸

A classic shoot 'em up game built with Python's built-in `turtle` module — no external dependencies required.

Move your ship left and right, blast the descending alien fleet, and use destructible barriers for cover before the aliens reach you.

## Features

- Player ship movement with screen boundary limits
- Shooting mechanic with fire-rate cooldown
- A full alien fleet that moves as a coordinated unit, changes direction at screen edges, and steps down after each bounce
- Bullet–alien, alien–player, and alien–barrier collision detection
- Four destructible defensive barriers, built from individually breakable segments
- Live scoreboard tracking score and current level
- Progressive difficulty — each cleared wave respawns a faster fleet
- Game over screen with a one-key restart (no need to relaunch the program)

## Why `turtle` instead of a game engine?

This project is part of a portfolio built to demonstrate range across different tools and architectures. Unlike other projects in this portfolio built with Pygame-CE, this one deliberately uses only the Python standard library. It's a good showcase of:

- Manual game-loop timing (`time.sleep()` + `screen.tracer(0)` + `screen.update()`) instead of a dedicated game clock
- Event-driven keyboard input (`onkey`) rather than per-frame key-state polling
- Building game object hierarchies on top of a general-purpose graphics module never designed for real-time games

## Controls

| Key | Action |
|---|---|
| ← / → | Move ship left / right |
| Space | Fire |
| R | Restart after Game Over |

## Tech Stack

- Python 3
- `turtle` (standard library)
- `tkinter` (standard library, used only to detect monitor resolution for window placement)

No third-party packages are required — see `requirements.txt`.

## Project Structure

```
space-invaders/
├── main.py            # Game loop, event bindings, collision orchestration
├── player.py          # Player ship class
├── alien.py           # Alien class + fleet movement logic
├── bullet.py          # Bullet class
├── barrier.py         # Destructible barrier segment class
├── scoreboard.py      # Score, level, and game-over display
├── requirements.txt
├── .gitignore
└── README.md
```

## Running the Game

```bash
python main.py
```

## Planned Improvements

This is an active project — visual and gameplay polish is still in progress. Planned next steps include:

- Custom barrier shapes (classic bunker silhouette instead of plain rectangles)
- Alien return fire
- Sound effects
- Visual redesign (sprites/colors instead of default turtle shapes)

## What I Learned

Some of the trickier bugs while building this:

- **Safe iteration while removing items**: iterating over a list copy (`list[:]`) is required whenever items get removed from that list mid-loop — otherwise Python skips elements as indices shift.
- **Two-pass fleet direction logic**: flipping the fleet's shared direction mid-iteration (as soon as one alien hits an edge) causes the fleet to desync, with some aliens moving one way and others the other way in the same frame. Direction changes must be collected first, then applied in a separate pass after every alien has moved.
- **Nearest-target collision selection**: when multiple targets can be within hit range in the same frame (e.g. two barrier rows), always resolve the *closest* one rather than the first found in a list — otherwise the result silently depends on unrelated object-creation order.
- **`turtle.Terminator` vs `tkinter.TclError`**: closing the game window while the manual game loop is running can raise either exception depending on exactly when the window is destroyed — both need to be caught for a clean exit.
