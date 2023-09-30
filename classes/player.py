class Player:
    def __init__(self, name: str, coins: int):
        self.name: str = name
        self.coins: int = coins

    def _remove_coin(self):
        self.coins -= 1

    def has_player_coins(self):
        return self.coins > 0

    def get_player_name(self):
        return self.name

    def get_number_of_coins(self):
        return self.coins
