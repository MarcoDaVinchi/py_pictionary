"""
Represents a round of the game.
"""
import time as t
from _thread import start_new_thread
from .game import Game
from .chat import Chat


class Round(object):
    def __init__(self, word, player_drawing, players, game):
        """[summary]
        init object
        Arguments:
            object {[type]} -- [description]
            word {[str]} -- [description]
            player_drawing {[object]} -- [Player]
            players {[list]} -- [Player[]]
        """
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.skips = 0
        self.player_scores = {player: 0 for player in players}
        self.time = 75
        self.game = game
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())

    def skip(self):
        """
        Returns true if round skipped threshold met

        Returns:
            [bool]: [description]
        """
        self.skips += 1
        if self.skips > len(self.players) - 2:
            self.skips = 0
            return True

        return False

    def get_scores(self):
        """Returns all the player scores

        Returns:
            [type]: [description]
        """
        return self.scores

    def get_score(self, player):
        """Gets a specific players scores

        Args:
            player ([type]): [description]

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception("Player not in score list")

    def time_thread(self):
        """
        Runs in thread to keep track of time
        """
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round("Time is up!")

    def guess(self, player, wrd):
        """[summary]
        returns bool if player gut guess correctly
        Arguments:
            player {[type]} -- [description]
            wrd {[str]} -- [description]

        Returns:
            [bool] -- [description]
        """
        correct = wrd == self.word
        if correct:
            self.player_guessed.append(player)
            # TODO implement scoring system here

    def player_left(self, player):
        """
        removes player that left from scores and list

        Arguments:
            player {[object]} -- [Player object]
        """

        # might not be able to use player as key
        if player in self.player_scores:
            del self.player_scores[player]
        if player in self.player_guessed:
            self.player_guessed.remove(player)
        if player == self.player_drawing:
            self.end_round("Drawing player leaves")

    def end_round(self, msg):
        # TODO implement end_round functionality
        self.game.round_ended()
