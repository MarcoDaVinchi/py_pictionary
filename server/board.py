"""
State of drawing board.
"""


class Board(object):
    ROWS = COLS = 720

    def __init__(self):
        """Init the board by creating empty board (all white pixels)
        """
        self.data = self._create_empty_board()

    def update(self, x, y, color):
        """
        Updates a singular pixel of the board

        Args:
            x (int): [description]
            y (int): [description]
            color (int, int, int): [description]
        """
        self.data[y][x] = color

    def clear(self):
        """clears the board to all white
        """
        self.data = self._create_empty_board()

    def _create_empty_board(self):
        """creates an empty board (all white)

        Returns:
            [type]: [description]
        """
        return [[(255, 255, 255) for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def fill(self, x, y):
        """fills in a specific shape or area using recursion

        Args:
            x (int): [description]
            y (int): [description]
        """
        pass

    def get_board(self):
        """gets the data of the board

        Returns:
            int, int, int: [description]
        """
        return self.data
