"""
Opponent Chess Engine - A configurable chess engine for testing other engines
Features:
- Opening book lookup
- Random move generation
- Configurable ELO strength using Stockfish
- Multiple opponent types
"""

import chess
import chess.engine
import chess.polyglot
import random
import json
import os
from typing import Optional, Dict, Any
from enum import Enum

class OpponentType(Enum):
    OPENING_ONLY_RANDOM = "opening_only_random"
    RANDOM_ONLY = "random_only"  
    ELO_400 = "elo_400"
    OPENING_PLUS_ELO_800 = "opening_plus_elo_800"
    OPENING_PLUS_ELO_1200 = "opening_plus_elo_1200"

class OpponentEngine:
    def __init__(self, opponent_type: OpponentType, stockfish_path: Optional[str] = None):
        """
        Initialize the opponent engine
        
        Args:
            opponent_type: Type of opponent to create
            stockfish_path: Path to Stockfish binary (optional)
        """
        self.opponent_type = opponent_type
        self.board = chess.Board()
        self.opening_book = None
        self.stockfish_engine = None
        self.stockfish_path = stockfish_path
        
        # Load opening book if needed
        if self._uses_opening_book():
            self._load_opening_book()
            
        # Initialize Stockfish if needed
        if self._uses_stockfish():
            self._init_stockfish()
    
    def _uses_opening_book(self) -> bool:
        """Check if this opponent type uses opening book"""
        return self.opponent_type in [
            OpponentType.OPENING_ONLY_RANDOM,
            OpponentType.OPENING_PLUS_ELO_800,
            OpponentType.OPENING_PLUS_ELO_1200
        ]
    
    def _uses_stockfish(self) -> bool:
        """Check if this opponent type uses Stockfish"""
        return self.opponent_type in [
            OpponentType.ELO_400,
            OpponentType.OPENING_PLUS_ELO_800,
            OpponentType.OPENING_PLUS_ELO_1200
        ]
    
    def _load_opening_book(self):
        """Load opening book from polyglot file or JSON"""
        # Try to load comprehensive opening book first
        comprehensive_path = os.path.join(os.path.dirname(__file__), "..", "opening_books", "comprehensive_openings.json")
        if os.path.exists(comprehensive_path):
            with open(comprehensive_path, 'r') as f:
                self.opening_book = json.load(f)
                print(f"Loaded comprehensive opening book with {len(self.opening_book)} positions")
                return
        
        # Try to load polyglot book
        polyglot_path = os.path.join(os.path.dirname(__file__), "..", "opening_books", "book.bin")
        if os.path.exists(polyglot_path):
            self.opening_book = chess.polyglot.open_reader(polyglot_path)
        else:
            # Fallback to basic JSON-based opening book
            json_path = os.path.join(os.path.dirname(__file__), "..", "opening_books", "openings.json")
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    self.opening_book = json.load(f)
    
    def _init_stockfish(self):
        """Initialize Stockfish engine"""
        try:
            if self.stockfish_path and os.path.exists(self.stockfish_path):
                self.stockfish_engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            else:
                # Try common Stockfish locations
                common_paths = [
                    "stockfish",
                    "/usr/games/stockfish",
                    "/usr/local/bin/stockfish",
                    "C:\\stockfish\\stockfish.exe"
                ]
                for path in common_paths:
                    try:
                        self.stockfish_engine = chess.engine.SimpleEngine.popen_uci(path)
                        break
                    except:
                        continue
        except Exception as e:
            print(f"Warning: Could not initialize Stockfish: {e}")
            print("Falling back to random moves for non-opening positions")
    
    def get_elo_limit(self) -> Optional[int]:
        """Get the ELO limit for this opponent type"""
        elo_map = {
            OpponentType.ELO_400: 400,
            OpponentType.OPENING_PLUS_ELO_800: 800,
            OpponentType.OPENING_PLUS_ELO_1200: 1200
        }
        return elo_map.get(self.opponent_type)
    
    def get_move(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Get the next move for the given board position
        
        Args:
            board: Current chess board position
            
        Returns:
            Chess move or None if no move available
        """
        self.board = board.copy()
        
        # Check for game end
        if board.is_game_over():
            return None
        
        # Try opening book first if applicable
        if self._uses_opening_book():
            opening_move = self._get_opening_move(board)
            if opening_move:
                return opening_move
        
        # Use Stockfish if available and applicable
        if self._uses_stockfish() and self.stockfish_engine:
            return self._get_stockfish_move(board)
        
        # Fallback to random move
        return self._get_random_move(board)
    
    def _get_opening_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Get move from opening book"""
        if not self.opening_book:
            return None
            
        try:
            if isinstance(self.opening_book, dict):
                # JSON-based opening book
                fen = board.fen().split(' ')[0]  # Just the position part
                if fen in self.opening_book:
                    moves = self.opening_book[fen]
                    if moves:
                        move_str = random.choice(moves)
                        return chess.Move.from_uci(move_str)
            else:
                # Polyglot opening book
                try:
                    entries = list(self.opening_book.find_all(board))
                    if entries:
                        # Weight moves by their frequency in the book
                        move = random.choices(
                            [entry.move for entry in entries],
                            weights=[entry.weight for entry in entries]
                        )[0]
                        return move
                except:
                    pass
        except Exception as e:
            print(f"Error accessing opening book: {e}")
        
        return None
    
    def _get_stockfish_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Get move from Stockfish engine with ELO limitation"""
        if not self.stockfish_engine:
            return None
            
        try:
            # Configure Stockfish ELO if specified
            elo_limit = self.get_elo_limit()
            if elo_limit:
                self.stockfish_engine.configure({"UCI_LimitStrength": True, "UCI_Elo": elo_limit})
            
            # Get move with time limit
            result = self.stockfish_engine.play(board, chess.engine.Limit(time=1.0))
            return result.move
        except Exception as e:
            print(f"Error getting Stockfish move: {e}")
            return None
    
    def _get_random_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Get random legal move"""
        legal_moves = list(board.legal_moves)
        if legal_moves:
            return random.choice(legal_moves)
        return None
    
    def quit(self):
        """Clean up resources"""
        if self.stockfish_engine:
            self.stockfish_engine.quit()
        if self.opening_book and hasattr(self.opening_book, 'close'):
            self.opening_book.close()

def create_opponent(opponent_type: str, stockfish_path: Optional[str] = None) -> OpponentEngine:
    """
    Factory function to create opponent engines
    
    Args:
        opponent_type: String representation of opponent type
        stockfish_path: Optional path to Stockfish binary
        
    Returns:
        OpponentEngine instance
    """
    try:
        opp_type = OpponentType(opponent_type)
        return OpponentEngine(opp_type, stockfish_path)
    except ValueError:
        raise ValueError(f"Unknown opponent type: {opponent_type}")

if __name__ == "__main__":
    # Example usage
    engine = create_opponent("opening_only_random")
    board = chess.Board()
    
    print("Testing opponent engine...")
    for i in range(5):
        move = engine.get_move(board)
        if move:
            print(f"Move {i+1}: {move}")
            board.push(move)
        else:
            print("No move available")
            break
    
    print(f"Final position: {board.fen()}")
    engine.quit()
