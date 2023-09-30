class Player:
    def __init__(self, name: str, coins: int):
        self.name = name
        self.coins = coins

    def _remove_coin(self):
        self.coins -= 1

    def has_player_coins(self) -> bool:
        return self.coins > 0

    def get_player_name(self):
        return self.name

    def get_number_of_coins(self):
        return self.coins

    def move(self, row: int):
        if not self.coins == 0:
            return
