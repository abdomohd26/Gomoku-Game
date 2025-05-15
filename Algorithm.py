import math
import random
from copy import deepcopy
import Utils


class BasicAlgo:
    @staticmethod
    def get_valid_locations(board):
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

        return list(set(locations))  # remove duplicates

    def score_board(self, board, piece):
        score = 0
        if board[len(board)//2][len(board)//2] == piece:
            score += 3

        for line in board:
            for i in range(len(line) - 4):
                array = line[i:i+5]
                score += self.score_array(array, piece)

        for i in range(len(board)):
            column = [board[k][i] for k in range(len(board))]
            for j in range(len(column) - 4):
                array = column[j:j+5]
                score += self.score_array(array, piece)

        for i in range(len(board)-1):
            diagonal_above = [board[i - k][k] for k in range(i + 1)]
            diagonal_under = [board[len(board) - k - 1][len(board) - (i - k) - 1] for k in range(i + 1)]
            for j in range(len(diagonal_above) - 4):
                score += self.score_array(diagonal_above[j:j+5], piece)
            for j in range(len(diagonal_under) - 4):
                score += self.score_array(diagonal_under[j:j+5], piece)

        diagonal = [board[len(board) - 1 - k][k] for k in range(len(board))]
        for j in range(len(diagonal) - 4):
            score += self.score_array(diagonal[j:j + 5], piece)

        for i in range(1, len(board)):
            diagonal_under = [board[i + k][k] for k in range(len(board) - i)]
            diagonal_above = [board[k][i + k] for k in range(len(board) - i)]
            for j in range(len(diagonal_above) - 4):
                score += self.score_array(diagonal_above[j:j + 5], piece)
            for j in range(len(diagonal_under) - 4):
                score += self.score_array(diagonal_under[j:j + 5], piece)

        diagonal = [board[k][k] for k in range(len(board))]
        for j in range(len(diagonal) - 4):
            score += self.score_array(diagonal[j:j + 5], piece)
        return score

    @staticmethod
    def score_array(array, piece):
        if len(array) != 5:
            return 0
        opp_piece = -1 * piece
        score = 0
        if array.count(piece) == 2 and array.count(0) == 3:
            score += 5
        elif array.count(piece) == 3 and array.count(0) == 2:
            score += 500
        elif array.count(piece) == 4 and array.count(0) == 1:
            score += 250000
        elif array.count(piece) == 5:
            score += 1000000000

        elif array.count(opp_piece) == 4 and array.count(0) == 1:
            score -= 100000000
        elif array.count(opp_piece) == 3 and array.count(0) == 2:
            score -= 600
        elif array.count(opp_piece) == 2 and array.count(0) == 3:
            score -= 6

        return score


class AlgorithmAlphaBeta(BasicAlgo):
    def __init__(self, depth, turn):
        self.depth = depth
        self.turn = turn

    def is_terminal_node(self, board):
        return Utils.game_over(board.get_board, -self.turn) or Utils.game_over(board.get_board, self.turn) or len(self.get_valid_locations(board.get_board)) == 0

    def mini_max(self, board_obj, depth, alpha, beta, maximizing_player):
        board = board_obj.get_board
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board_obj)

        if depth == 0 or is_terminal:
            if is_terminal:
                if Utils.game_over(board, self.turn):
                    return None, 100000000
                elif Utils.game_over(board, -self.turn):
                    return None, -100000000
            return None, self.score_board(board, self.turn)

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
        point, value = self.mini_max(board, self.depth, -math.inf, math.inf, True)
        return point[0], point[1]


class AlgorithmMinimax(BasicAlgo):
    def __init__(self, depth, turn):
        self.depth = depth
        self.turn = turn

    def is_terminal_node(self, board):
        return Utils.game_over(board.get_board, -self.turn) or Utils.game_over(board.get_board, self.turn) or len(self.get_valid_locations(board.get_board)) == 0

    def mini_max(self, board_obj, depth, maximizing_player):
        board = board_obj.get_board
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board_obj)

        if depth == 0 or is_terminal:
            if is_terminal:
                if Utils.game_over(board, self.turn):
                    return None, 100000000
                elif Utils.game_over(board, -self.turn):
                    return None, -100000000
            return None, self.score_board(board, self.turn)

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
        point, value = self.mini_max(board, self.depth, True)
        return point[0], point[1]