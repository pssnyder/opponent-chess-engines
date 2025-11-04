# Chess Engine Template

A comprehensive, production-ready template for building UCI-compatible chess engines in Python. This template provides a complete foundation with advanced search algorithms, optimization techniques, and a clean modular design for rapid engine development and testing.

## Overview

This template includes everything needed to create a competitive chess engine:
- **Complete Search Infrastructure**: Minimax with alpha-beta pruning, iterative deepening
- **Advanced Optimizations**: Transposition table, move ordering, pruning techniques
- **Modular Evaluation System**: Easy to customize and extend
- **UCI Protocol Support**: Ready for tournament play and testing
- **Time Management**: Sophisticated time allocation for various time controls
- **Example Implementations**: Multiple working examples to learn from

## Quick Start

### Basic Usage

```python
from opponent_template import ChessEngineTemplate, UCIEngineInterface

# Create a basic engine
engine = ChessEngineTemplate()
move = engine.get_best_move(time_left=10.0)

# Use with UCI interface
interface = UCIEngineInterface()
interface.run()  # Starts UCI protocol
```

### Creating Custom Engines

```python
class MyEngine(ChessEngineTemplate):
    def __init__(self, **kwargs):
        kwargs.setdefault('engine_name', 'My Custom Engine')
        super().__init__(**kwargs)
    
    def _evaluate_position(self, board: chess.Board) -> int:
        # Your evaluation function here
        score = self._evaluate_material_simple(board)
        # Add your custom heuristics
        return score

# Run your engine
interface = UCIEngineInterface(MyEngine)
interface.run()
```

## Architecture

### Core Components

#### ChessEngineTemplate
The main engine class providing:
- **Search Algorithm**: Minimax with alpha-beta pruning
- **Move Ordering**: MVV-LVA, killer moves, history heuristic
- **Pruning**: Null move pruning, quiescence search
- **Transposition Table**: Zobrist hashing with replacement strategy
- **Time Management**: Adaptive time allocation

#### UCIEngineInterface
Complete UCI protocol implementation supporting:
- Standard UCI commands (`uci`, `isready`, `position`, `go`, `quit`)
- Configurable options (`MaxDepth`, `TTSize`)
- Time controls and depth-limited searches
- Error handling and logging

### Key Methods to Override

#### _evaluate_position(board) → int
**Required override** - Your main evaluation function.
```python
def _evaluate_position(self, board: chess.Board) -> int:
    """
    Evaluate position and return score in centipawns
    Positive = good for side to move
    """
    return your_evaluation_score
```

#### Optional Customizations
- `piece_values`: Custom piece value dictionary
- `_order_moves()`: Custom move ordering logic
- `_calculate_time_limit()`: Custom time management
- `_is_endgame()`: Endgame detection logic

## Built-in Examples

### 1. MaterialEngine
Simple material-only evaluation:
```bash
python opponent_template.py material
```

### 2. MaterialWithBishopPairs
Material + dynamic bishop pair evaluation:
```bash
python opponent_template.py bishops
```

### 3. CustomPieceValues
Demonstrates custom piece valuations:
```bash
python opponent_template.py custom
```

## Features

### Search Algorithm
- **Minimax with Alpha-Beta Pruning**: Classic negamax implementation
- **Iterative Deepening**: Progressive depth increase with time management
- **Principal Variation Search**: Enhanced alpha-beta with null window searches
- **Quiescence Search**: Captures-only search to avoid horizon effects
- **Null Move Pruning**: Skip move to achieve beta cutoffs faster

### Move Ordering (Optimized for Performance)
1. **Transposition Table Move**: Best move from previous search
2. **Checkmate Threats**: Moves leading to mate
3. **Checks**: All checking moves
4. **Captures**: MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
5. **Killer Moves**: Best non-capture moves that caused cutoffs
6. **Pawn Promotions**: Ranked by promoted piece value
7. **Pawn Advances**: Toward promotion ranks
8. **History Heuristic**: Success-based move ordering

### Optimizations
- **Zobrist Transposition Table**: Fast position hashing and lookup
- **Age-based Replacement**: Efficient memory management
- **Killer Move Tables**: 2 killer moves per ply
- **History Heuristic**: Move success tracking
- **Time Check Optimization**: Periodic time limit checking

### Time Management
Sophisticated time allocation strategy:
- **30+ minute games**: Conservative allocation (time/40 + increment*0.8)
- **10-30 minute games**: Moderate allocation (time/30 + increment*0.8)
- **1-10 minute games**: Aggressive allocation (time/20 + increment*0.8)
- **<1 minute games**: Emergency allocation (time/10 + increment*0.8)
- **Depth-based**: Unlimited time when depth specified

## Configuration Options

### Engine Parameters
```python
ChessEngineTemplate(
    max_depth=6,           # Maximum search depth (1-20)
    tt_size_mb=128,        # Transposition table size (16-1024 MB)
    engine_name="My Engine",  # UCI identification name
    piece_values={...}     # Custom piece values dictionary
)
```

### UCI Options
- `MaxDepth`: Maximum search depth (default: 6, range: 1-20)
- `TTSize`: Transposition table size in MB (default: 128, range: 16-1024)

## Performance Characteristics

### Typical Performance (Python 3.9+)
- **Node Rate**: 15,000-40,000 nodes/second
- **Depth Achievement**: 6-10 ply in practical time
- **Memory Usage**: 128-512 MB (configurable)
- **Time Overhead**: Minimal UCI protocol overhead

### Scaling
- **Opening**: Depth 6-8 in 1-3 seconds
- **Middle Game**: Depth 6-9 depending on complexity
- **Endgame**: Depth 8-15+ based on material count

## Development Guide

### Adding New Evaluation Features

1. **Override _evaluate_position()**:
```python
def _evaluate_position(self, board: chess.Board) -> int:
    score = self._evaluate_material_simple(board)
    score += self._evaluate_piece_activity(board)
    score += self._evaluate_king_safety(board)
    return score
```

2. **Add helper methods**:
```python
def _evaluate_piece_activity(self, board: chess.Board) -> int:
    # Your piece activity evaluation
    return activity_score

def _evaluate_king_safety(self, board: chess.Board) -> int:
    # Your king safety evaluation
    return safety_score
```

### Custom Move Ordering
```python
def _order_moves(self, board, moves, ply, tt_move=None):
    # Call parent implementation
    ordered = super()._order_moves(board, moves, ply, tt_move)
    # Add your custom ordering logic
    return your_custom_ordering(ordered)
```

### Engine Variants
Create different versions for testing:
```python
class AggressiveEngine(ChessEngineTemplate):
    def _calculate_time_limit(self, time_left, increment=0):
        # More aggressive time usage
        return super()._calculate_time_limit(time_left, increment) * 1.5

class DefensiveEngine(ChessEngineTemplate):
    def _evaluate_position(self, board):
        score = super()._evaluate_position(board)
        # Add defensive bonuses
        return score + self._defensive_bonus(board)
```

## Testing and Validation

### Quick Functionality Test
```python
python -c "
import opponent_template
engine = opponent_template.MaterialEngine()
print('Engine created successfully')
"
```

### UCI Protocol Test
```bash
echo -e 'uci\nisready\nposition startpos\ngo depth 5\nquit' | python opponent_template.py
```

### Performance Benchmarking
```bash
# Test different variants
echo -e 'uci\nposition startpos\ngo depth 6\nquit' | python opponent_template.py material
echo -e 'uci\nposition startpos\ngo depth 6\nquit' | python opponent_template.py bishops
```

## Integration with Chess GUIs

### Arena Chess GUI
1. Add engine: `python /path/to/opponent_template.py material`
2. Configure time controls
3. Start tournament or analysis

### ChessBase/Fritz
1. Install as UCI engine
2. Set appropriate hash size (TTSize option)
3. Configure analysis depth

### Lichess Bot
```python
# Example integration with python-chess
import chess.engine
engine = chess.engine.SimpleEngine.popen_uci("python opponent_template.py")
```

## Best Practices

### Performance
- Start with material-only evaluation for baseline
- Add features incrementally and measure impact
- Use larger transposition tables for longer games
- Profile evaluation function for bottlenecks

### Development
- Test each change with consistent benchmark positions
- Use version control for different evaluation experiments
- Keep evaluation functions deterministic for reproducible results
- Document evaluation parameter tuning

### Debugging
- Use depth-limited searches for analysis
- Print evaluation components for position understanding
- Compare with known engine evaluations
- Test edge cases (endgames, tactical positions)

## Extending the Template

### Common Extensions
1. **Positional Evaluation**: Piece-square tables, mobility, pawn structure
2. **Endgame Knowledge**: Tablebase integration, specific endgame rules
3. **Opening Theory**: Opening book integration, early game heuristics
4. **Tactical Awareness**: Pin detection, fork recognition, discovered attacks

### Advanced Features
1. **Multi-threading**: Parallel search implementation
2. **Pruning Enhancements**: Late move reductions, futility pruning
3. **Evaluation Tuning**: Automated parameter optimization
4. **Learning**: Position evaluation learning from games

## License and Attribution

This template is designed for educational and competitive use. Feel free to use as a foundation for your own chess engine development.

## Version History

- **v1.0**: Initial template with complete search infrastructure
- **Material Opponent**: Successfully tested baseline achieving depth 10
- **Template Conversion**: Generalized for rapid engine development

---

**Ready to build your chess engine? Start by inheriting from `ChessEngineTemplate` and implementing your `_evaluate_position()` method!**