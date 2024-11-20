# Responsible for rendering the game.
import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square


class Game:
    def __init__(self):
        self.config = Config()
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()

    # show methods

    def show_bg(self, surface):

        theme = self.config.active_theme

        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # drawing a rectangle
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)  # tuple [ x-axis,y-axis,width,height]
                pygame.draw.rect(surface, color, rect)  # drawing rectangle on screen

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(str(ROWS-row), 1, color)
                    label_pos = (5, 5 + row * SQSIZE)
                    # blit
                    surface.blit(label, label_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(Square.get_alphacol(col), 1, color)
                    label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(label, label_pos)

    # Rendering for show-pieces
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # check if there is piece present or not.
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except dragger piece.
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)

                        img = pygame.image.load(piece.texture)
                        # to center the image vertically and horizontally on the board
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.active_theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark  # color
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)  # rect
                pygame.draw.rect(surface, color, rect)  # blit

    def show_last_move(self, surface):
        theme = self.config.active_theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark  # color
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)  # rect
                pygame.draw.rect(surface, color, rect)  # blit

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)  # color
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)  # rect
            pygame.draw.rect(surface, color, rect, width=3)  # blit

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
