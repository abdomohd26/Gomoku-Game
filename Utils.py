def game_over(board, turn):
    """
    Checks if the game is over : five in a raw
                                 five on a column
                                 five on diagonal

    @return: True if the game is over
             False if game can continue
    """
    def five_consecutive(array):
        if len(array) < 5:
            return False
        c = 1
        for el in range(1, len(array)):
            if array[el] == array[el - 1] and array[el] == turn:
                c += 1
            else:
                c = 1
            if c == 5:
                return True
        return False

    # line
    for line in board:
        if five_consecutive(line):
            return True

    # column
    for i in range(len(board)):
        column = [board[k][i] for k in range(len(board))]
        if five_consecutive(column):
            return True

    # diagonal "/"  - secondary diagonal
    for i in range(len(board)):
        diagonal_above = [board[i - k][k] for k in range(i + 1)]
        diagonal_under = [board[len(board) - k - 1][len(board) - (i - k) - 1] for k in
                          range(i + 1)]
        if five_consecutive(diagonal_above) or five_consecutive(diagonal_under):
            return True

    # diagonal "\"  - main diagonal
    for i in range(len(board)):
        diagonal_under = [board[i + k][k] for k in range(len(board) - i)]
        diagonal_above = [board[k][i + k] for k in range(len(board) - i)]
        if five_consecutive(diagonal_under) or five_consecutive(diagonal_above):
            return True

    return False

def heuristic(board, player):
    """
    Evaluate board state for the given player.
    Returns a score based on number of 2, 3, 4, and 5 in-a-rows.
    """
    def count_sequences(line, player, length):
        count = 0
        for i in range(len(line) - length + 1):
            window = line[i:i + length]
            if all(cell == player for cell in window):
                count += 1
        return count

    def evaluate_lines(lines, player):
        score = 0
        weights = {2: 10, 3: 100, 4: 1000, 5: 100000}
        for line in lines:
            for length, weight in weights.items():
                score += count_sequences(line, player, length) * weight
        return score

    size = len(board)
    lines = []

    # Rows and Columns
    for i in range(size):
        lines.append(board[i])                      # row
        lines.append([board[j][i] for j in range(size)])  # column

    # Diagonals (\)
    for p in range(2 * size - 1):
        diag = []
        for q in range(max(p - size + 1, 0), min(p + 1, size)):
            diag.append(board[q][p - q])
        if len(diag) >= 2:
            lines.append(diag)

    # Anti-diagonals (/)
    for p in range(2 * size - 1):
        anti_diag = []
        for q in range(max(p - size + 1, 0), min(p + 1, size)):
            i = q
            j = size - 1 - (p - q)
            if 0 <= i < size and 0 <= j < size:
                anti_diag.append(board[i][j])
        if len(anti_diag) >= 2:
            lines.append(anti_diag)

    # Final score = player's advantage - opponent's
    player_score = evaluate_lines(lines, player)
    opponent_score = evaluate_lines(lines, -player)
    return player_score - opponent_score

