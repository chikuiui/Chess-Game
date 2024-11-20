import copy

from const import *
from square import Square
from piece import *
from move import Move


# _ before methods means these methods are private.

class Board:

    def __init__(self):
        # create the list of 8 zeros for each column  COLS = 8
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(COLS)]

        self._create()
        self.last_move = None
        self._add_pieces('white')
        self._add_pieces('black')

    #  moving pieces
    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)  # we don't know until we move our piece then we check in temp board.

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece  # enemy piece
                    temp_board.calc_moves(p, row, col, bool=False)  # calculating valid moves for enemy piece.
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False

    def _create(self):
        # removing zero and adding square object.
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        # when the color is white we want pieces to be in bottom 2 rows. otherwise at top 2 rows.
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # start adding the pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # adding knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    #  calc_moves is responsible for calculating the valid move for specific piece.
    def calc_moves(self, piece, row, col, bool=True):

        def knight_moves():
            # 8 possible moves when there is no one around
            possible_moves = [
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 1, col + 2),
                (row - 1, col - 2),
                (row + 1, col - 2),
                (row + 1, col + 2)
            ]
            for move in possible_moves:
                move_row, move_col = move
                # check if possible moves are in range or not.
                if Square.in_range(move_row, move_col):
                    # check if there is piece present or not.
                    if self.squares[move_row][move_col].isempty_or_enemy(piece.color):
                        # create a squares of new move
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)

                        # move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break  # for optimization
                        else:
                            piece.add_move(move)

        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))  # exclusive ending range

            print(start)
            print(end)

            for possible_move_row in range(start, end, piece.dir):

                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal moves (only when we eat enemy piece)
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def straightline_moves(increment):
            for incr in increment:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        # create a possible new move
                        move = Move(initial, final)

                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        # has enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break

                        # has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    else:
                        break
                    # incrementing the range.
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            possible_moves = [
                (row - 1, col + 0),  # up
                (row - 1, col + 1),  # up-right
                (row + 0, col + 1),  # right
                (row + 1, col + 1),  # down-right
                (row + 1, col + 0),  # down
                (row + 1, col - 1),  # down-left
                (row + 0, col - 1),  # left
                (row - 1, col - 1)  # up-left
            ]

            # normal moves
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                # check if possible moves are in range or not.
                if Square.in_range(possible_move_row, possible_move_col):
                    # check if there is piece present or not.
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create a squares of new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):  # 4 is excluded.
                            #  castling not possible bcz there are pieces b/w them.
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook
                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) or not self.in_check(left_rook, moveR):
                                        piece.add_move(moveK)
                                        left_rook.add_move(moveR)

                                else:
                                    # append new move to king
                                    piece.add_move(moveK)
                                    left_rook.add_move(moveR)

                # king castling
                right_rook = self.squares[row][0].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):  # 4 is excluded.
                            #  castling not possible bcz there are pieces b/w them.
                            if self.squares[row][c].has_piece():
                                break
                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook
                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) or not self.in_check(right_rook, moveR):
                                        piece.add_move(moveK)
                                        right_rook.add_move(moveR)

                                else:
                                    # append new move to king
                                    piece.add_move(moveK)
                                    right_rook.add_move(moveR)

        # piece.name == 'pawn' both are same
        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),  # top-right
                (-1, -1),  # top-left
                (1, 1),  # bottom-right
                (1, -1)  # bottom-left
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),  # top
                (1, 0),  # bottom
                (0, 1),  # right
                (0, -1)  # left
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # top-right
                (-1, -1),  # top-left
                (1, 1),  # bottom-right
                (1, -1),  # bottom-left
                (-1, 0),  # top
                (1, 0),  # bottom
                (0, 1),  # right
                (0, -1)  # left
            ])

        elif isinstance(piece, King):
            king_moves()
