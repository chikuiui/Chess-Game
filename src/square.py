class Square:
    ALHPACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    # not all square are going to have piece.
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.ALHPACOL = self.ALHPACOLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece is not None

    # static method can be direcly called using class name without creating the object of it.
    @staticmethod
    def in_range(*args):  # *args -> means list of arguments
        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True

    # check whether the piece is present or not
    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    @staticmethod
    def get_alphacol(col):
        ALHPACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALHPACOLS[col]