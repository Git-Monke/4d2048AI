# import random
import random
import copy


class Board:
    def __init__(self):
        self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.is_over = False

    def clone(self):
        clone = Board()
        clone.board = copy.deepcopy(self.board)
        return clone

    # 0 = up, 1 = down, 2 = left, 3 = right
    def small_move(self, direction):
        movement = False

        for i in range(4):
            sub_board = self.board[i]

            if direction == 0:
                for i in range(2):
                    if (sub_board[i] == sub_board[2 + i] and sub_board[i] != 0) or (
                        sub_board[i] == 0 and sub_board[2 + i] != 0
                    ):
                        movement = True
                        sub_board[i] += sub_board[2 + i]
                        sub_board[2 + i] = 0
            if direction == 1:
                for i in range(2):
                    if (sub_board[i] == sub_board[2 + i] and sub_board[i] != 0) or (
                        sub_board[i] != 0 and sub_board[2 + i] == 0
                    ):
                        movement = True
                        sub_board[2 + i] += sub_board[i]
                        sub_board[i] = 0
            if direction == 2:
                for i in [0, 2]:
                    if (sub_board[i] == sub_board[i + 1] and sub_board[i] != 0) or (
                        sub_board[i] == 0 and sub_board[i + 1] != 0
                    ):
                        movement = True
                        sub_board[i] += sub_board[i + 1]
                        sub_board[i + 1] = 0
            if direction == 3:
                for i in [0, 2]:
                    if (sub_board[i] == sub_board[i + 1] and sub_board[i] != 0) or (
                        sub_board[i] != 0 and sub_board[i + 1] == 0
                    ):
                        movement = True
                        sub_board[i + 1] += sub_board[i]
                        sub_board[i] = 0

        if movement:
            self.spawn_tile()

        return movement

    # 0 = up, 1 = down, 2 = left, 3 = right
    def large_move(self, direction):
        movement = False

        for i in range(2):
            board_1, board_2 = None, None

            if direction == 0 or direction == 1:
                board_1 = self.board[i]
                board_2 = self.board[2 + i]
            else:
                board_1 = self.board[i * 2]
                board_2 = self.board[i * 2 + 1]

            for x in range(4):
                if direction == 0 or direction == 2:
                    if (board_1[x] == 0 and board_2[x] != 0) or (
                        board_1[x] == board_2[x] and board_1[x] != 0
                    ):
                        movement = True
                        board_1[x] += board_2[x]
                        board_2[x] = 0
                else:
                    if (board_2[x] == 0 and board_1[x] != 0) or (
                        board_1[x] == board_2[x] and board_1[x] != 0
                    ):
                        movement = True
                        board_2[x] += board_1[x]
                        board_1[x] = 0

        if movement:
            self.spawn_tile()
        return movement

    def spawn_tile(self):
        if self.is_full():
            return

        # spawn_x, spawn_y = int(random.random() * 4), int(random.random() * 4)

        # while self.board[spawn_x][spawn_y] != 0:
        #     spawn_x, spawn_y = int(random.random() * 4), int(random.random() * 4)

        options = []
        for x in range(4):
            for y in range(4):
                if not self.board[x][y]:
                    options.append((x, y))
        choice = options[int(random.random() * len(options))]

        tile_value = int(random.random() * 10)

        if tile_value >= 1:
            tile_value = 2
        else:
            tile_value = 4

        self.board[choice[0]][choice[1]] = tile_value
        self.update_game_over_status()

    def update_game_over_status(self):
        if not self.is_full():
            self.is_over = False
            return

        for i in range(4):
            board = self.board
            sub_board = board[i]

            if (
                sub_board[0] == sub_board[1]
                or sub_board[0] == sub_board[2]
                or sub_board[1] == sub_board[3]
                or sub_board[2] == sub_board[3]
            ):
                self.is_over = False
                return

            if (
                board[0][i] == board[1][i]
                or board[0][i] == board[2][i]
                or board[1][i] == board[3][i]
                or board[2][i] == board[3][i]
            ):
                self.is_over = False
                return

            self.is_over = True

    def is_full(self):
        for i in range(4):
            for x in range(4):
                if self.board[i][x] == 0:
                    return False
        return True

    def score(self):
        score = 0
        for i in range(4):
            for x in range(4):
                score += self.board[i][x]
        return score
