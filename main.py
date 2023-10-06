"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/connect_four
    Mateusz Olstowski

Rules:
    https://en.wikipedia.org/wiki/Connect_Four
    variant: PopOut
"""

from easyAI import AI_Player, Human_Player, Negamax, SSS

from classes.game import Game


def main():
    player_choice = ''
    available_choice = ['player', 'ai']
    while (player_choice == '' or player_choice not in available_choice):
        player_choice = input("Please select game type, 'player' to play against AI, or 'ai' to watch game between two AIs: ")

    neg_ai = Negamax(5)
    sss_ai = SSS(5)

    if player_choice == 'player':
        player_1 = Human_Player
        player_2 = AI_Player(neg_ai)
    elif player_choice == 'ai':
        player_1 = AI_Player(neg_ai)
        player_2 = AI_Player(sss_ai)

    game = Game([player_1, player_2])
    game.show()
    game.play()
    if game.lose():
        print("Player %d wins." % (game.opponent_index))
    else:
        print("Looks like we have a draw.")


if __name__ == '__main__':
    main()
