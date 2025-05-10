import pygame
from Game_modes import HumanVsMiniMax, MiniMaxVsAlphaBeta
from Service import Service
from Board import Board
from Algorithm import AlgorithmMiniMax, AlgorithmAlphaBeta

class Graphical:
    def __init__(self, service):
        self._service = service
        pygame.init()
        self._screen = pygame.display.set_mode((45 * self._service.get_length(), 45 * self._service.get_length()))
        pygame.display.set_caption("Gomoku")

    def draw_board(self):
        board = self._service.get_board()
        for c in range(len(board)):
            for r in range(len(board)):
                pygame.draw.rect(self._screen, (120, 96, 66), (c * 45, r * 45, 45, 45))
                pygame.draw.rect(self._screen, (0, 0, 0), (c * 45, r * 45, 45, 45), 1)

        for c in range(len(board)):
            for r in range(len(board)):
                if board[c][r] == 1:
                    pygame.draw.circle(self._screen, (59, 47, 31), (c * 45 + 45 // 2, r * 45 + 45 // 2), 45 // 2 - 3)
                elif board[c][r] == -1:
                    pygame.draw.circle(self._screen, (255, 210, 166), (c * 45 + 45 // 2, r * 45 + 45 // 2), 45 // 2 - 3)

        pygame.display.update()

    def main_menu(self):
        self._screen.fill((240, 220, 180))
        font = pygame.font.Font('freesansbold.ttf', 40)
        small_font = pygame.font.Font('freesansbold.ttf', 30)

        title = font.render("Welcome to Gomoku", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self._screen.get_width() // 2, 100))
        self._screen.blit(title, title_rect)

        button1 = pygame.Rect(self._screen.get_width() // 2 - 200, 200, 400, 60)
        button2 = pygame.Rect(self._screen.get_width() // 2 - 250, 300, 500, 60)

        pygame.draw.rect(self._screen, (100, 100, 200), button1)
        pygame.draw.rect(self._screen, (100, 200, 100), button2)

        txt1 = small_font.render("1. Human vs AI (Minimax)", True, (255, 255, 255))
        txt2 = small_font.render("2. AI (Minimax) vs AI (Alpha-Beta)", True, (255, 255, 255))

        self._screen.blit(txt1, (self._screen.get_width() // 2 - 100, 210))
        self._screen.blit(txt2, (self._screen.get_width() // 2 - 120, 310))

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    row, col = x // 45, y // 45
                    if self._service.get_board()[row][col] == 0:  # If the square is empty
                        self._service.player_move(row, col)
                        return False
        return False

    def game_loop(self):
        running = True
        while running:
            self._screen.fill((240, 220, 180))  # Clear screen

            self.draw_board()  # Draw the current state of the board
            running = not self.handle_events()  # Handle events (player move)
            if self._service.game_over():
                self.display_winner()
                running = False
            pygame.time.wait(100)

    def display_winner(self):
        font = pygame.font.Font('freesansbold.ttf', 40)
        winner = "Human Wins!" if self._service.get_turn() == -1 else "Computer Wins!"
        text = font.render(winner, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
        self._screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)

class GameController:
    def __init__(self):
        self.board = Board(15)  # Create a 15x15 board
        self.algorithm = AlgorithmMiniMax(depth=3)  # Use MiniMax with depth 3
        self.service = Service(self.board, self.algorithm)
        self.graphical = Graphical(self.service)

    def run(self):
        self.graphical.main_menu()
        self.graphical.game_loop()


if __name__ == "__main__":
    game = GameController()
    game.run()
