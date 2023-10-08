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


def create_players_opponent():
    """
    :return:
    Returns selected bot as a player
    """
    bot_level = int(input("Input level of bot's depth: "))
    bot_type = ''
    while bot_type not in ['sss', 'neg']:
        bot_type = input("Select bot type, 'sss' or 'neg': ")
        if bot_type == 'sss':
            sss_ai = SSS(bot_level)
            player_2 = AI_Player(sss_ai)
        elif bot_type == 'neg':
            neg_ai = Negamax(bot_level)
            player_2 = AI_Player(neg_ai)

    return player_2


def main():
    player_choice = ''
    while (player_choice == '' or player_choice not in ['player', 'ai']):
        player_choice = input(
            "Please select game type, 'player' to play against AI, or 'ai' to watch game between two AIs: "
        )

    if player_choice == 'player':
        player_1 = Human_Player()
        player_2 = create_players_opponent()
    elif player_choice == 'ai':
        neg_ai = Negamax(5)
        sss_ai = SSS(5)
        player_1 = AI_Player(neg_ai)
        player_2 = AI_Player(sss_ai)

    game = Game([player_1, player_2])
    game.play()
    if game.lose():
        print("Player %d wins." % (game.opponent_index))
    else:
        print("Looks like we have a draw.")


if __name__ == '__main__':
    main()
