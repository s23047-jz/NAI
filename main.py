from classes.game import Game


def main():
    game = Game(6, 7)
    game.show_board()
    print("===============")
    game.place_piece(2, 3)
    game.show_board()


if __name__ == '__main__':
    main()
