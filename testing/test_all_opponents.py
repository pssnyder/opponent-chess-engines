#!/usr/bin/env python3
"""
Test all opponent types to ensure they're working correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.opponent_engine import create_opponent, OpponentType
import chess

def test_opponent_type(opponent_type, test_moves=3):
    """Test a specific opponent type"""
    print(f"\nTesting {opponent_type.value}:")
    print("-" * 40)
    
    try:
        engine = create_opponent(opponent_type.value)
        board = chess.Board()
        
        for i in range(test_moves):
            move = engine.get_move(board)
            if move:
                print(f"Move {i+1}: {move} ({'opening book' if engine._get_opening_move(board) else 'engine/random'})")
                board.push(move)
                
                # Also test with a response
                legal_moves = list(board.legal_moves)
                if legal_moves:
                    response = legal_moves[0]  # Simple response
                    board.push(response)
                    print(f"Response: {response}")
            else:
                print(f"No move available at move {i+1}")
                break
        
        print(f"Final FEN: {board.fen()}")
        engine.quit()
        return True
        
    except Exception as e:
        print(f"Error testing {opponent_type.value}: {e}")
        return False

def main():
    """Test all opponent types"""
    print("Testing All Opponent Engine Types")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    for opponent_type in OpponentType:
        total_count += 1
        if test_opponent_type(opponent_type):
            success_count += 1
    
    print(f"\n\nTest Results:")
    print(f"Successful: {success_count}/{total_count}")
    print(f"Failed: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ All opponent types working correctly!")
    else:
        print("❌ Some opponent types failed - check error messages above")

if __name__ == "__main__":
    main()
