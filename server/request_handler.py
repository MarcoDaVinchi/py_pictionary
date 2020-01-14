"""
MAIN THREAD
Handles all of the connections, creating new games and
requests from the client(s).
"""
import socket
import threading
from .player import Player
from .game import Game
from queue import Queue


def player_thread(conn, ip, name):
    pass


def authentication(conn, addr):
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

        threading.Thread(target=player_thread, args=(conn, addr, name))
    except Exception as e:
        print("[EXCEPTION]", e)
        conn.close()


def connection_thread():

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

        authentication(conn, addr)


if __name__ == "__main__":
    threading.Thread(target=connection_thread())
