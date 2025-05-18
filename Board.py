from Exceptions import InvalidMove
from copy import deepcopy


class Board:
    """
    0   -> empty square
    1   -> player 1 move
    -1  -> player 2 move

    board   -> a matrix of dimension length
    """

    def __init__(self, length):
        self.length = length
        self._board = [[0] * length for i in range(length)]
        self._turn = 1

    @property
    def get_board(self):
        return deepcopy(self._board)

    @property
    def get_turn(self):
        return self._turn

    def move(self, x, y):
        if not (0 <= x < self.length and 0 <= y < self.length):
            raise InvalidMove("Move outside the board")

        if self._board[x][y] != 0:
            raise InvalidMove("Square taken")

        self._board[x][y] = self._turn
        self._turn *= -1
