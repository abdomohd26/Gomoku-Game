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
        self._screen = pygame.display.set_mode((800,800))
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

        button_width = 450
        button_height = 60

        input_box_width = 60
        input_box_height = 60
        label_width = 140
        horizontal_spacing = 10
        vertical_position = 275
        x_start = 175
        block_spacing = 30

        button1 = pygame.Rect(self._screen.get_width() // 2 - button_width // 2, 360, button_width, button_height)
        button2 = pygame.Rect(self._screen.get_width() // 2 - button_width // 2, 440, button_width, button_height)

        # Define static positions for input boxes
        label_box1 = pygame.Rect(x_start, vertical_position, label_width, input_box_height)
        input_box = pygame.Rect(label_box1.right + horizontal_spacing, vertical_position, input_box_width,
                                input_box_height)

        label_box2 = pygame.Rect(input_box.right + block_spacing, vertical_position, label_width, input_box_height)
        input_box2 = pygame.Rect(label_box2.right + horizontal_spacing, vertical_position, input_box_width,
                                 input_box_height)

        input_color_inactive = (30, 90, 150)
        input_color_active = (137, 180, 222)

        input_active = False
        input_active2 = False

        input_color = input_color_inactive
        input_color2 = input_color_inactive

        user_text = str(self.selected_depth)
        user_text2 = str(self.length)

        button_color = (30, 90, 150)
        shadow_color = (0, 22, 64)

        running = True
        while running:
            self._screen.blit(background, (0, 0))

            # Draw label 1
            pygame.draw.rect(self._screen, shadow_color, label_box1.move(4, 4), border_radius=12)
            pygame.draw.rect(self._screen, button_color, label_box1, border_radius=12)
            label_text1 = small_font.render("AI Depth", True, (255, 255, 255))
            self._screen.blit(label_text1, label_text1.get_rect(center=label_box1.center))

            # Draw input 1
            pygame.draw.rect(self._screen, shadow_color, input_box.move(4, 4), border_radius=10)
            pygame.draw.rect(self._screen, input_color, input_box, border_radius=10)
            text_surface = input_font.render(user_text, True, (0, 0, 0))
            self._screen.blit(text_surface,
                              (input_box.x + 10, input_box.y + (input_box.height - text_surface.get_height()) // 2))

            # Draw label 2
            pygame.draw.rect(self._screen, shadow_color, label_box2.move(4, 4), border_radius=12)
            pygame.draw.rect(self._screen, button_color, label_box2, border_radius=12)
            label_text2 = small_font.render("Length", True, (255, 255, 255))
            self._screen.blit(label_text2, label_text2.get_rect(center=label_box2.center))

            # Draw input 2
            pygame.draw.rect(self._screen, shadow_color, input_box2.move(4, 4), border_radius=10)
            pygame.draw.rect(self._screen, input_color2, input_box2, border_radius=10)
            text_surface2 = input_font.render(user_text2, True, (0, 0, 0))
            self._screen.blit(text_surface2,
                              (input_box2.x + 10, input_box2.y + (input_box2.height - text_surface2.get_height()) // 2))

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
                    # Activate input boxes correctly
                    if input_box.collidepoint(event.pos):
                        input_active = True
                        input_active2 = False
                    elif input_box2.collidepoint(event.pos):
                        input_active2 = True
                        input_active = False
                    else:
                        input_active = False
                        input_active2 = False

                    input_color = input_color_active if input_active else input_color_inactive
                    input_color2 = input_color_active if input_active2 else input_color_inactive

                    if button1.collidepoint(event.pos):
                        self.mode = "human_vs_ai"
                        try:
                            self.selected_depth = int(user_text)
                            self.length = int(user_text2)
                            print(f"Selected Depth: {self.selected_depth}, Length: {self.length}")
                        except ValueError:
                            self.selected_depth = 3
                            self.length = 5
                            print("Invalid input. Using default depth=3 and length=5")
                        running = False

                    elif button2.collidepoint(event.pos):
                        self.mode = "ai_vs_ai"
                        try:
                            self.selected_depth = int(user_text)
                            self.length = int(user_text2)
                            print(f"Selected Depth: {self.selected_depth}, Length: {self.length}")
                        except ValueError:
                            self.selected_depth = 3
                            self.length = 5
                            print("Invalid input. Using default depth=3 and length=5")
                        running = False

                elif event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.unicode.isdigit() and len(user_text) < 2:
                            user_text += event.unicode

                    elif input_active2:
                        if event.key == pygame.K_BACKSPACE:
                            user_text2 = user_text2[:-1]
                        elif event.key == pygame.K_RETURN:
                            input_active2 = False
                        elif event.unicode.isdigit() and len(user_text2) < 2:
                            user_text2 += event.unicode

    def game_loop(self, mode):
        while True:  # Outer loop to allow replay
            self.b = Board(self.length)

            if mode == "human_vs_ai":
                alg = AlgorithmMinimax(self.selected_depth)
                self._service = Service1(self.b, alg)
            else:
                alg1 = AlgorithmMinimax(self.selected_depth)
                alg2 = AlgorithmAlphaBeta(self.selected_depth)
                self._service = Service2(self.b, alg1, alg2)

            self._screen.fill((230, 230, 230))
            self.draw_board()
            pygame.display.update()

            if mode == "human_vs_ai":
                game_over = False
                draw = False

                while not game_over:
                    self.draw_board()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if self._service.get_turn() == 1:
                                try:
                                    cell_size = self._screen.get_width() // self.length
                                    x = event.pos[0] // cell_size
                                    y = event.pos[1] // cell_size

                                    self._service.player_move(x, y)
                                    pygame.mixer.Sound('click.wav').play()

                                    if Utils.game_over(self._service.get_board(), 1):
                                        game_over = True
                                    elif not any(0 in row for row in self._service.get_board()):
                                        draw = True
                                        game_over = True
                                except Exceptions.InvalidMove:
                                    pygame.mixer.Sound('wrong.wav').play()

                                    red_overlay = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                                    pygame.draw.rect(red_overlay, (255, 0, 0, 128), red_overlay.get_rect(),
                                                     border_radius=7)
                                    self._screen.blit(red_overlay, (x * cell_size, y * cell_size))
                                    pygame.display.update()
                                    time.sleep(0.5)
                                    self.draw_board()
                                    continue

                    if not game_over and self._service.get_turn() == -1:
                        self._service.computer_move()
                        pygame.mixer.Sound('click.wav').play()
                        if Utils.game_over(self._service.get_board(), -1):
                            game_over = True
                        elif not any(0 in row for row in self._service.get_board()):
                            draw = True
                            game_over = True

                # === Game Over Message ===
                self.draw_board()
                font = pygame.font.Font('Jersey10-Regular.ttf', 60)

                if draw:
                    message = 'Draw!'
                    pygame.mixer.Sound('draw.wav').play()
                    overlay_color = (100, 100, 100, 128)
                elif self._service.get_turn() == -1:
                    message = 'You Won!'
                    pygame.mixer.Sound('win.wav').play()
                    overlay_color = (0, 255, 0, 128)
                else:
                    message = 'You Lose!'
                    pygame.mixer.Sound('lose.wav').play()
                    overlay_color = (255, 0, 0, 128)

                overlay = pygame.Surface((800, 800), pygame.SRCALPHA)
                overlay.fill(overlay_color)
                self._screen.blit(overlay, (0, 0))

                text = font.render(message, True, (255, 255, 255))
                text_rect = text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2 - 70))
                bg_rect = text_rect.inflate(40, 20)
                pygame.draw.rect(self._screen, (54, 116, 181), bg_rect, border_radius=10)
                self._screen.blit(text, text_rect)

                # === Play Again Buttons ===
                font_small = pygame.font.Font('Jersey10-Regular.ttf', 40)
                button_width, button_height = 200, 50
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

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if button_play.collidepoint(event.pos):
                                break  # restart outer loop
                            elif button_quit.collidepoint(event.pos):
                                pygame.quit()
                                exit()
                    else:
                        continue
                    break

            else:  # AI vs AI Mode
                while True:
                    self.draw_board()
                    self._service.computer_move1()
                    pygame.mixer.Sound('click.wav').play()
                    time.sleep(0.5)
                    pygame.display.update()
                    if Utils.game_over(self._service.get_board(), -1):
                        break

                    self.draw_board()
                    self._service.computer_move2()
                    pygame.mixer.Sound('click.wav').play()
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

                pygame.mixer.Sound('win1.wav').play()
                green_overlay = pygame.Surface((800, 800), pygame.SRCALPHA)
                green_overlay.fill((0, 255, 0, 128))
                self._screen.blit(green_overlay, (0, 0))

                text = font.render(message, True, (255, 255, 255))
                text_rect = text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
                bg_rect = text_rect.inflate(40, 20)
                pygame.draw.rect(self._screen, (54, 116, 181), bg_rect, border_radius=10)
                self._screen.blit(text, text_rect)
                pygame.display.update()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()


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
                    if 360 <= y <= 420:
                        self.mode = "human_vs_ai"
                        waiting = False
                    elif 440 <= y <= 500:
                        self.mode = "ai_vs_ai"
                        waiting = False


        self.graphical.game_loop(self.mode)


if __name__ == "__main__":
    game = Graphical()
    game.main_menu()
    game.game_loop(game.mode)

