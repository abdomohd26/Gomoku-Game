import Utils


class Service:
    def __init__(self, board):
        self._board = board

    def get_board(self):
        return self._board.get_board

    def get_length(self):
        return self._board.length

    def get_turn(self):
        return self._board.get_turn

    def game_over(self):
        return Utils.game_over(self.get_board(), self.get_turn())


class Service1(Service):  # human vs ai
    def __init__(self, board, algorithm):
        super().__init__(board)
        self._algorithm = algorithm

    def player_move(self, x, y):
        self._board.move(x, y)

    def computer_move(self):
        square = self._algorithm.next_move(self._board)
        self._board.move(square[0], square[1])


class Service2(Service):  # ai vs ai
    def __init__(self, board, algorithm1, algorithm2):
        super().__init__(board)
        self._algorithm1 = algorithm1
        self._algorithm2 = algorithm2

    def computer_move1(self):
        square = self._algorithm1.next_move(self._board)
        self._board.move(square[0], square[1])

    def computer_move2(self):
        square = self._algorithm2.next_move(self._board)
        self._board.move(square[0], square[1])
