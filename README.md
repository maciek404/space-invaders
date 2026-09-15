# Space Invaders 🛸

A classic shoot 'em up game built with Python's built-in `turtle` module — no external dependencies required. Features a custom synthwave visual theme with hand-designed vector sprites, a particle-based explosion system, and a starfield backdrop.

Move your ship left and right, blast the descending alien fleet, and use destructible bunker barriers for cover before the aliens reach you.

## Features

- Custom vector-drawn sprites for the player ship and aliens (`screen.register_shape`) — no default turtle shapes
- Neon synthwave color palette, centralized in a single `theme.py` module
- Static starfield background
- Particle-based explosion animation on alien and player destruction, colored to match the object destroyed
- Destructible bunker-style barriers, built from individually breakable segments arranged via a shape mask
- Player ship movement with screen boundary limits
- Shooting mechanic with fire-rate cooldown
- A full alien fleet that moves as a coordinated unit, changes direction at screen edges, and steps down after each bounce
- Bullet–alien, alien–player, bullet–barrier, and alien–barrier collision detection
- Live scoreboard tracking score and current level
- Progressive difficulty — each cleared wave respawns a faster fleet
- Game over screen with a one-key restart (`r` or `R`, no need to relaunch the program)

## Why `turtle` instead of a game engine?

This project is part of a portfolio built to demonstrate range across different tools and architectures. Unlike other projects in this portfolio built with Pygame-CE, this one deliberately uses only the Python standard library. It's a good showcase of:

- Manual game-loop timing (`time.sleep()` + `screen.tracer(0)` + `screen.update()`) instead of a dedicated game clock
- Event-driven keyboard input (`onkey`) rather than per-frame key-state polling
- Building game object hierarchies — and a distinctive visual identity — on top of a general-purpose graphics module never designed for real-time games
- Simulating effects `turtle` doesn't support natively (no alpha transparency) through shape scaling and color choices instead

## Controls

| Key | Action |
|---|---|
| ← / → | Move ship left / right |
| Space | Fire |
| R / r | Restart after Game Over |

## Tech Stack

- Python 3
- `turtle` (standard library)
- `tkinter` (standard library, used only to detect monitor resolution for window placement)

No third-party packages are required — see `requirements.txt`.

## Project Structure

```
space-invaders/
├── main.py              # Game loop, event bindings, collision orchestration
├── theme.py             # Centralized color palette
├── player.py            # Player ship class + custom shape definition
├── alien.py             # Alien class + fleet movement logic + custom shape definition
├── bullet.py            # Bullet class
├── barrier.py           # Barrier segment class + bunker shape mask
├── starfield.py         # Background starfield
├── explosion.py         # Particle-based explosion animation
├── scoreboard.py        # Score, level, and game-over display
├── requirements.txt
├── .gitignore
└── README.md
```

## Running the Game

```bash
python main.py
```

## Planned Improvements

This is an active project. Ideas for further iteration:

- Sound effects

## What I Learned

Some of the trickier bugs and design decisions while building this:

- **Safe iteration while removing items**: iterating over a list copy (`list[:]`) is required whenever items get removed from that list mid-loop — otherwise Python skips elements as indices shift.
- **Two-pass fleet direction logic**: flipping the fleet's shared direction mid-iteration (as soon as one alien hits an edge) causes the fleet to desync, with some aliens moving one way and others the other way in the same frame. Direction changes must be collected first, then applied in a separate pass after every alien has moved.
- **Nearest-target collision selection**: when multiple targets can be within hit range in the same frame (e.g. two barrier rows), always resolve the *closest* one rather than the first found in a list — otherwise the result silently depends on unrelated object-creation order.
- **`turtle.Terminator` vs `tkinter.TclError`**: closing the game window while the manual game loop is running can raise either exception depending on exactly when the window is destroyed — both need to be caught for a clean exit.
- **Composition vs. inheritance**: most game objects (`Player`, `Alien`, `Bullet`, `Barrier`, `Starfield`) are a single visual element, so they inherit from `Turtle` directly. `Explosion` manages a *group* of particles instead of being one itself, so it holds a list of `Turtle` instances rather than inheriting from `Turtle` — composition over inheritance when a class needs to coordinate multiple graphical objects.
- **Z-order in turtle graphics**: objects are layered in creation order, not draw-call order — the first `Turtle` instantiated renders at the back. This matters when building composite or layered effects.
- **Simulating shape masks for level/layout generation**: representing a barrier's silhouette as a 2D grid of 1s and 0s decouples the *shape* from the *placement loop*, so the loop stays generic while the visual design lives entirely in one small, easy-to-edit data structure.
- **Resetting all object state on restart, not just position**: a game restart needs to reset every piece of mutable state an object can carry (position, visibility, color) — resetting only position left the player ship invisible-but-still-active after the first restart.
