from Algorithm import AlgorithmMiniMax, AlgorithmAlphaBeta
from Board import Board
import Utils

class Service:
    def __init__(self, board, algorithm):
        self._board = board
        self._algorithm = algorithm

    def get_board(self):
        return self._board.get_board

    def get_length(self):
        return self._board.length

    def get_turn(self):
        return self._board.get_turn

    def game_over(self):
        return Utils.game_over(self.get_board(), self.get_turn())

    def player_move(self, x, y):
        self._board.move(x, y)

    def computer_move(self):
        x, y = self._algorithm.next_move(self._board)
        self._board.move(x, y)
