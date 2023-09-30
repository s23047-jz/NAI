"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/connect_four
    Mateusz Olstowski

Rules:
    https://en.wikipedia.org/wiki/Connect_Four
    variant: PopOut
"""


from classes.game import Game


def main():
    game = Game(6, 7)
    game.show_board()
    print("===============")
    game.place_piece(2, 3)
    game.show_board()


if __name__ == '__main__':
    main()
