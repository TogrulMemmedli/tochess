import chess
import math
from .agent import Agent as BaseAgent
import random

class HeuristicAgent(BaseAgent):
    def __init__(self):
        super().__init__(name=f"Heuristic Agent)")        
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

    def evaluate_board(self, board):
        if board.is_checkmate():
            return -9999 if board.turn == chess.WHITE else 9999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                val = self.piece_values.get(piece.piece_type, 0)
                if piece.color == chess.WHITE:
                    score += val
                else:
                    score -= val
        return score

    def get_move(self, board: chess.Board):
        best_move = None
        is_white = board.turn == chess.WHITE
        best_value = -float('inf') if is_white else float('inf')

        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)

        for move in legal_moves:
            board.push(move)
            board_value = self.evaluate_board(board)
            board.pop()

            if is_white:
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
            else:
                if board_value < best_value:
                    best_value = board_value
                    best_move = move

        return best_move if best_move else list(board.legal_moves)[0]