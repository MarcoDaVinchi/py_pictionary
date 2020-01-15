"""
MAIN THREAD
Handles all of the connections, creating new games and
requests from the client(s).
"""
import socket
import threading
from .player import Player
from .game import Game
import json


class Server(object):
    PLAYERS = 8

    def __init__(self):
        self.connection_queue = []
        self.game_id = 0

    def player_thread(self, conn, player):
        """handles in game communication between clients

        Args:
            conn (object): connection object
            ip (str): [description]
            name (str): [description]
        """
        while True:
            try:
                # Receive request
                data = conn.recv(1024)
                data = json.loads(data)

                # PLayer is not apart of game
                keys = [key for key in data.keys()]
                send_msg = {key: [] for key in keys}
                for key in keys:
                    if key == -1:  # get game, returns a list of players
                        if player.game:
                            send_msg[-1] = player.game.players
                        else:
                            send_msg[-1] = []
                    if player.game:
                        if key == 0:  # guess
                            correct = player.game.player_guess(
                                player, data[0][0])
                            send_msg[0] = [correct]
                        elif key == 1:  # skip
                            pass
                        elif key == 2:  # get chat
                            pass
                        elif key == 3:  # get board
                            pass
                        elif key == 4:  # get score
                            pass
                        elif key == 5:  # get round
                            pass
                        elif key == 6:  # get word
                            pass
                        elif key == 7:  # get skips
                            pass
                        elif key == 8:  # update board
                            pass
                        elif key == 9:  # get round time
                            pass
                        else:
                            raise Exception("Not a valid request")

                conn.sendall(json.dumps(send_msg))

            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()} disconnected:", e)
                conn.close()
                # TODO call player game disconnect method

    def handle_queue(self, player):
        """adds player to queue and creates new game if enough players

        Args:
            player (object): [description]
        """
        self.connection_queue.append(player)
        if len(self.connection_queue) >= 8:
            game = Game(self.connection_queue[:], self.game_id)

            for p in self.connection_queue:
                p.set_game(game)

            self.game_id += 1
            self.connection_queue = []

    def authentication(self, conn, addr):
        """authentication here

        Args:
            ip (str): [description]
        """
        try:
            data = conn.recv(16)
            name = str(data.decode())
            if not name:
                raise Exception("No name received")
            conn.sendall("1".encode())

            player = Player(addr, name)
            self.handle_queue(player)
            threading.Thread(target=self.player_thread,
                             args=(conn, addr, name))
        except Exception as e:
            print("[EXCEPTION]", e)
            conn.close()

    def connection_thread(self):

        server = ""
        port = 5555
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen()
        print("Waiting for a connection, Server Started")

        while True:
            conn, addr = s.accept()
            print("[CONNECT] New connection!")

            self.authentication(conn, addr)


if __name__ == "__main__":
    s = Server()
    threading.Thread(target=s.connection_thread)
