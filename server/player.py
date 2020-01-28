"""
Player object on the server
"""
from game import Game


class Player(object):
    def __init__(self, ip, name):
        """init the player object

        Args:
            object (object): [description]
            ip (str): [description]
            name (str): [description]
        """
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0

    def set_game(self, game):
        """sets the players game association

        Args:
            game ([type]): [description]
        """
        self.game = game

    def update_score(self, x):
        """updates a players score

        Args:
            x (int): [description]
        """
        self.score += x

    def guess(self, wrd):
        """Makes a player guess

        Args:
            wrd ([str]): [description]
        return: bool
        """
        return self.game.player_guess(self, wrd)

    def disconnect(self):
        """call to disconnect player
        """
        self.game.player_disconnected(self)

    def get_ip(self):
        """Gets player ip address

        Returns:
            [str]: [description]
        """
        return self.ip

    def get_name(self):
        """Get player name

        Returns:
            str: [description]
        """
        return self.name

    def get_score(self):
        """get player score

        Returns:
            int: [description]
        """
        return self.score
