import random

from player import Player


class TicTacToe:
    def __init__(self):
        self.current_turn = None
        self.current_player = None
        self.board = None

    def start_new_game(self, player1: Player, player2: Player):
        self.reset_board()
        self.current_turn = 1
        self.current_player = random.choice([player1, player2])

    def reset_board(self):
        self.board = []
        for _ in range(3):
            row = []
            for _ in range(3):
                row.append(" ")
            self.board.append(row)

    def show_board(self):
        print("")
        for row_index, row in enumerate(self.board):
            print(" ", end="")
            print(*row, sep=" | ", end="")
            print(" ")
            if row_index != len(self.board) - 1:
                print(11 * "-")
        print("")

    def place_symbol(self, row_number: int, column_number: int):
        self.board[row_number][column_number] = self.current_player.symbol

    def is_win(self, chosen_row: int, chosen_column: int) -> bool:
        if self.is_row_complete(chosen_row) or self.is_column_complete(chosen_column) or \
                self.is_diagonal_complete(True) or self.is_diagonal_complete(False):
            return True

    def is_row_complete(self, chosen_row: int) -> bool:
        row_count = 0
        for value in self.board[chosen_row]:
            if value == self.current_player.symbol:
                row_count += 1

        if row_count == 3:
            return True

    def is_column_complete(self, chosen_column: int) -> bool:
        column_count = 0
        for row in self.board:
            if row[chosen_column] == self.current_player.symbol:
                column_count += 1

        if column_count == 3:
            return True

    def is_diagonal_complete(self, left_to_right: bool) -> bool:
        sign = 1 if left_to_right else -1
        column = 0 if left_to_right else 2
        diagonal_count = 0
        for row in self.board:
            if row[column] == self.current_player.symbol:
                diagonal_count += 1
            column += sign
        if diagonal_count == 3:
            return True

    def is_draw(self) -> bool:
        empty_squares = 0
        for row in self.board:
            empty_squares += row.count(" ")
        if empty_squares == 0:
            return True

    def next_turn(self, player1: Player, player2: Player):
        if self.current_player == player1:
            self.current_player = player2
        else:
            self.current_player = player1
        self.current_turn += 1

