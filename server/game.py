"""
handles operations related to game and connections
between player, board, chat and round
"""
from .player import Player
from .round import Round
from .board import Board
import random


class Game(object):
    def __init__(self, id, players):
        """
        init the game. once player threshold is met

        Arguments:
            object {[type]} -- [description]
            id {int} -- [description]
            players {Player[]} -- [description]
        """
        self.id = id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 1
        self.start_new_round()

    def start_new_round(self):
        """
        starts a new round with a new word
        """
        round_word = self.get_word()
        self.round = Round(
            round_word, self.players[self.player_draw_ind], self.players, self)
        self.player_draw_ind += 1
        self.round_count += 1

        if self.player_draw_ind >= len(self.players):
            self.end_round()
            self.end_game()

    def player_guess(self, player, guess):
        """
        Makes the player guess the word

        Arguments:
            player {[Player]} -- [description]
            guess {[str]} -- [description]
        """
        return self.round.guess(player, guess)

    def player_disconnected(self, player):
        """
        Call to clean up objects when player disconnects

        Arguments:
            player {[Player]} -- [description]
        Raises : Exception()
        """

        # TODO check this later
        if player in self.players:
            player_ind = self.players.index(player)
            if player_ind >= self.player_draw_ind:
                self.player_draw_ind -= 1
            self.players.remove(player)
            self.round.player_left(player)
        else:
            raise Exception("PLayer not in game")

        if len(self.players) <= 2:
            self.end_game()

    def get_player_scores(self):
        """give a dict of player scores.

        Returns:
            dict: [description]
        """
        scores = {player: player.get_score() for player in self.players}
        return scores

    def skip(self):
        """
        INcrements the round skips, If skips are greater than
        threshold, starts new round.

        Return: None
        """
        if self.round:
            new_round = self.round.skip()
            if new_round:
                self.round_ended()
        else:
            raise Exception("No round started yet!")

    def round_ended(self):
        """
        if the round ends call this
        Return: None
        """
        self.round.skips = 0
        self.start_new_round()
        self.board.clear()

    def update_board(self, x, y, color):
        """
        calls update method on board

        Args:
            x ([int]): [description]
            y ([int]): [description]
            color ([int, int, int]): [description]
        Return:
            None
        """
        if not self.board:
            raise Exception("No board created")
        self.board.update(x, y, color)

    def end_game(self):
        """
        ends the game
        """
        # TODO implement
        for player in self.players:
            self.round.player_left(player)

    def get_word(self):
        """
        gives a word that has not yet used
        returns str
        """
        with open("words.txt", "r") as f:
            words = []

            for line in f:
                wrd = line.strip()
                if wrd not in self.words_used:
                    words.append(wrd)

            self.words_used.add(wrd)

            r = random.randint(0, len(words)-1)
            return words[r].strip()
