# Opponent Chess Engine

A configurable Python chess engine designed specifically for testing and training other chess engines. This engine provides various opponent types with different playing styles and strength levels.

## Features

- **Opening Book Support**: Uses JSON-based opening book for strong opening play
- **Multiple Opponent Types**: 5 different opponent configurations
- **UCI Protocol**: Full UCI support for tournament play
- **Configurable ELO**: Uses Stockfish with ELO limitations
- **Random Fallback**: Falls back to random moves when other methods unavailable

## Opponent Types

1. **Opening Only + Random** (`opening_only_random`)
   - Plays opening book moves when available
   - Falls back to random legal moves

2. **Random Only** (`random_only`)
   - Plays only random legal moves
   - Good for testing basic functionality

3. **400 ELO** (`elo_400`)
   - Uses Stockfish limited to 400 ELO strength
   - Beginner level play

4. **Opening + 800 ELO** (`opening_plus_elo_800`)
   - Opening book moves when available
   - 800 ELO Stockfish otherwise
   - Intermediate level play

5. **Opening + 1200 ELO** (`opening_plus_elo_1200`)
   - Opening book moves when available
   - 1200 ELO Stockfish otherwise
   - Advanced intermediate play

## Installation

1. Ensure Python 3.7+ is installed
2. Install required packages:
   ```bash
   pip install python-chess stockfish pyinstaller
   ```
3. Download or install Stockfish engine for ELO-based opponents

## Project Structure

```
opponent_engine/
├── src/                    # Source code
│   ├── opponent_engine.py  # Main engine logic
│   └── uci_interface.py    # UCI protocol implementation
├── build/                  # Build scripts and interactive versions
├── opening_books/          # Opening book files
│   └── openings.json      # JSON-based opening book
├── exe_builds/            # Generated executables
└── build_executables.py   # Build script
```

## Usage

### Building Executables

Run the build script to generate all executables:

```bash
python build_executables.py
```

This creates:
- **Interactive versions**: For testing and manual play
- **UCI versions**: For tournament and engine-vs-engine play

### Interactive Play

Run any interactive executable to play against the engine:

```bash
./exe_builds/Interactive_Opening_Random.exe
```

### Tournament Play

Use UCI executables with chess GUIs or tournament managers:

```bash
./exe_builds/OpponentEngine_Opening_800_ELO.exe
```

### Programmatic Usage

```python
from src.opponent_engine import create_opponent, OpponentType
import chess

# Create an opponent
engine = create_opponent(OpponentType.OPENING_PLUS_ELO_800.value)

# Get moves
board = chess.Board()
move = engine.get_move(board)

# Clean up
engine.quit()
```

## Configuration

### Opening Book

The opening book is stored in `opening_books/openings.json`. You can:
- Add new positions and responses
- Modify existing opening lines
- Use Polyglot format books (place `book.bin` in opening_books/)

### Stockfish Path

If Stockfish is not in your PATH, specify the path when creating the engine:

```python
engine = OpponentEngine(OpponentType.ELO_400, stockfish_path="/path/to/stockfish")
```

## UCI Commands Supported

- `uci` - Initialize UCI mode
- `isready` - Check if engine is ready
- `ucinewgame` - Start new game
- `position` - Set board position
- `go` - Start searching for move
- `stop` - Stop current search
- `quit` - Exit engine

## Development

### Adding New Opponent Types

1. Add new enum value to `OpponentType` in `opponent_engine.py`
2. Update relevant methods (`_uses_opening_book`, `_uses_stockfish`, `get_elo_limit`)
3. Create build script entry in `build_executables.py`

### Customizing Opening Book

The JSON opening book format:
```json
{
  "position_fen": ["move1", "move2", "move3"],
  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR": ["e2e4", "d2d4", "g1f3"]
}
```

### Testing

Test the core engine functionality:

```bash
python src/opponent_engine.py
```

## Requirements

- Python 3.7+
- python-chess
- stockfish (optional, for ELO-based opponents)
- pyinstaller (for building executables)

## License

This project is designed for chess engine development and testing purposes.

## Troubleshooting

### Stockfish Not Found

If you get Stockfish errors:
1. Install Stockfish: https://stockfishchess.org/download/
2. Add to PATH or specify path when creating engine
3. For ELO-based opponents, ensure Stockfish supports UCI_LimitStrength

### Import Errors

If you get import errors when running built executables:
1. Ensure all dependencies are installed
2. Rebuild with `python build_executables.py`
3. Check that source files are in correct directories

### Opening Book Issues

If opening moves seem random:
1. Check that `opening_books/openings.json` exists
2. Verify JSON format is correct
3. Add debug prints to see if book is loading

## Future Enhancements

- Support for PGN-based opening books
- Time management for tournament play
- Endgame tablebase support
- Neural network evaluation
- Custom evaluation functions
