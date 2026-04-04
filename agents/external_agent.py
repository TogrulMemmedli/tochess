import chess
import chess.engine
from .agent import Agent as BaseAgent

class UciAgent(BaseAgent):
    def __init__(self, name, engine_path, engine_options=None, time_limit=0.1):
        super().__init__(name=name)
        self.time_limit = time_limit
        
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        except FileNotFoundError:
            raise Exception(f"Error: '{engine_path}' not found. Make sure the engine is installed.")

        if engine_options:
            self.engine.configure(engine_options)

    def get_move(self, board: chess.Board):
        result = self.engine.play(board, chess.engine.Limit(time=self.time_limit))
        return result.move

    def close(self):
        self.engine.quit()