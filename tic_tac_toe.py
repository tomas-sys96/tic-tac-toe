import random
import time


class Player:

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.score = 0


class TicTacToe:

    def __init__(self, p1_name, p2_name):
        self.player1 = Player(p1_name, "X")
        self.player2 = Player(p2_name, "O")
        self.current_turn = None
        self.current_player = None
        self.game_board = None
        self.row_number = None
        self.column_number = None

    def new_game(self):
        # Create a blank board (underscore = empty position)
        self.game_board = []
        for i in range(3):
            row = []
            for k in range(3):
                row.append("_")
            self.game_board.append(row)
        # Reset the turn count
        self.current_turn = 1
        # Decide which player goes first
        self.current_player = random.choice([self.player1, self.player2])

    def show_game_board(self):
        # Display the game board with blank space instead of underscores
        board_to_print = []
        for row in self.game_board:
            new_row = []
            for value in row:
                if value == "_":
                    new_row.append(" ")
                else:
                    new_row.append(value)
            board_to_print.append(new_row)

        print("")
        for index_row, row in enumerate(board_to_print):
            print(" ", end="")
            print(*row, sep=" | ", end="")
            print(" ")
            if index_row != len(board_to_print) - 1:
                print((3 * len(row) + 2) * "-")
        print("")

    def players_turn(self):
        while True:
            try:
                self.row_number = int(input("Enter row's number: "))
                self.column_number = int(input("Enter column's number: "))
            except ValueError:
                print("\nNot a number, try again.")
            else:
                # Check if the row or column number is viable
                if self.row_number not in [1, 2, 3] or self.column_number not in [1, 2, 3]:
                    print("\nOff the board, try again.")
                    continue
                else:
                    self.row_number -= 1
                    self.column_number -= 1
                # Check if the selected position is empty
                # If so, place the symbol there
                if self.game_board[self.row_number][self.column_number] == "_":
                    self.place_symbol(self.current_player)
                    break
                else:
                    print("\nAlready taken, try again.")
                    continue

    def get_symbols_data(self, player):
        # For each "friendly" symbol, check if their row, column or diagonals are devoid of "unfriendly" symbols
        # If there are "unfriendly" symbols in the direction, count is 0
        # Otherwise, count equals to the number of "friendly" symbols in the direction

        if player == self.player1:
            enemy_player = self.player2
        else:
            enemy_player = self.player1

        symbols_data = {}
        symbol_number = 0
        for index_row, row in enumerate(self.game_board):
            for index_col, value in enumerate(row):
                if value == player.symbol:
                    # Position
                    position_row = index_row
                    position_col = index_col

                    # Number of symbols in the row
                    row_unfr_count = row.count(enemy_player.symbol)
                    if row_unfr_count > 0:
                        row_fr_count = 0
                    else:
                        row_fr_count = row.count(value)

                    # Number of symbols in the column
                    col_fr_count = 0
                    for row_a in self.game_board:
                        if row_a[position_col] == enemy_player.symbol:
                            col_fr_count = 0
                            break
                        elif row_a[position_col] == player.symbol:
                            col_fr_count += 1

                    # Number of symbols in the left-to-right and right-to-left diagonals
                    for col in [0, 2]:
                        if col == 0:
                            sign = 1
                            left_to_right = True
                        else:
                            sign = -1
                            left_to_right = False
                        lr_diag_count = 0
                        rl_diag_count = 0
                        for row_b in self.game_board:
                            if row_b[col] == enemy_player.symbol:
                                if left_to_right:
                                    lr_diag_count = 0
                                    break
                                else:
                                    rl_diag_count = 0
                                    break
                            elif row_b[col] == player.symbol:
                                if left_to_right:
                                    lr_diag_count += 1
                                else:
                                    rl_diag_count += 1
                            col += sign * 1

                    symbols_data[f"symbol{symbol_number}"] = {
                        "position": [position_row, position_col],
                        "count": {
                            "row": row_fr_count,
                            "col": col_fr_count,
                            "lr_diag": lr_diag_count,
                            "rl_diag": rl_diag_count
                        }
                    }

                    symbol_number += 1

        return symbols_data

    def get_random_symbol(self, computer_symbols):
        viable_symbols = []
        for symbol in computer_symbols:
            total_count = 0
            for dir_key, dir_value in computer_symbols[symbol]["count"].items():
                total_count += dir_value
            if total_count != 0:
                viable_symbols.append(symbol)
        chosen_symbol = computer_symbols[random.choice(viable_symbols)]
        return chosen_symbol

    def get_random_direction(self, chosen_symbol):
        viable_directions = []
        for dir_key, dir_value in chosen_symbol["count"].items():
            if dir_value == 1:
                viable_directions.append(dir_key)
        chosen_direction = random.choice(viable_directions)
        return chosen_direction

    def get_random_position(self, chosen_symbol, chosen_direction):
        if chosen_direction == "row":
            self.row_number = chosen_symbol["position"][0]
            self.column_number = chosen_symbol["position"][1]
            while self.game_board[self.row_number][self.column_number] != "_":
                self.column_number = random.choice(list(range(3)))
        elif chosen_direction == "col":
            self.row_number = chosen_symbol["position"][0]
            self.column_number = chosen_symbol["position"][1]
            while self.game_board[self.row_number][self.column_number] != "_":
                self.row_number = random.choice(list(range(3)))
        elif chosen_direction == "lr_diag":
            diagonal_positions = [[0, 0], [2, 2], [3, 3]]
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

    def place_symbol(self, player):
        self.game_board[self.row_number][self.column_number] = player.symbol

    def computers_turn(self):
        # If going first, pick a random position to place the symbol at
        if self.current_turn in [1, 2]:
            while True:
                self.row_number = random.choice(list(range(3)))
                self.column_number = random.choice(list(range(3)))
                if self.game_board[self.row_number][self.column_number] == "_":
                    break
                else:
                    pass
        else:
            player_symbols = self.get_symbols_data(self.player1)
            computer_symbols = self.get_symbols_data(self.player2)
            chosen_symbol = None
            chosen_direction = None
            # Check if the computer is only one step away from winning
            # If not, look out for an imminent threat that the enemy player's symbols' placement poses
            for symbols_data in [computer_symbols, player_symbols]:
                for symbol in symbols_data:
                    for dir_key, dir_value in symbols_data[symbol]["count"].items():
                        if dir_value == 2:
                            chosen_symbol = symbols_data[symbol]
                            chosen_direction = dir_key
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            # If none of the above-mentioned scenarios occur, pick a random symbol
            if chosen_symbol is None:
                chosen_symbol = self.get_random_symbol(computer_symbols)
                chosen_direction = self.get_random_direction(chosen_symbol)
            # Pick a random position in the chosen direction
            self.get_random_position(chosen_symbol, chosen_direction)

        # Place a symbol
        print("Computer is thinking...")
        time.sleep(2)
        self.place_symbol(self.current_player)

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
