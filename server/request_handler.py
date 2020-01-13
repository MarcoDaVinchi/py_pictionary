"""
MAIN THREAD
Handles all of the connections, creating new games and
requests from the client(s).
"""
import socket
from _thread import *
import time
from .player import Player
from .game import Game
from queue import Queue