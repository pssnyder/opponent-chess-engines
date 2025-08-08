#!/usr/bin/env python3
"""
UCI Wrapper for OpponentEngine_Random_Only
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from uci_interface import UCIOpponentEngine, OpponentType

if __name__ == "__main__":
    uci_engine = UCIOpponentEngine(OpponentType("random_only"))
    uci_engine.run()
