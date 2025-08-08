#!/usr/bin/env python3
"""
Opening + 1200 ELO Opponent
Uses opening book when available, otherwise 1200 ELO Stockfish
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from opponent_engine import create_opponent, OpponentType
import chess

def main():
    print("Opening + 1200 ELO Opponent")
    print("=" * 40)
    
    engine = create_opponent(OpponentType.OPENING_PLUS_ELO_1200.value)
    board = chess.Board()
    
    try:
        while not board.is_game_over():
            print(f"\nCurrent position:")
            print(board)
            print(f"FEN: {board.fen()}")
            
            # Get user input for opponent move
            user_input = input("\nEnter your move (e.g., e2e4) or 'quit': ").strip()
            
            if user_input.lower() == 'quit':
                break
                
            try:
                user_move = chess.Move.from_uci(user_input)
                if user_move in board.legal_moves:
                    board.push(user_move)
                    print(f"You played: {user_move}")
                else:
                    print("Illegal move! Try again.")
                    continue
            except:
                print("Invalid move format! Use format like 'e2e4'")
                continue
            
            if board.is_game_over():
                break
                
            # Get engine move
            engine_move = engine.get_move(board)
            if engine_move:
                board.push(engine_move)
                print(f"Engine played: {engine_move}")
            else:
                print("Engine has no legal moves")
                break
                
        print(f"\nGame over! Result: {board.result()}")
        
    finally:
        engine.quit()

if __name__ == "__main__":
    main()
