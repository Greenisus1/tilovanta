# Tilovanta

Offline terminal turn-based tile path puzzle. Version 1.0.0. Original terminal artwork; no account, desktop or telemetry. No assets or names taken from other games.

## Install and run

    bash app-store.sh install
    bash app-store.sh run

Python3 with curses (normally included on Linux). No downloaded dependencies.

Arrows/WASD step. J arms a two-tile jump for the next direction; only its landing tile is checked. Blank gaps and ! hazards end the game when landed on. X is the finish. R starts a new board, Q quits. Every generated board has at least one safe step-by-step path; randomized tiles can create shortcuts. No timing, moving hazards, level progression or saves.

Interactive curses terminal at least 58x18. Too-small windows show a resize notice and retain/pause the game. Terminal default, no GUI and no desktop requirement. R with --seed restarts the same seeded sequence, otherwise a fresh random board. For a non-interactive snapshot, use:

    python3 tilovanta.py --seed 42 --demo

For tests:

    python3 -m unittest -v

8 core tests plus actual Linux PTY visual/input smoke. Linux tested; physical Raspberry Pi and non-Linux untested. Without curses the interactive game is unavailable. No paid features. games category marker line3; older stores still list/launch it. MIT license; see LICENSE.txt.
