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
        self.length = 5
        self.b = Board(self.length)
        self._screen = pygame.display.set_mode((800,800))
        self._service = Service(self.b)
        self.selected_depth = 1
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
        background = pygame.transform.scale(background, (800, 800))
        self._screen.blit(background, (0, 0))

        font = pygame.font.Font('Jersey10-Regular.ttf', 70)
        small_font = pygame.font.Font('Jersey10-Regular.ttf', 45)
        input_font = pygame.font.Font('Jersey10-Regular.ttf', 40)

        button_width = 400
        button_height = 60
        button1 = pygame.Rect(self._screen.get_width() // 2 - button_width // 2, 320, button_width, button_height)
        button2 = pygame.Rect(self._screen.get_width() // 2 - button_width // 2, 400, button_width, button_height)

        input_font = pygame.font.Font('Jersey10-Regular.ttf', 40)
        input_box = pygame.Rect(self._screen.get_width() // 2 + 40, 250, 45, 45)  # Reduced width
        input_color = (200, 200, 200)
        user_text = str(self.selected_depth)
        input_active = False


        button_color = (30, 90, 150)
        shadow_color = (0, 22, 64)
        input_color_inactive = (200, 200, 200)
        input_color_active = (255, 255, 255)
        input_color = input_color_inactive

        running = True
        while running:
            self._screen.blit(background, (0, 0))

            # Draw input box
            input_label = input_font.render("AI Depth:", True, (0, 0, 0))
            self._screen.blit(input_label, (input_box.x - 150, input_box.y + 7))


            pygame.draw.rect(self._screen, input_color, input_box, border_radius=10)
            text_surface = input_font.render(user_text, True, (0, 0, 0))
            self._screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

            # Draw buttons
            pygame.draw.rect(self._screen, shadow_color, button1.move(4, 4), border_radius=12)
            pygame.draw.rect(self._screen, shadow_color, button2.move(4, 4), border_radius=12)
            pygame.draw.rect(self._screen, button_color, button1, border_radius=12)
            pygame.draw.rect(self._screen, button_color, button2, border_radius=12)

            txt1 = small_font.render("Human  VS  Minimax", True, (255, 255, 255))
            txt2 = small_font.render("Minimax VS Alpha-Beta", True, (255, 255, 255))

            self._screen.blit(txt1, txt1.get_rect(center=button1.center))
            self._screen.blit(txt2, txt2.get_rect(center=button2.center))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_active = not input_active
                    else:
                        input_active = False
                    input_color = input_color_active if input_active else input_color_inactive

                    if button1.collidepoint(event.pos) or button2.collidepoint(event.pos):
                        try:
                            self.selected_depth = int(user_text)
                            print(f"Selected Depth: {self.selected_depth}")
                        except ValueError:
                            self.selected_depth = 3  # Default fallback
                            print("Invalid input, using default depth = 3")
                        running = False  # Exit menu and start game

                elif event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.unicode.isdigit() and len(user_text) < 2:  # limit to 2-digit numbers
                        user_text += event.unicode


    def game_loop(self, mode):

        self._screen.fill((230, 230, 230))
        self.draw_board()

        pygame.display.update()

        if mode == "human_vs_ai":
            alg = AlgorithmMinimax(self.selected_depth)
            self._service = Service1(self.b, alg)
            game_over = False
            draw = False
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
                                click = pygame.mixer.Sound('click.wav')
                                click.play()
                                if Utils.game_over(self._service.get_board(), 1):
                                    game_over = True
                                elif not any(0 in row for row in self._service.get_board()):
                                    draw = True
                                    game_over = True
                            except Exceptions.InvalidMove:
                                wrong = pygame.mixer.Sound('wrong.wav')
                                wrong.play()

                                cell_size = self._screen.get_width() // self.length
                                x = event.pos[0] // cell_size
                                y = event.pos[1] // cell_size

                                red_overlay = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

                                pygame.draw.rect(
                                    red_overlay,
                                    (255, 0, 0, 128),  # RGBA, 128 = 50% opacity
                                    red_overlay.get_rect(),
                                    border_radius=7
                                )

                                # Blit overlay and update
                                self._screen.blit(red_overlay, (x * cell_size, y * cell_size))
                                pygame.display.update()
                                time.sleep(0.5)

                                self.draw_board()
                                continue
                self.draw_board()
                if not game_over and self._service.get_turn() == -1:
                    self._service.computer_move()
                    click = pygame.mixer.Sound('click.wav')
                    click.play()
                    if Utils.game_over(self._service.get_board(), -1):
                        game_over = True
                    elif not any(0 in row for row in self._service.get_board()):
                        draw = True
                        game_over = True

            self.draw_board()


            font = pygame.font.Font('Jersey10-Regular.ttf', 60)
            if draw:
                green_overlay = pygame.Surface((800, 800), pygame.SRCALPHA)
                green_overlay.fill((0, 255, 0, 128))
                self._screen.blit(green_overlay, (0, 0))
                message = 'Draw!'
                bg_color = (162, 185, 167)
                # draw_sound = pygame.mixer.Sound('draw.wav')
                # draw_sound.play()

            elif self._service.get_turn() == -1:
                green_overlay = pygame.Surface((800, 800), pygame.SRCALPHA)
                green_overlay.fill((0, 255, 0, 128))
                self._screen.blit(green_overlay, (0, 0))
                message = 'You Won!'
                bg_color = (54, 116, 181)
                win_sound = pygame.mixer.Sound('win.wav')
                win_sound.play()

            elif self._service.get_turn() == 1:
                red_overlay = pygame.Surface((800, 800), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 128))
                self._screen.blit(red_overlay, (0, 0))
                message = 'You lose!'
                bg_color = (54, 116, 181)
                lose_sound = pygame.mixer.Sound('lose.wav')
                lose_sound.play()

            else:
                return

            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2 - 70))
            bg_rect = text_rect.inflate(40, 20)

            pygame.draw.rect(self._screen, bg_color, bg_rect, border_radius=10)
            self._screen.blit(text, text_rect)
            pygame.display.update()
#Play Again

            font_small = pygame.font.Font('Jersey10-Regular.ttf', 40)
            button_width = 200
            button_height = 50
            button_spacing = 40

            total_width = 2 * button_width + button_spacing
            start_x = (self._screen.get_width() - total_width) // 2
            y_pos = self._screen.get_height() // 2 + 40

            button_play = pygame.Rect(start_x, y_pos, button_width, button_height)
            button_quit = pygame.Rect(start_x + button_width + button_spacing, y_pos, button_width, button_height)

            pygame.draw.rect(self._screen, (54, 116, 181), button_play, border_radius=10)
            pygame.draw.rect(self._screen, (54, 116, 181), button_quit, border_radius=10)

            txt_play = font_small.render("Play Again", True, (255, 255, 255))
            txt_quit = font_small.render("Quit", True, (255, 255, 255))

            self._screen.blit(txt_play, txt_play.get_rect(center=button_play.center))
            self._screen.blit(txt_quit, txt_quit.get_rect(center=button_quit.center))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if button_play.collidepoint(x, y):
                            self.__init__()  # Reset the game
                            self.game_loop("human_vs_ai")
                            return
                        elif button_quit.collidepoint(x, y):
                            pygame.quit()
                            return


        else:
            alg1 = AlgorithmMinimax(self.selected_depth)
            alg2 = AlgorithmAlphaBeta(self.selected_depth)
            self._service = Service2(self.b, alg1, alg2)

            while True:
                self.draw_board()
                self._service.computer_move1()
                click = pygame.mixer.Sound('click.wav')
                click.play()
                time.sleep(0.5)
                pygame.display.update()

                if Utils.game_over(self._service.get_board(), -1):
                    break

                self.draw_board()
                self._service.computer_move2()
                click = pygame.mixer.Sound('click.wav')
                click.play()
                time.sleep(0.5)
                pygame.display.update()

                if Utils.game_over(self._service.get_board(), -1):
                    break

            self.draw_board()
            font = pygame.font.Font('Jersey10-Regular.ttf', 50)

            if self._service.get_turn() == -1:
                message = 'Minimax Algorithm Won!'
                green_overlay = pygame.Surface((800, 800), pygame.SRCALPHA)
                green_overlay.fill((0, 255, 0, 128))
                self._screen.blit(green_overlay, (0, 0))
                win_sound1 = pygame.mixer.Sound('win1.wav')
                win_sound1.play()
            else:
                message = 'Alpha Beta Algorithm Won!'
                green_overlay = pygame.Surface((800, 800), pygame.SRCALPHA)
                green_overlay.fill((0, 255, 0, 128))
                self._screen.blit(green_overlay, (0, 0))
                win_sound1 = pygame.mixer.Sound('win1.wav')
                win_sound1.play()

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
