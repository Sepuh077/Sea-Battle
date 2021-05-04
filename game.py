import arcade
from copy import deepcopy

s_w, s_h = arcade.get_display_size()


class GameWindow(arcade.Window):
    def __init__(self):
        super(GameWindow, self).__init__(s_w, s_h, "Sea battle", True)
        arcade.set_background_color(arcade.color.GREEN)
        self.all_ships = [4, 3, 2, 1]
        self.player1_board = []
        self.player2_board = []
        self.player1_visual_board = []
        self.player2_visual_board = []
        self.is_game_started = False
        self.is_first_player_turn = True
        self.left_ships = None
        self.box_size = int(s_h / 15)
        self.start_pos = None
        self.end_pos = None
        self.is_correct_ship = True
        self.board_start_x = int((s_w - 10 * self.box_size) / 2)
        self.board_start_y = int((s_h - 10 * self.box_size) / 2)
        self.board_size_during_game = min((s_w / 2 - s_w / 50), (s_h - s_h / 50))
        self.board1_start_x = (s_w / 2 - self.board_size_during_game) / 2
        self.board2_start_x = s_w / 2 + (s_w / 2 - self.board_size_during_game) / 2
        self.game_ended = False
        self.is_player1_winner = False
        self.player1_ships = deepcopy(self.all_ships)
        self.player2_ships = deepcopy(self.all_ships)

    def setup(self):
        self.is_game_started = False
        self.is_first_player_turn = True
        self.left_ships = deepcopy(self.all_ships)
        self.fill_boards()
        self.start_pos = [0, 0]
        self.end_pos = [0, 4]
        self.is_correct_ship = True
        self.game_ended = False
        self.player1_ships = deepcopy(self.all_ships)
        self.player2_ships = deepcopy(self.all_ships)

    def on_draw(self):
        arcade.start_render()
        if self.is_game_started:
            self.draw_during_game()
        else:
            self.draw_board_in_start()

    def draw_board_in_start(self):
        if self.is_first_player_turn:
            board = self.player1_board
        else:
            board = self.player2_board

        for i in range(10):
            for j in range(10):
                if board[i][j] <= 0:
                    color = arcade.color.WHITE
                else:
                    color = arcade.color.BLACK

                arcade.draw_rectangle_filled(self.board_start_x + (i + 0.5) * self.box_size,
                                             self.board_start_y + (j + 0.5) * self.box_size,
                                             self.box_size, self.box_size, color)

        pos = deepcopy(self.start_pos)
        while pos != self.end_pos:
            if board[pos[0]][pos[1]] != 0:
                color = arcade.color.RED
                self.is_correct_ship = False
            else:
                color = arcade.color.GRAY

            arcade.draw_rectangle_filled(self.board_start_x + (pos[0] + 0.5) * self.box_size,
                                         self.board_start_y + (pos[1] + 0.5) * self.box_size,
                                         self.box_size, self.box_size, color)
            if pos[0] == self.end_pos[0]:
                pos[1] += 1
            else:
                pos[0] += 1

        for i in range(11):
            arcade.draw_line(self.board_start_x, self.board_start_y + i * self.box_size,
                             self.board_start_x + 10 * self.box_size,
                             self.board_start_y + i * self.box_size, arcade.color.BLACK)
            arcade.draw_line(self.board_start_x + i * self.box_size, self.board_start_y,
                             self.board_start_x + i * self.box_size,
                             self.board_start_y + 10 * self.box_size, arcade.color.BLACK)

    def draw_during_game(self):
        if self.is_first_player_turn:
            text = "First player`s turn"
            text_x = self.board2_start_x + self.board_size_during_game / 2
        else:
            text = "Second player`s turn"
            text_x = self.board1_start_x + self.board_size_during_game / 2
            arcade.draw_rectangle_filled(self.board2_start_x + self.board_size_during_game / 2, s_h / 2,
                                         self.board_size_during_game, self.board_size_during_game, (0, 0, 0, 100))

        arcade.draw_text(text, text_x, s_h / 2 + self.board_size_during_game / 2,
                         arcade.color.BLACK, s_h / 50, anchor_x="center")
        self.draw_board(self.player1_visual_board, self.board1_start_x)
        self.draw_board(self.player2_visual_board, self.board2_start_x)

        if self.is_first_player_turn:
            arcade.draw_rectangle_filled(self.board1_start_x + self.board_size_during_game / 2, s_h / 2,
                                         self.board_size_during_game, self.board_size_during_game, (0, 0, 0, 100))
        else:
            arcade.draw_rectangle_filled(self.board2_start_x + self.board_size_during_game / 2, s_h / 2,
                                         self.board_size_during_game, self.board_size_during_game, (0, 0, 0, 100))

        if self.game_ended:
            arcade.draw_text("END", s_w / 2, s_h / 2, arcade.color.BLACK, s_h / 10, anchor_x="center")

    def draw_board(self, board, start_x):
        start_y = (s_h - self.board_size_during_game) / 2
        box_size = self.board_size_during_game / 10
        for i in range(10):
            for j in range(10):
                if board[i][j] >= -1:
                    color = arcade.color.WHITE
                elif board[i][j] <= -3:
                    color = arcade.color.GRAY
                else:
                    color = arcade.color.PINK

                arcade.draw_rectangle_filled(start_x + (i + 0.5) * box_size,
                                             start_y + (j + 0.5) * box_size,
                                             box_size, box_size, color)

        for i in range(11):
            arcade.draw_line(start_x, start_y + i * box_size,
                             start_x + 10 * box_size,
                             start_y + i * box_size, arcade.color.BLACK)
            arcade.draw_line(start_x + i * box_size, start_y,
                             start_x + i * box_size,
                             start_y + 10 * box_size, arcade.color.BLACK)

    def fill_boards(self):
        row = []
        for _ in range(10):
            row.append(0)

        self.player1_board = []
        self.player2_board = []
        for _ in range(10):
            self.player1_board.append(deepcopy(row))
            self.player2_board.append(deepcopy(row))

    def on_key_release(self, key: int, modifiers: int):
        if not self.is_game_started:
            if key == arcade.key.LEFT and self.start_pos[0] > 0 and self.end_pos[0] > 0:
                self.start_pos[0] -= 1
                self.end_pos[0] -= 1

            if key == arcade.key.RIGHT and self.start_pos[0] < 9 and self.end_pos[0] < 10:
                self.start_pos[0] += 1
                self.end_pos[0] += 1

            if key == arcade.key.UP and self.start_pos[1] < 9 and self.end_pos[1] < 10:
                self.start_pos[1] += 1
                self.end_pos[1] += 1

            if key == arcade.key.DOWN and self.start_pos[1] > 0 and self.end_pos[1] > 0:
                self.start_pos[1] -= 1
                self.end_pos[1] -= 1

            if key == arcade.key.C:
                if self.start_pos[0] == self.end_pos[0]:
                    self.end_pos[0] = self.start_pos[0] + self.end_pos[1] - self.start_pos[1]
                    self.end_pos[1] = self.start_pos[1]
                    if self.end_pos[0] > 10:
                        self.start_pos[0] -= (self.end_pos[0] - 10)
                        self.end_pos[0] = 10
                else:
                    self.end_pos[1] = self.start_pos[1] + self.end_pos[0] - self.start_pos[0]
                    self.end_pos[0] = self.start_pos[0]
                    if self.end_pos[1] > 10:
                        self.start_pos[1] -= (self.end_pos[1] - 10)
                        self.end_pos[1] = 10

            if key == arcade.key.ENTER and self.is_correct_ship:
                if self.is_first_player_turn:
                    board = self.player1_board
                else:
                    board = self.player2_board

                pos = deepcopy(self.start_pos)
                x,  y = pos[0], pos[1]
                while pos != self.end_pos:
                    board[x][y] = 1
                    for i in range(max(0, pos[0] - 1), min(10, pos[0] + 2)):
                        for j in range(max(0, pos[1] - 1), min(10, pos[1] + 2)):
                            if board[i][j] == 0:
                                board[i][j] = -1

                    if pos[0] == self.end_pos[0]:
                        pos[1] += 1
                        y += 1
                    else:
                        pos[0] += 1
                        x += 1

                index = self.end_pos[0] - self.start_pos[0] + self.end_pos[1] - self.start_pos[1] - 1
                self.left_ships[index] -= 1
                if self.left_ships[index] == 0:
                    if index > 0:
                        self.start_pos = [0, 0]
                        self.end_pos = [0, index]
                    else:
                        if self.is_first_player_turn:
                            self.is_first_player_turn = False
                            self.left_ships = deepcopy(self.all_ships)
                            self.start_pos = [0, 0]
                            self.end_pos = [0, 4]
                        else:
                            self.is_game_started = True
                            self.is_first_player_turn = True
                            self.player1_visual_board = deepcopy(self.player1_board)
                            self.player2_visual_board = deepcopy(self.player2_board)
                else:
                    self.start_pos = [0, 0]
                    self.end_pos = [0, index + 1]

            self.is_correct_ship = True

    def on_mouse_release(self, x, y, button, modifiers):
        box_size = self.board_size_during_game / 10
        start_y = (s_h - self.board_size_during_game) / 2
        if self.is_game_started and not self.game_ended:
            if self.is_first_player_turn:
                board = self.player2_visual_board
                start_x = self.board2_start_x
            else:
                board = self.player1_visual_board
                start_x = self.board1_start_x

            if start_x < x < start_x + self.board_size_during_game and \
                    start_y < y < start_y + self.board_size_during_game:
                i = int((x - start_x) / box_size)
                j = int((y - start_y) / box_size)
                if board[i][j] == 0 or board[i][j] == -1:
                    board[i][j] = -2
                    self.is_first_player_turn = not self.is_first_player_turn
                elif board[i][j] == 1:
                    board[i][j] = -4
                    self.check_completely_ship_destroyed(board, i, j)

        elif self.game_ended:
            self.setup()

    def check_completely_ship_destroyed(self, board, x, y):
        if (x < 9 and board[x + 1][y] == 1) or (x > 0 and board[x - 1][y] == 1) or \
                (y < 9 and board[x][y + 1] == 1) or (y > 0 and board[x][y - 1] == 1):
            return

        start = [x, y]
        end = [x, y]
        j = x
        while j < 9 and (board[j + 1][y] == -4 or board[j + 1][y] == 1):
            end[0] += 1
            j += 1
            if board[j][y] == 1:
                return
        j = x
        while j > 0 and (board[j - 1][y] == -4 or board[j - 1][y] == 1):
            start[0] -= 1
            j -= 1
            if board[j][y] == 1:
                return

        j = y
        while j < 9 and (board[x][j + 1] == -4 or board[x][j + 1] == 1):
            end[1] += 1
            j += 1
            if board[x][j] == 1:
                return

        j = y
        while j > 0 and (board[x][j - 1] == -4 or board[x][j - 1] == 1):
            start[1] -= 1
            j -= 1
            if board[x][j] == 1:
                return

        for i in range(max(0, start[0] - 1), min(10, end[0] + 2)):
            for j in range(max(0, start[1] - 1), min(10, end[1] + 2)):
                if 1 > board[i][j] > -3:
                    board[i][j] = -2

        index = end[0] - start[0] + end[1] - start[1]
        if self.is_first_player_turn:
            self.player2_ships[index] -= 1
            self.game_ended = is_game_ended(self.player2_ships)
        else:
            self.player1_ships[index] -= 1
            self.game_ended = is_game_ended(self.player1_ships)


def is_game_ended(array):
    for i in range(4):
        if array[i] != 0:
            return False

    return True


window = GameWindow()
window.setup()
arcade.set_window(window)
arcade.run()
