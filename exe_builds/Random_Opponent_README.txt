# Random Opponent Chess Engine

A minimal UCI-compatible chess engine that plays random legal moves.

## Features
- Full UCI compatibility
- Plays completely random legal moves
- No opening book, no evaluation, just pure randomness
- Perfect for testing basic chess GUI integration
- Very fast response time

## UCI Commands Supported
- `uci` - Engine identification
- `isready` - Ready check
- `ucinewgame` - New game initialization
- `position` - Set board position
- `go` - Get a random move
- `quit` - Exit engine

## Usage with Chess GUIs
1. Add as a UCI engine in your chess GUI (Arena, Cutechess, etc.)
2. No configuration needed - it will play random legal moves
3. Compatible with any time control (moves instantly)

## Technical Details
- Uses python-chess for legal move generation
- No external dependencies in the executable
- Platform: Windows 64-bit
