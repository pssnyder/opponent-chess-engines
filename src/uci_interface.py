#!/usr/bin/env python3
"""
UCI Interface for Opponent Engine
Implements Universal Chess Interface protocol for tournament play
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from opponent_engine import create_opponent, OpponentType
import chess
import threading
import time

class UCIOpponentEngine:
    def __init__(self, opponent_type: OpponentType):
        self.opponent_type = opponent_type
        self.engine = None
        self.board = chess.Board()
        self.searching = False
        self.search_thread = None
        
    def send(self, message):
        """Send message to GUI"""
        print(message, flush=True)
        
    def handle_uci(self):
        """Handle uci command"""
        self.send("id name OpponentEngine-" + self.opponent_type.value)
        self.send("id author OpponentEngine")
        self.send("option name OwnBook type check default true")
        if "elo" in self.opponent_type.value:
            elo = self.opponent_type.value.split("_")[-1]
            self.send(f"option name UCI_LimitStrength type check default true")
            self.send(f"option name UCI_Elo type spin default {elo} min 100 max 3000")
        self.send("uciok")
        
    def handle_isready(self):
        """Handle isready command"""
        if not self.engine:
            try:
                self.engine = create_opponent(self.opponent_type.value)
                self.send("readyok")
            except Exception as e:
                self.send(f"info string Error initializing engine: {e}")
                self.send("readyok")
        else:
            self.send("readyok")
            
    def handle_ucinewgame(self):
        """Handle ucinewgame command"""
        self.board = chess.Board()
        
    def handle_position(self, command):
        """Handle position command"""
        parts = command.split()
        if len(parts) < 2:
            return
            
        if parts[1] == "startpos":
            self.board = chess.Board()
            moves_start = 2
        elif parts[1] == "fen":
            # Find where moves start
            moves_start = None
            for i, part in enumerate(parts[2:], 2):
                if part == "moves":
                    moves_start = i + 1
                    break
            
            if moves_start:
                fen = " ".join(parts[2:moves_start-1])
            else:
                fen = " ".join(parts[2:])
                moves_start = len(parts)
                
            try:
                self.board = chess.Board(fen)
            except:
                self.send("info string Invalid FEN")
                return
        else:
            return
            
        # Apply moves
        if moves_start < len(parts) and parts[moves_start-1] == "moves":
            for move_str in parts[moves_start:]:
                try:
                    move = chess.Move.from_uci(move_str)
                    if move in self.board.legal_moves:
                        self.board.push(move)
                    else:
                        self.send(f"info string Illegal move: {move_str}")
                        return
                except:
                    self.send(f"info string Invalid move format: {move_str}")
                    return
                    
    def search_worker(self):
        """Worker thread for searching"""
        try:
            if not self.engine:
                self.engine = create_opponent(self.opponent_type.value)
                
            move = self.engine.get_move(self.board)
            if move and self.searching:
                self.send(f"bestmove {move.uci()}")
            elif self.searching:
                self.send("bestmove 0000")
        except Exception as e:
            self.send(f"info string Search error: {e}")
            self.send("bestmove 0000")
        finally:
            self.searching = False
            
    def handle_go(self, command):
        """Handle go command"""
        if self.searching:
            return
            
        self.searching = True
        self.search_thread = threading.Thread(target=self.search_worker)
        self.search_thread.start()
        
    def handle_stop(self):
        """Handle stop command"""
        self.searching = False
        if self.search_thread and self.search_thread.is_alive():
            self.search_thread.join(timeout=1.0)
            
    def handle_quit(self):
        """Handle quit command"""
        self.searching = False
        if self.search_thread and self.search_thread.is_alive():
            self.search_thread.join(timeout=1.0)
        if self.engine:
            self.engine.quit()
        sys.exit(0)
        
    def run(self):
        """Main UCI loop"""
        while True:
            try:
                line = input().strip()
                if not line:
                    continue
                    
                command = line.split()[0]
                
                if command == "uci":
                    self.handle_uci()
                elif command == "isready":
                    self.handle_isready()
                elif command == "ucinewgame":
                    self.handle_ucinewgame()
                elif command == "position":
                    self.handle_position(line)
                elif command == "go":
                    self.handle_go(line)
                elif command == "stop":
                    self.handle_stop()
                elif command == "quit":
                    self.handle_quit()
                else:
                    # Unknown command, ignore
                    pass
                    
            except EOFError:
                break
            except Exception as e:
                self.send(f"info string Error: {e}")

def main():
    """Main entry point"""
    # Default to opening + random if no argument provided
    opponent_type = OpponentType.OPENING_ONLY_RANDOM
    
    if len(sys.argv) > 1:
        try:
            opponent_type = OpponentType(sys.argv[1])
        except ValueError:
            print(f"Unknown opponent type: {sys.argv[1]}")
            print("Available types:")
            for ot in OpponentType:
                print(f"  {ot.value}")
            sys.exit(1)
    
    uci_engine = UCIOpponentEngine(opponent_type)
    uci_engine.run()

if __name__ == "__main__":
    main()
