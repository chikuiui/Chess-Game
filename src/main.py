import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()  # reference of game class

    def mainloop(self):

        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        # setting up py game file by looping through all the events.(like click button)
        # if user click on exit button so that we can
        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            # so when we move the piece it will show on top of our board
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # for actually clicking and moving the piece

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        # valid piece (color)
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row,motion_col)

                    if dragger.dragging:  # means we have saved a piece to drag.
                        dragger.update_mouse(event.pos)
                        # we are showing the screen and showing the pieces again because we are moving the piece
                        # so to avoid seeing multiple pieces at same time we show background and pieces.
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # check if its valid
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece, move)
                            # play sound
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()

                    dragger.undrag_piece()

                # key press to change the theme
                elif event.type == pygame.KEYDOWN:
                    # for changing theme
                    if event.key == pygame.K_t:
                        game.change_theme()
                    # for restarting game
                    if event.key == pygame.K_r:
                        game.reset()
                        # this is important in order to restart the game.
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # Quitting Application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # to update the screen.
            pygame.display.update()


# instance of main class
main = Main()
main.mainloop()
