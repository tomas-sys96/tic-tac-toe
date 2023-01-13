from tic_tac_toe import TicTacToe
from ascii_art import logo


print(logo)

versus_ai = None
player1_name = ""
player2_name = ""

while True:
    friend_or_ai = input("Type (f) to play with a friend,\n"
                         "or type (c) to play against the computer.\n").lower()
    if friend_or_ai == "f":
        player1_name = input("First player's name: ").title()
        player2_name = input("Second player's name: ").title()
        versus_ai = False
        break
    elif friend_or_ai == "c":
        player1_name = input("Your name: ").title()
        player2_name = "Computer"
        versus_ai = True
        break

tic_tac_toe = TicTacToe(player1_name, player2_name)

# Start a new game
tic_tac_toe.new_game()

print(f"\n{tic_tac_toe.player1.name} uses '{tic_tac_toe.player1.symbol}' as their symbol.")
print(f"{tic_tac_toe.player2.name} uses '{tic_tac_toe.player2.symbol}' as their symbol.")

tic_tac_toe.show_game_board()

is_game_over = False
while not is_game_over:
    print(f"{tic_tac_toe.current_player.name}'s turn.")

    if versus_ai:
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
                tic_tac_toe.new_game()
                break
            elif another_game == "n":
                is_game_over = True
                break
    else:
        tic_tac_toe.next_turn()
