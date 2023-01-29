from abc import ABC, abstractmethod
import random
import time

from direction_picker import DirectionPicker
from directions_count import DirectionsCount
from diagonal_symbols_count import DiagonalSymbolsCount


class Player(ABC):
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.score = 0

    @abstractmethod
    def make_move(self, game, player1, player2) -> tuple:
        pass


class HumanPlayer(Player):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)

    def make_move(self, game, player1: Player, player2: Player) -> tuple:
        while True:
            row_number, column_number = self._enter_position()
            if self._is_position_number(row_number, column_number):
                row_number = int(row_number) - 1
                column_number = int(column_number) - 1
            else:
                continue

            if self._is_position_on_board(row_number, column_number):
                pass
            else:
                continue

            if self._is_position_empty(game, row_number, column_number):
                break

        game.place_symbol(row_number, column_number)
        return row_number, column_number

    @staticmethod
    def _enter_position() -> tuple:
        row_number = input("Enter the row's number: ")
        column_number = input("Enter the column's number: ")
        return row_number, column_number

    @staticmethod
    def _is_position_number(row_number: str, column_number: str) -> bool:
        try:
            int(row_number)
            int(column_number)
        except ValueError:
            print("\nNot a number, try again.")
            return False
        else:
            return True

    @staticmethod
    def _is_position_on_board(row_number: int, column_number: int) -> bool:
        if row_number not in [0, 1, 2] or column_number not in [0, 1, 2]:
            print("\nOff the board, try again.")
            return False
        else:
            return True

    @staticmethod
    def _is_position_empty(game, row_number: int, column_number: int) -> bool:
        if not game.board[row_number][column_number] == " ":
            print("\nAlready taken, try again.")
            return False
        else:
            return True


class ComputerPlayer(Player):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)

    def make_move(self, game, player1: Player, player2: Player) -> tuple:
        friendly_symbols = self._get_symbols_data(game, player1, player2, True)
        enemy_symbols = self._get_symbols_data(game, player1, player2, False)

        direction_picker = DirectionPicker({}, "")

        # If the friendly player is close to win, place the final symbol to complete a streak
        # If the enemy player is close to win, spoil it for them
        if self._is_close_to_win(friendly_symbols, enemy_symbols, direction_picker):
            row_number, column_number = self._get_next_position(game, direction_picker.chosen_symbol,
                                                                direction_picker.chosen_direction)
        elif (not friendly_symbols and not enemy_symbols) or (not self._is_any_viable_direction(friendly_symbols)
                                                              and not self._is_any_viable_direction(enemy_symbols)):
            # If going first or if there's no way to win, pick a random empty square to place the symbol
            row_number, column_number = self._get_random_empty_position(game)
        elif friendly_symbols and self._is_any_viable_direction(friendly_symbols):
            # Place a symbol based upon the position of an already existing friendly symbol, if there are any
            # viable directions
            direction_picker.get_viable_position(friendly_symbols)
            row_number, column_number = self._get_next_position(game, direction_picker.chosen_symbol,
                                                                direction_picker.chosen_direction)
        else:
            # If going second, there are no friendly symbols data available at the start of the turn
            # -> try clause gives an error
            # Therefore, place a symbol based upon the position of the enemy symbol
            direction_picker.get_viable_position(enemy_symbols)
            row_number, column_number = self._get_next_position(game, direction_picker.chosen_symbol,
                                                                direction_picker.chosen_direction)

        print("Computer is thinking...")
        time.sleep(2)
        game.place_symbol(row_number, column_number)
        return row_number, column_number

    def _get_symbols_data(self, game, player1: Player, player2: Player, friendly_player: bool) -> dict:
        player = self._choose_friendly_player(game, friendly_player, player1, player2)
        enemy_player = self._choose_enemy_player(player, player1, player2)

        symbols_data = {}
        symbol_number = 0
        for row_index, row in enumerate(game.board):
            for column_index, value in enumerate(row):
                if value == player.symbol:
                    symbols_data = self._update_symbols_data(game, symbols_data, symbol_number, row_index, column_index,
                                                             player, enemy_player)
                    symbol_number += 1
        return symbols_data

    @staticmethod
    def _choose_friendly_player(game, friendly_player: bool, player1: Player, player2: Player) -> Player:
        if friendly_player:
            player = game.current_player
        else:
            if game.current_player == player1:
                player = player2
            else:
                player = player1
        return player

    @staticmethod
    def _choose_enemy_player(player: Player, player1: Player, player2: Player) -> Player:
        if player == player1:
            enemy_player = player2
        else:
            enemy_player = player1
        return enemy_player

    def _update_symbols_data(self, game, symbols_data: dict, symbol_number: int, row_index: int, column_index: int,
                             player: Player, enemy_player: Player) -> dict:
        current_position_data = self._get_data_for_position(game, row_index, column_index, player, enemy_player)
        symbols_data[symbol_number] = {
            "position": (row_index, column_index),
            "count": {
                "row": current_position_data.row_symbols_count,
                "column": current_position_data.column_symbols_count,
                "left_to_right_diagonal": current_position_data.left_to_right_diagonal_symbols_count,
                "right_to_left_diagonal": current_position_data.right_to_left_diagonal_symbols_count
            }
        }
        return symbols_data

    def _get_data_for_position(self, game, row_index: int, column_index: int, player: Player, enemy_player: Player) \
            -> DirectionsCount:
        directions_count = DirectionsCount(0, 0, 0, 0)
        directions_count.row_symbols_count = self._get_row_symbols_count(game, row_index, player, enemy_player)
        directions_count.column_symbols_count = self._get_column_symbols_count(game, column_index, player, enemy_player)
        directions_count.left_to_right_diagonal_symbols_count = self._get_diagonal_symbols_count(game, True, player,
                                                                                                 enemy_player)
        directions_count.right_to_left_diagonal_symbols_count = self._get_diagonal_symbols_count(game, False, player,
                                                                                                 enemy_player)
        return directions_count

    @staticmethod
    def _get_row_symbols_count(game, row_index: int, player: Player, enemy_player: Player) -> int:
        row_enemy_symbols_count = game.board[row_index].count(enemy_player.symbol)
        if row_enemy_symbols_count > 0:
            row_symbols_count = 0
        else:
            row_symbols_count = game.board[row_index].count(player.symbol)
        return row_symbols_count

    @staticmethod
    def _get_column_symbols_count(game, column_index: int, player: Player, enemy_player: Player) -> int:
        column_symbols_count = 0
        for row in game.board:
            if row[column_index] == enemy_player.symbol:
                column_symbols_count = 0
                break
            elif row[column_index] == player.symbol:
                column_symbols_count += 1
        return column_symbols_count

    @staticmethod
    def _get_diagonal_symbols_count(game, left_to_right: bool, player: Player, enemy_player: Player) -> int:
        sign = 1 if left_to_right else -1
        column = 0 if left_to_right else 2
        diagonal_symbols_count = DiagonalSymbolsCount(0, 0)
        for row in game.board:
            if row[column] == enemy_player.symbol:
                diagonal_symbols_count.reset_count(left_to_right)
                break
            elif row[column] == player.symbol:
                diagonal_symbols_count.increase_count(left_to_right)
            column += sign
        if left_to_right:
            return diagonal_symbols_count.left_to_right
        else:
            return diagonal_symbols_count.right_to_left

    @staticmethod
    def _get_next_position(game, chosen_symbol: dict, chosen_direction: str) -> tuple:
        row_number, column_number = chosen_symbol["position"]
        if chosen_direction == "row":
            while game.board[row_number][column_number] != " ":
                column_number = random.choice(list(range(3)))
        elif chosen_direction == "column":
            while game.board[row_number][column_number] != " ":
                row_number = random.choice(list(range(3)))
        elif chosen_direction == "left_to_right_diagonal":
            while game.board[row_number][column_number] != " ":
                diagonal_positions = [[0, 0], [1, 1], [2, 2]]
                chosen_position = random.choice(diagonal_positions)
                row_number = chosen_position[0]
                column_number = chosen_position[1]
        else:
            while game.board[row_number][column_number] != " ":
                diagonal_positions = [[0, 2], [1, 1], [2, 0]]
                chosen_position = random.choice(diagonal_positions)
                row_number = chosen_position[0]
                column_number = chosen_position[1]
        return row_number, column_number

    @staticmethod
    def _is_close_to_win(friendly_symbols: dict, enemy_symbols: dict, direction_picker: DirectionPicker) -> bool:
        for symbols_data in [friendly_symbols, enemy_symbols]:
            for symbol in symbols_data:
                for direction_name, direction_value in symbols_data[symbol]["count"].items():
                    if direction_value == 2:
                        direction_picker.chosen_symbol = symbols_data[symbol]
                        direction_picker.chosen_direction = direction_name
                        return True
        return False

    @staticmethod
    def _is_any_viable_direction(symbols_data: dict) -> bool:
        for symbol in symbols_data:
            for direction_value in symbols_data[symbol]["count"].values():
                if direction_value != 0:
                    return True
        return False

    @staticmethod
    def _get_random_empty_position(game) -> tuple:
        empty_positions = []
        for row_index, row in enumerate(game.board):
            for column_index, value in enumerate(row):
                if value == " ":
                    empty_positions.append((row_index, column_index))
        return random.choice(empty_positions)
