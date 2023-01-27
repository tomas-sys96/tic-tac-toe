from game import TicTacToe
from player import Player, HumanPlayer, ComputerPlayer


logo = """
╔════╗          ╔════╗             ╔════╗        
║╔╗╔╗║          ║╔╗╔╗║             ║╔╗╔╗║        
╚╝║║╚╝╔╗╔══╗    ╚╝║║╚╝╔══╗ ╔══╗    ╚╝║║╚╝╔══╗╔══╗
  ║║  ╠╣║╔═╝      ║║  ╚ ╗║ ║╔═╝      ║║  ║╔╗║║╔╗║
 ╔╝╚╗ ║║║╚═╗     ╔╝╚╗ ║╚╝╚╗║╚═╗     ╔╝╚╗ ║╚╝║║║═╣
 ╚══╝ ╚╝╚══╝     ╚══╝ ╚═══╝╚══╝     ╚══╝ ╚══╝╚══╝
"""


def select_game_mode() -> str:
    while True:
        friend_or_computer = input("Type (f) to play with a friend, or\n"
                                   "type (c) to play against the computer.\n").lower()
        if friend_or_computer in ["f", "c"]:
            return friend_or_computer


def instantiate_players(chosen_game_mode: str):
    if chosen_game_mode == "c":
        player1_name = enter_name("Your name: ")
        player2 = ComputerPlayer("Computer", "O")
    else:
        player1_name = enter_name("First player's name: ")
        player2_name = enter_name("Second player's name: ")
        player2 = HumanPlayer(player2_name, "O")
    player1 = HumanPlayer(player1_name, "X")
    return player1, player2


def enter_name(description: str) -> str:
    name = input(description)
    return name


def show_symbol_affiliation(player1: Player, player2: Player):
    print(f"\n{player1.name} uses '{player1.symbol}' as their symbol.")
    print(f"{player2.name} uses '{player2.symbol}' as their symbol.")


def show_current_score(player1: Player, player2: Player):
    print(f"\n{player1.name}: {player1.score}")
    print(f"{player2.name}: {player2.score}\n")


def main():
    print(logo)
    selected_game_mode = select_game_mode()
    player1, player2 = instantiate_players(selected_game_mode)
    show_symbol_affiliation(player1, player2)

    game = TicTacToe()
    game.start_new_game(player1, player2)
    game.show_board()

    is_game_over = False
    while not is_game_over:
        print(f"{game.current_player.name}'s turn.")
        chosen_row, chosen_column = game.current_player.make_move(game, player1, player2)
        game.show_board()

        turn_win = False
        turn_draw = False
        if game.is_win(chosen_row, chosen_column):
            print(f"{game.current_player.name} wins!")
            game.current_player.score += 1
            turn_win = True
        elif game.is_draw():
            print("It's a draw!")
            turn_draw = True

        if turn_win or turn_draw:
            show_current_score(player1, player2)
            while True:
                another_game = input("Would you like to play another round? Type yes (y) or no (n). ").lower()
                if another_game == "y":
                    game.start_new_game(player1, player2)
                    break
                elif another_game == "n":
                    is_game_over = True
                    break
        else:
            game.next_turn(player1, player2)


if __name__ == "__main__":
    main()
