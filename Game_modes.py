from Algorithm import AlgorithmMiniMax, AlgorithmAlphaBeta
from Service import Service


class HumanVsMiniMax:
    def __init__(self, board):
        self.board = board
        self.algorithm = AlgorithmMiniMax(depth=3)  # Use MiniMax with a depth of 3
        self.service = Service(board, self.algorithm)

    def start_game(self):
        game_over = False
        while not game_over:
            # Handle the human move
            self.handle_human_move()
            if self.service.game_over():
                game_over = True
                break

            # Handle the AI move
            self.service.computer_move()
            if self.service.game_over():
                game_over = True

    def handle_human_move(self):
        # The human plays by clicking on the board (this will be handled in the GUI controller)
        pass


class MiniMaxVsAlphaBeta:
    def __init__(self, board):
        self.board = board
        self.algorithm_minimax = AlgorithmMiniMax(depth=3)  # Use MiniMax with a depth of 3
        self.algorithm_alphabeta = AlgorithmAlphaBeta(depth=3)  # Use AlphaBeta with a depth of 3
        self.service_minimax = Service(board, self.algorithm_minimax)
        self.service_alphabeta = Service(board, self.algorithm_alphabeta)

    def start_game(self):
        game_over = False
        while not game_over:
            # Handle MiniMax move
            self.service_minimax.computer_move()
            if self.service_minimax.game_over():
                game_over = True
                break

            # Handle AlphaBeta move
            self.service_alphabeta.computer_move()
            if self.service_alphabeta.game_over():
                game_over = True
