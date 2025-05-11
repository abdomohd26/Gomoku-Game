import pygame
import time
import Utils
import Exceptions
from Service import Service, Service1, Service2
from Board import Board
from Algorithm import AlgorithmAlphaBeta, AlgorithmMinimax
pygame.mixer.init()


class Graphical:
    def __init__(self):
        pygame.init()
        self.length = 6
        self.b = Board(self.length)
        self._screen = pygame.display.set_mode((800,800))
        self._service = Service(self.b)
        pygame.display.set_caption("Gomoku")

    def draw_board(self):
        board = self._service.get_board()
        board_size = len(board)
        cell_size = 800 // board_size

        for c in range(board_size):
            for r in range(board_size):
                rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
                pygame.draw.rect(self._screen, (146, 184, 224), rect, border_radius=7)
                pygame.draw.rect(self._screen, (237, 237, 237), rect, width=1, border_radius=7)

        for c in range(board_size):
            for r in range(board_size):
                center = (c * cell_size + cell_size // 2, r * cell_size + cell_size // 2)
                radius = cell_size // 2 - 3

                if board[c][r] == 1:
                    pygame.draw.circle(self._screen, (80, 160, 255), center, radius)
                    pygame.draw.circle(self._screen, (200, 230, 255),
                                       (center[0] - radius // 3, center[1] - radius // 3), radius // 4)
                    pygame.draw.circle(self._screen, (30, 90, 180), center, radius, 2)

                elif board[c][r] == -1:
                    pygame.draw.circle(self._screen, (30, 60, 120), center, radius)
                    pygame.draw.circle(self._screen, (180, 200, 230),
                                       (center[0] - radius // 3, center[1] - radius // 3), radius // 4)
                    pygame.draw.circle(self._screen, (10, 25, 70), center, radius, 2)

        pygame.display.update()

    def main_menu(self):
        background = pygame.image.load("background.png")
        background = pygame.transform.scale(background, (800,800))
        self._screen.blit(background, (0, 0))

        font = pygame.font.Font('Jersey10-Regular.ttf', 70)
        small_font = pygame.font.Font('Jersey10-Regular.ttf', 45)

        # title = font.render("Welcome to Gomoku", True, (0, 0, 0))
        # title_rect = title.get_rect(center=(self._screen.get_width() // 2, 100))
        # self._screen.blit(title, title_rect)

        button_width = 400
        button_height = 60
        button1 = pygame.Rect(self._screen.get_width() // 2 - button_width // 2, 320, button_width, button_height)
        button2 = pygame.Rect(self._screen.get_width() // 2 - button_width // 2, 400, button_width, button_height)


        button_color = (30, 90, 150)
        shadow_color = (0, 22, 64)
        # border_color = (30, 90, 150)


        shadow_offset = 4
        pygame.draw.rect(self._screen, shadow_color, button1.move(shadow_offset, shadow_offset), border_radius=12)
        pygame.draw.rect(self._screen, shadow_color, button2.move(shadow_offset, shadow_offset), border_radius=12)


        pygame.draw.rect(self._screen, button_color, button1, border_radius=12)
        pygame.draw.rect(self._screen, button_color, button2, border_radius=12)

        # pygame.draw.rect(self._screen, border_color, button1, 2, border_radius=12)
        # pygame.draw.rect(self._screen, border_color, button2, 2, border_radius=12)


        txt1 = small_font.render("Human  VS  Minimax", True, (255, 255, 255))
        txt2 = small_font.render("Minimax VS Alpha-Beta", True, (255, 255, 255))

        txt1_rect = txt1.get_rect(center=button1.center)
        txt2_rect = txt2.get_rect(center=button2.center)

        self._screen.blit(txt1, txt1_rect)
        self._screen.blit(txt2, txt2_rect)

        pygame.display.update()

    def game_loop(self, mode):

        self._screen.fill((230, 230, 230))
        self.draw_board()

        pygame.display.update()

        if mode == "human_vs_ai":
            alg = AlgorithmMinimax(3)
            self._service = Service1(self.b, alg)
            game_over = False

            while not game_over:
                self.draw_board()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self._service.get_turn() == 1:
                            try:
                                cell_size = self._screen.get_width() // self.length
                                x = event.pos[0] // cell_size
                                y = event.pos[1] // cell_size

                                self._service.player_move(x, y)
                                if Utils.game_over(self._service.get_board(), 1):
                                    game_over = True
                            except Exceptions.InvalidMove:
                                continue
                self.draw_board()
                if not game_over and self._service.get_turn() == -1:
                    self._service.computer_move()
                    if Utils.game_over(self._service.get_board(), -1):
                        game_over = True

            self.draw_board()
            font = pygame.font.Font('Jersey10-Regular.ttf', 60)

            if self._service.get_turn() == -1:
                message = 'You Won!'
                bg_color = (54, 116, 181)
                win_sound = pygame.mixer.Sound('win.wav')
                win_sound.play()

            elif self._service.get_turn() == 1:
                message = 'lose Win!'
                bg_color = (54, 116, 181)
                lose_sound = pygame.mixer.Sound('lose.wav')
                lose_sound.play()

            else:
                return

            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
            bg_rect = text_rect.inflate(40, 20)

            pygame.draw.rect(self._screen, bg_color, bg_rect, border_radius=10)
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
            self._service = Service2(self.b, alg1, alg2)

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
            font = pygame.font.Font('Jersey10-Regular.ttf', 50)

            if self._service.get_turn() == -1:
                message = 'Minimax Algorithm Won!'
            else:
                message = 'Alpha Beta Algorithm Won!'

            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
            bg_rect = text_rect.inflate(40, 20)

            pygame.draw.rect(self._screen, (54, 116, 181), bg_rect, border_radius=10)
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
                    if 320 <= y <= 380:
                        self.mode = "human_vs_ai"
                        waiting = False
                    elif 390 <= y <= 450:
                        self.mode = "ai_vs_ai"
                        waiting = False

        self.graphical.game_loop(self.mode)


if __name__ == "__main__":
    game = GameController()
    game.run()
