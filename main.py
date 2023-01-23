import random
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod
from pprint import pprint
import subprocess


logo = """
╔════╗          ╔════╗             ╔════╗        
║╔╗╔╗║          ║╔╗╔╗║             ║╔╗╔╗║        
╚╝║║╚╝╔╗╔══╗    ╚╝║║╚╝╔══╗ ╔══╗    ╚╝║║╚╝╔══╗╔══╗
  ║║  ╠╣║╔═╝      ║║  ╚ ╗║ ║╔═╝      ║║  ║╔╗║║╔╗║
 ╔╝╚╗ ║║║╚═╗     ╔╝╚╗ ║╚╝╚╗║╚═╗     ╔╝╚╗ ║╚╝║║║═╣
 ╚══╝ ╚╝╚══╝     ╚══╝ ╚═══╝╚══╝     ╚══╝ ╚══╝╚══╝
"""


@dataclass
class Player:
    name: str
    symbol: str
    score: int = 0


class TicTacToe:
    def __init__(self, p1_name, p2_name):
        self.player1 = Player(p1_name, "X")
        self.player2 = Player(p2_name, "O")
        self.current_turn = None
        self.current_player = None
        self.game_board = None
        self.row_number = None
        self.column_number = None

    def start_new_game(self):
        self.create_game_board()
        self.current_turn = 1
        self.current_player = random.choice([self.player1, self.player2])

    def create_game_board(self):
        # Create a blank game board (underscore = empty position)
        self.game_board = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append("_")
            self.game_board.append(row)

    def _modify_game_board(self) -> list:
        # Display the game board with blank spaces instead of underscores
        modified_game_board = []
        for row in self.game_board:
            new_row = []
            for value in row:
                if value == "_":
                    new_row.append(" ")
                else:
                    new_row.append(value)
            modified_game_board.append(new_row)
        return modified_game_board

    def show_game_board(self):
        modified_game_board = self._modify_game_board()
        print("")
        for row_index, row in enumerate(modified_game_board):
            print(" ", end="")
            print(*row, sep=" | ", end="")
            print(" ")
            if row_index != len(modified_game_board) - 1:
                print(11 * "-")
        print("")

    def players_turn(self):
        while True:
            self._enter_position()
            if self._is_position_available():
                self.place_symbol(self.current_player)
                break

    def _enter_position(self):
        self.row_number = input("Enter row's number (1-3): ")
        self.column_number = input("Enter column's number (1-3): ")

    def _is_position_available(self) -> bool:
        if not self._is_position_number() or not self._is_position_on_board():
            return False
        else:
            self.row_number -= 1
            self.column_number -= 1
            if not self._is_position_empty():
                return False
            else:
                return True

    def _is_position_number(self) -> bool:
        try:
            self.row_number = int(self.row_number)
            self.column_number = int(self.column_number)
        except ValueError:
            print("\nNot a number, try again.")
            return False
        else:
            return True

    def _is_position_on_board(self) -> bool:
        if self.row_number not in [1, 2, 3] or self.column_number not in [1, 2, 3]:
            print("\nOff the board, try again.")
            return False
        else:
            return True

    def _is_position_empty(self) -> bool:
        if not self.game_board[self.row_number][self.column_number] == "_":
            print("\nAlready taken, try again.")
            return False
        else:
            return True

    def get_symbols_data(self, player: Player) -> dict:
        # For each "enemy" symbol, check if their row, column or diagonals are devoid of "enemy" symbols
        # If there are any "enemy" symbols in the direction, the count is 0
        # Otherwise, the count equals to the number of "friendly" symbols in that specific direction

        enemy_player = self.determine_enemy_player(player)
        symbols_data = {}
        symbol_number = 0
        for row_index, row in enumerate(self.game_board):
            for column_index, value in enumerate(row):
                if value == player.symbol:
                    symbols_data = self.update_symbols_data(symbols_data, symbol_number, row_index, row, column_index, value, player, enemy_player)
                    symbol_number += 1
        return symbols_data

    def determine_enemy_player(self, player: Player) -> Player:
        if player == self.player1:
            enemy_player = self.player2
        else:
            enemy_player = self.player1
        return enemy_player

    def update_symbols_data(self, symbols_data: dict, symbol_number: int, row_index: int, row: list, column_index: int, value: str, player: Player, enemy_player: Player) -> dict:
        current_position_data = self.get_data_for_position(row, column_index, value, player, enemy_player)
        symbols_data[symbol_number] = {
            "position": (row_index, column_index),
            "count": {
                "row": current_position_data.row_symbols_count,
                "column": current_position_data.column_symbols_count,
                "left_to_right_diag": current_position_data.left_to_right_diag_symbols_count,
                "right_to_left_diag": current_position_data.right_to_left_diag_symbols_count
            }
        }
        return symbols_data

    @dataclass
    class DirectionsCount:
        row_symbols_count: int
        column_symbols_count: int
        left_to_right_diag_symbols_count: int
        right_to_left_diag_symbols_count: int

    def get_data_for_position(self, row: list, column_index: int, value: str, player: Player, enemy_player: Player) -> DirectionsCount:
        directions_count = self.DirectionsCount(0, 0, 0, 0)
        directions_count.row_symbols_count = self.get_row_symbols_count(row, value, enemy_player)
        directions_count.column_symbols_count = self.get_column_symbols_count(column_index, player, enemy_player)
        directions_count.left_to_right_diag_symbols_count = self.get_diagonal_symbols_count(True, player, enemy_player)
        directions_count.right_to_left_diag_symbols_count = self.get_diagonal_symbols_count(False, player, enemy_player)
        return directions_count

    def get_row_symbols_count(self, row: list, value: str, enemy_player: Player) -> int:
        row_enemy_symbols_count = row.count(enemy_player.symbol)
        if row_enemy_symbols_count > 0:
            row_symbols_count = 0
        else:
            row_symbols_count = row.count(value)
        return row_symbols_count

    def get_column_symbols_count(self, column_index: int, player: Player, enemy_player: Player) -> int:
        column_symbols_count = 0
        for row in self.game_board:
            if row[column_index] == enemy_player.symbol:
                column_symbols_count = 0
                break
            elif row[column_index] == player.symbol:
                column_symbols_count += 1
        return column_symbols_count

    @dataclass
    class DiagonalSymbolsCount:
        left_to_right: int
        right_to_left: int

        def reset_count(self, left_to_right: bool):
            if left_to_right:
                self.left_to_right = 0
            else:
                self.right_to_left = 0

        def increase_count(self, left_to_right: bool):
            if left_to_right:
                self.left_to_right += 1
            else:
                self.right_to_left += 1

    def get_diagonal_symbols_count(self, left_to_right: bool, player: Player, enemy_player: Player) -> int:
        sign = 1 if left_to_right else -1
        column = 0 if left_to_right else 2
        diagonal_symbols_count = self.DiagonalSymbolsCount(0, 0)
        for row in self.game_board:
            if row[column] == enemy_player.symbol:
                diagonal_symbols_count.reset_count(left_to_right)
                break
            elif row[column] == player.symbol:
                diagonal_symbols_count.increase_count(left_to_right)
            column += sign * 1
        if left_to_right:
            return diagonal_symbols_count.left_to_right
        else:
            return diagonal_symbols_count.right_to_left

    def get_random_position(self, chosen_symbol: dict, chosen_direction: str):
        if chosen_direction == "row":
            self.row_number = chosen_symbol["position"][0]
            self.column_number = chosen_symbol["position"][1]
            while self.game_board[self.row_number][self.column_number] != "_":
                self.column_number = random.choice(list(range(3)))
        elif chosen_direction == "column":
            self.row_number = chosen_symbol["position"][0]
            self.column_number = chosen_symbol["position"][1]
            while self.game_board[self.row_number][self.column_number] != "_":
                self.row_number = random.choice(list(range(3)))
        elif chosen_direction == "left_to_right_diag":
            diagonal_positions = [[0, 0], [1, 1], [2, 2]]
            self.row_number = chosen_symbol["position"][0]
            self.column_number = chosen_symbol["position"][1]
            while self.game_board[self.row_number][self.column_number] != "_":
                chosen_position = random.choice(diagonal_positions)
                self.row_number = chosen_position[0]
                self.column_number = chosen_position[1]
        else:
            diagonal_positions = [[0, 2], [2, 2], [2, 0]]
            self.row_number = chosen_symbol["position"][0]
            self.column_number = chosen_symbol["position"][1]
            while self.game_board[self.row_number][self.column_number] != "_":
                chosen_position = random.choice(diagonal_positions)
                self.row_number = chosen_position[0]
                self.column_number = chosen_position[1]

    def place_symbol(self, player: Player):
        self.game_board[self.row_number][self.column_number] = player.symbol

    @dataclass
    class DirectionPicker:
        chosen_symbol: dict
        chosen_direction: str

        def pick_random_symbol(self, computer_symbols: dict):
            random_key = random.choice(list(computer_symbols.keys()))
            self.chosen_symbol = computer_symbols[random_key]

        def pick_random_direction(self):
            viable_directions = []
            for direction_name, direction_value in self.chosen_symbol["count"].items():
                if direction_value != 0:
                    viable_directions.append(direction_name)
            self.chosen_direction = random.choice(viable_directions)

    def computers_turn(self):
        # If going first, pick a random position to place the symbol at
        if self.current_turn in [1, 2]:
            self.pick_first_position()
        else:
            human_symbols = self.get_symbols_data(self.player1)
            computer_symbols = self.get_symbols_data(self.player2)

            # Check if the computer is only one step away from winning
            # If not, look out for an imminent threat that the enemy player's symbols' placement poses
            direction_picker = self.DirectionPicker({}, "")
            if self.is_anyone_close_to_win(computer_symbols, human_symbols, direction_picker):
                pass
            else:
                direction_picker.pick_random_symbol(computer_symbols)
                direction_picker.pick_random_direction()
            # Pick a random position in the chosen direction
            self.get_random_position(direction_picker.chosen_symbol, direction_picker.chosen_direction)

        # Place a symbol
        print("Computer is thinking...")
        time.sleep(2)
        self.place_symbol(self.current_player)

    def pick_first_position(self):
        while True:
            self.row_number = random.choice(list(range(3)))
            self.column_number = random.choice(list(range(3)))
            if self.game_board[self.row_number][self.column_number] == "_":
                break

    def is_anyone_close_to_win(self, computer_symbols: dict, human_symbols: dict, direction_picker: DirectionPicker) -> bool:
        for symbols_data in [computer_symbols, human_symbols]:
            for symbol in symbols_data:
                for direction_name, direction_value in symbols_data[symbol]["count"].items():
                    if direction_value == 2:
                        direction_picker.chosen_symbol = symbols_data[symbol]
                        direction_picker.chosen_direction = direction_name
                        print(direction_picker.chosen_direction)
                        return True
        return False

    def is_win(self):
        # Horizontal check
        for row in self.game_board:
            horizontal_count = row.count(self.current_player.symbol)
            if horizontal_count == 3:
                return True

        # Vertical check
        vertical_count = {}
        for row in self.game_board:
            for index, value in enumerate(row):
                try:
                    vertical_count[f"column{index}_count"]
                except KeyError:
                    vertical_count[f"column{index}_count"] = 0
                finally:
                    if value == self.current_player.symbol:
                        vertical_count[f"column{index}_count"] += 1
        for column in vertical_count:
            if vertical_count[column] == 3:
                return True

        # Diagonal check
        for column in [0, 2]:
            if column == 0:
                sign = 1
            else:
                sign = -1
            diagonal_count = 0
            for row in self.game_board:
                if row[column] == self.current_player.symbol:
                    diagonal_count += 1
                column += sign * 1
            if diagonal_count == 3:
                return True

    def is_draw(self):
        empty_squares = 0
        for row in self.game_board:
            empty_squares += row.count("_")
        if empty_squares == 0:
            return True

    def next_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        self.current_turn += 1


print(logo)


def select_game_mode() -> str:
    while True:
        friend_or_computer = input("Type (f) to play with a friend,\n"
                                   "or type (c) to play against the computer.\n").lower()
        if friend_or_computer in ["f", "c"]:
            return friend_or_computer


def is_against_computer(chosen_game_mode: str) -> bool:
    if chosen_game_mode == "f":
        return False
    else:
        return True


def enter_name(description: str) -> str:
    name = input(description).capitalize()
    return name


def show_each_players_symbol(game: TicTacToe):
    print(f"\n{game.player1.name} uses '{game.player1.symbol}' as their symbol.")
    print(f"{game.player2.name} uses '{game.player2.symbol}' as their symbol.")


if __name__ == "__main__":
    selected_game_mode = select_game_mode()
    versus_computer = is_against_computer(selected_game_mode)
    if not versus_computer:
        player1_name = enter_name("First player's name: ")
        player2_name = enter_name("Second player's name: ")
    else:
        player1_name = enter_name("Your name: ")
        player2_name = "Computer"

    tic_tac_toe = TicTacToe(player1_name, player2_name)

    tic_tac_toe.start_new_game()
    show_each_players_symbol(tic_tac_toe)
    tic_tac_toe.show_game_board()

    is_game_over = False
    while not is_game_over:
        print(f"{tic_tac_toe.current_player.name}'s turn.")

        if versus_computer:
            if tic_tac_toe.current_player == tic_tac_toe.player1:
                tic_tac_toe.players_turn()
            else:
                tic_tac_toe.computers_turn()
        else:
            tic_tac_toe.players_turn()

        tic_tac_toe.show_game_board()

        draw = False
        win = False
        if tic_tac_toe.is_win():
            print(f"{tic_tac_toe.current_player.name} wins!")
            tic_tac_toe.current_player.score += 1
            win = True
        elif tic_tac_toe.is_draw():
            print(f"It's a draw!")
            draw = True

        if draw or win:
            print(f"\n{tic_tac_toe.player1.name}: {tic_tac_toe.player1.score}")
            print(f"{tic_tac_toe.player2.name}: {tic_tac_toe.player2.score}\n")
            another_game = input("Would you like to play again? Yes (y) or no (n). ").lower()
            while True:
                if another_game == "y":
                    tic_tac_toe.start_new_game()
                    break
                elif another_game == "n":
                    is_game_over = True
                    break
        else:
            tic_tac_toe.next_turn()
