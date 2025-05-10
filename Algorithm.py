import math
import random
from copy import deepcopy
import Utils

class BasicAlgo:
    @staticmethod
    def get_valid_locations(board):
        """
        @param board: the board
        @return: a list of all points that are in neighborhood with any point + the center point
        """
        locations = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 0:
                    continue
                if i > 0:
                    if j > 0:
                        if board[i - 1][j - 1] != 0 or board[i][j - 1] != 0:
                            locations.append((i, j))
                            continue
                    if j < len(board) - 1:
                        if board[i - 1][j + 1] != 0 or board[i][j + 1] != 0:
                            locations.append((i, j))
                            continue
                    if board[i - 1][j] != 0:
                        locations.append((i, j))
                        continue
                if i < len(board) - 1:
                    if j > 0:
                        if board[i + 1][j - 1] != 0 or board[i][j - 1] != 0:
                            locations.append((i, j))
                            continue
                    if j < len(board) - 1:
                        if board[i + 1][j + 1] != 0 or board[i][j + 1] != 0:
                            locations.append((i, j))
                            continue
                    if board[i + 1][j] != 0:
                        locations.append((i, j))
                        continue
        if board[len(board) // 2][len(board) // 2] == 0:
            locations.append((len(board) // 2, len(board) // 2))

        return list(set(locations))

    def score_board(self, board, player):
        # You should implement this based on your game's heuristic
        # For now, just a placeholder
        return Utils.heuristic(board, player)


class AlgorithmMiniMax(BasicAlgo):
    """
    Plain MiniMax algorithm (without Alpha-Beta pruning)
    """
    def __init__(self, depth):
        self.depth = depth

    def is_terminal_node(self, board):
        return Utils.game_over(board.get_board, -1) or Utils.game_over(board.get_board, 1) or \
               len(self.get_valid_locations(board.get_board)) == 0

    def mini_max(self, board_obj, depth, maximizing_player):
        board = board_obj.get_board
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board_obj)

        if depth == 0 or is_terminal:
            if is_terminal:
                if Utils.game_over(board, -1):
                    return None, 100000000
                elif Utils.game_over(board, 1):
                    return None, -100000000
            return None, self.score_board(board, -1)

        if maximizing_player:
            value = -math.inf
            point_good = random.choice(valid_locations)
            for point in valid_locations:
                row, col = point
                b_copy = deepcopy(board_obj)
                b_copy.move(row, col)
                new_score = self.mini_max(b_copy, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    point_good = point
            return point_good, value
        else:
            value = math.inf
            point_good = random.choice(valid_locations)
            for point in valid_locations:
                row, col = point
                b_copy = deepcopy(board_obj)
                b_copy.move(row, col)
                new_score = self.mini_max(b_copy, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    point_good = point
            return point_good, value

    def next_move(self, board):
        point, _ = self.mini_max(board, self.depth, True)
        return point[0], point[1]


class AlgorithmAlphaBeta(BasicAlgo):
    """
    MiniMax algorithm with Alpha-Beta pruning
    """
    def __init__(self, depth):
        self.depth = depth

    def is_terminal_node(self, board):
        return Utils.game_over(board.get_board, -1) or Utils.game_over(board.get_board, 1) or \
               len(self.get_valid_locations(board.get_board)) == 0

    def mini_max(self, board_obj, depth, alpha, beta, maximizing_player):
        board = board_obj.get_board
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board_obj)

        if depth == 0 or is_terminal:
            if is_terminal:
                if Utils.game_over(board, -1):
                    return None, math.inf
                elif Utils.game_over(board, 1):
                    return None, -math.inf
            return None, self.score_board(board, -1)

        if maximizing_player:
            value = -math.inf
            point_good = random.choice(valid_locations)
            for point in valid_locations:
                row, col = point
                b_copy = deepcopy(board_obj)
                b_copy.move(row, col)
                new_score = self.mini_max(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    point_good = point
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return point_good, value
        else:
            value = math.inf
            point_good = random.choice(valid_locations)
            for point in valid_locations:
                row, col = point
                b_copy = deepcopy(board_obj)
                b_copy.move(row, col)
                new_score = self.mini_max(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    point_good = point
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return point_good, value

    def next_move(self, board):
        point, _ = self.mini_max(board, self.depth, -math.inf, math.inf, True)
        return point[0], point[1]
