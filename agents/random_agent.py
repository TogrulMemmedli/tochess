import random
from .agent import Agent as BaseAgent

class RandomAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Random Agent")

    def get_move(self, board):
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None