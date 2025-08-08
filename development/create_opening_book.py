#!/usr/bin/env python3
"""
PGN Opening Book Extractor
Analyzes PGN files to extract opening positions and moves for the opening book
"""

import os
import chess
import chess.pgn
import json
from collections import defaultdict
import sys

def extract_openings_from_pgn(pgn_file_path, max_moves=8):
    """
    Extract opening moves from a PGN file
    
    Args:
        pgn_file_path: Path to the PGN file
        max_moves: Maximum number of moves to extract from each game
        
    Returns:
        Dictionary mapping positions to lists of moves
    """
    openings = defaultdict(set)
    
    try:
        with open(pgn_file_path, 'r', encoding='utf-8', errors='ignore') as pgn_file:
            game_count = 0
            while True:
                try:
                    game = chess.pgn.read_game(pgn_file)
                    if game is None:
                        break
                    
                    board = game.board()
                    moves_analyzed = 0
                    
                    # Analyze the opening moves
                    for move in game.mainline_moves():
                        if moves_analyzed >= max_moves:
                            break
                            
                        # Get the position before the move
                        position_fen = board.fen().split(' ')[0]  # Just the position part
                        
                        # Record this move as a possibility for this position
                        openings[position_fen].add(move.uci())
                        
                        # Make the move
                        board.push(move)
                        moves_analyzed += 1
                    
                    game_count += 1
                    if game_count % 100 == 0:
                        print(f"Processed {game_count} games from {os.path.basename(pgn_file_path)}")
                        
                except Exception as e:
                    # Skip problematic games
                    continue
                    
    except Exception as e:
        print(f"Error reading {pgn_file_path}: {e}")
        return {}
    
    # Convert sets to lists
    return {pos: list(moves) for pos, moves in openings.items()}

def process_all_pgn_files(pgn_directory, output_file):
    """
    Process all PGN files in a directory and create comprehensive opening book
    """
    all_openings = defaultdict(set)
    
    # Get list of PGN files
    pgn_files = [f for f in os.listdir(pgn_directory) if f.endswith('.pgn')]
    
    print(f"Found {len(pgn_files)} PGN files to process...")
    
    for i, pgn_file in enumerate(pgn_files, 1):
        print(f"\nProcessing {i}/{len(pgn_files)}: {pgn_file}")
        pgn_path = os.path.join(pgn_directory, pgn_file)
        
        file_openings = extract_openings_from_pgn(pgn_path, max_moves=10)
        
        # Merge with all openings
        for position, moves in file_openings.items():
            all_openings[position].update(moves)
        
        print(f"  Extracted {len(file_openings)} positions")
    
    # Convert to final format and sort by popularity
    final_openings = {}
    for position, moves in all_openings.items():
        # Limit to most common moves (max 6 per position to avoid too much branching)
        move_list = list(moves)
        if len(move_list) > 6:
            move_list = move_list[:6]
        final_openings[position] = move_list
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(final_openings, f, indent=2, sort_keys=True)
    
    print(f"\nOpening book created with {len(final_openings)} positions")
    print(f"Saved to: {output_file}")
    
    return final_openings

def add_essential_openings(openings_dict):
    """
    Add some essential opening positions that might be missing
    """
    # Starting position
    start_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    if start_pos not in openings_dict:
        openings_dict[start_pos] = []
    openings_dict[start_pos].extend(["e2e4", "d2d4", "g1f3", "c2c4", "b1c3"])
    openings_dict[start_pos] = list(set(openings_dict[start_pos]))  # Remove duplicates
    
    # Essential e4 responses
    after_e4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
    if after_e4 not in openings_dict:
        openings_dict[after_e4] = []
    openings_dict[after_e4].extend(["e7e5", "c7c5", "e7e6", "c7c6", "d7d6", "g8f6"])
    openings_dict[after_e4] = list(set(openings_dict[after_e4]))
    
    # Essential d4 responses  
    after_d4 = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR"
    if after_d4 not in openings_dict:
        openings_dict[after_d4] = []
    openings_dict[after_d4].extend(["d7d5", "g8f6", "c7c6", "e7e6", "c7c5", "f7f5"])
    openings_dict[after_d4] = list(set(openings_dict[after_d4]))
    
    return openings_dict

def main():
    """Main function"""
    pgn_dir = "s:/Maker Stuff/Programming/Opponent Chess Engine/opponent_engine/pgn_data_openings"
    output_file = "s:/Maker Stuff/Programming/Opponent Chess Engine/opponent_engine/opening_books/comprehensive_openings.json"
    
    if not os.path.exists(pgn_dir):
        print(f"PGN directory not found: {pgn_dir}")
        return
    
    print("Creating comprehensive opening book from PGN files...")
    print("=" * 60)
    
    # Process all PGN files
    openings = process_all_pgn_files(pgn_dir, output_file)
    
    # Add essential openings
    print("\nAdding essential opening moves...")
    openings = add_essential_openings(openings)
    
    # Save final version
    with open(output_file, 'w') as f:
        json.dump(openings, f, indent=2, sort_keys=True)
    
    print(f"\nFinal opening book saved with {len(openings)} positions")
    
    # Show some statistics
    total_moves = sum(len(moves) for moves in openings.values())
    avg_moves = total_moves / len(openings) if openings else 0
    
    print(f"Total move options: {total_moves}")
    print(f"Average moves per position: {avg_moves:.1f}")
    
    # Show sample positions
    print("\nSample positions from opening book:")
    sample_count = 0
    for position, moves in list(openings.items())[:5]:
        try:
            board = chess.Board(position + " w - - 0 1")
            print(f"\nPosition: {board.fen()}")
            print(f"Moves: {', '.join(moves)}")
            sample_count += 1
        except:
            continue

if __name__ == "__main__":
    main()
