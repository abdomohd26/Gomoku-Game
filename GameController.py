import pygame
import time
import Utils
import Exceptions
from Service import Service, Service1, Service2
from Board import Board
from Algorithm import AlgorithmAlphaBeta, AlgorithmMinimax


class Graphical:
    def __init__(self):
        pygame.init()
        self.length = 15
        self.board = Board(self.length)
        self._screen = pygame.display.set_mode((45 * self.length, 45 * self.length))
        self._service = Service(self.board)
        pygame.display.set_caption("Gomoku")

    def draw_board(self):
        board = self._service.get_board()
        for c in range(len(board)):
            for r in range(len(board)):
                pygame.draw.rect(self._screen, (227, 185, 100), (c * 45, r * 45, 45, 45))
                pygame.draw.rect(self._screen, (84, 56, 0), (c * 45, r * 45, 45, 45), 1)

        for c in range(len(board)):
            for r in range(len(board)):
                if board[c][r] == 1:
                    pygame.draw.circle(self._screen, (255, 255, 255), (c * 45 + 22, r * 45 + 22), 19)
                elif board[c][r] == -1:
                    pygame.draw.circle(self._screen, (0, 0, 0), (c * 45 + 22, r * 45 + 22), 19)

        pygame.display.update()

    def main_menu(self):
        self._screen.fill((240, 220, 180))
        width, height = self._screen.get_size()

        # Scale font sizes
        title_font_size = height // 10
        button_font_size = height // 20

        font = pygame.font.Font('freesansbold.ttf', title_font_size)
        button_font = pygame.font.Font('freesansbold.ttf', button_font_size)

        # Title
        title = font.render("Welcome to Gomoku", True, (0, 0, 0))
        title_rect = title.get_rect(center=(width // 2, height // 6))
        self._screen.blit(title, title_rect)

        # Button texts
        txt1 = button_font.render("1. Human vs AI (Minimax)", True, (255, 255, 255))
        txt2 = button_font.render("2. AI (Minimax) vs AI (Alpha-Beta)", True, (255, 255, 255))

        # Get text rects and center them
        txt1_rect = txt1.get_rect(center=(width // 2, height // 2))
        txt2_rect = txt2.get_rect(center=(width // 2, height // 2 + txt1_rect.height + height // 20))

        # Inflate for padding (10px horizontal, 5px vertical)
        button1_rect = txt1_rect.inflate(20, 10)
        button2_rect = txt2_rect.inflate(20, 10)

        # Draw rectangles behind text
        pygame.draw.rect(self._screen, (100, 100, 200), button1_rect)
        pygame.draw.rect(self._screen, (100, 200, 100), button2_rect)

        # Blit text
        self._screen.blit(txt1, txt1_rect)
        self._screen.blit(txt2, txt2_rect)

        pygame.display.update()

        # Store the button rectangles if you want to use them for click detection
        self._button1_rect = button1_rect
        self._button2_rect = button2_rect


    def game_loop(self, mode):

        self._screen.fill((240, 220, 180))
        self.draw_board()

        pygame.display.update()

        if mode == "human_vs_ai":
            alg = AlgorithmMinimax(1)
            self._service = Service1(self.board, alg)
            game_over = False

            while not game_over:
                self.draw_board()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self._service.get_turn() == 1:
                            try:
                                x = event.pos[0] // 45
                                y = event.pos[1] // 45
                                self._service.player_move(x, y)
                                if Utils.game_over(self._service.get_board(), 1):
                                    game_over = True
                            except Exceptions:
                                continue
                self.draw_board()
                if not game_over and self._service.get_turn() == -1:
                    self._service.computer_move()
                    if Utils.game_over(self._service.get_board(), -1):
                        game_over = True

            self.draw_board()
            font = pygame.font.Font('freesansbold.ttf', 70)

            if self._service.get_turn() == -1:
                text = font.render('You Won!', True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (45 * self.length // 2, 45 * self.length // 2)
                pygame.draw.rect(self._screen, (0, 128, 0), text_rect.inflate(20, 10))

                self._screen.blit(text, text_rect)

            elif self._service.get_turn() == 1:
                text = font.render('You Lost!', True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (45 * self.length // 2, 45 * self.length // 2)
                pygame.draw.rect(self._screen, (128, 0, 0), text_rect.inflate(20, 10))

                self._screen.blit(text, text_rect)

            pygame.display.update()

            r = True
            while r:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        r = False
            pygame.quit()
        else:
            alg1 = AlgorithmMinimax(3)
            alg2 = AlgorithmAlphaBeta(3)
            self._service = Service2(self.board, alg1, alg2)

            while True:
                self.draw_board()
                self._service.computer_move1()
                time.sleep(0.5)
                pygame.display.update()

                if Utils.game_over(self._service.get_board(), -1):
                    break

                self.draw_board()
                self._service.computer_move2()
                time.sleep(0.5)
                pygame.display.update()

                if Utils.game_over(self._service.get_board(), -1):
                    break

            self.draw_board()
            font = pygame.font.Font('freesansbold.ttf', 50)

            if self._service.get_turn() == -1:
                text = font.render('Minimax Algorithm Won!', True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (45 * self.length // 2, 45 * self.length // 2)
                pygame.draw.rect(self._screen, (54, 116, 181), text_rect.inflate(20, 10))

                self._screen.blit(text, text_rect)

            elif self._service.get_turn() == 1:
                text = font.render('Alpa Beta Algorithm Won!', True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (45 * self.length // 2, 45 * self.length // 2)
                pygame.draw.rect(self._screen, (54, 116, 181), text_rect.inflate(20, 10))

                self._screen.blit(text, text_rect)

            pygame.display.update()

            r = True
            while r:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        r = False
            pygame.quit()


class GameController:
    def __init__(self):
        self.mode = None
        self.graphical = Graphical()

    def run(self):
        self.graphical.main_menu()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.graphical._button1_rect.collidepoint(x, y):
                        self.mode = "human_vs_ai"
                        waiting = False
                    elif self.graphical._button2_rect.collidepoint(x, y):
                        self.mode = "ai_vs_ai"
                        waiting = False

        self.graphical.game_loop(self.mode)


if __name__ == "__main__":
    game = GameController()
    game.run()
