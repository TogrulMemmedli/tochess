import random
from .agent import Agent as BaseAgent

class GreedyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Greedy Agent")

    def get_move(self, board):
        legal_moves = list(board.legal_moves)
        
        captures = [move for move in legal_moves if board.is_capture(move)]
        
        if captures:
            return random.choice(captures)
        
        return random.choice(legal_moves) if legal_moves else None