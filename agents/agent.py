from abc import ABC, abstractmethod
import chess

class Agent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_move(self, board: chess.Board):
        raise NotImplementedError("Subclasses must implement this method")