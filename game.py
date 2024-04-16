import pygame
from const import *
from Board import Board
from Dragger import Dragger
from configuration import Config
from Square import Square
class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
    
    #blit methods
    
    def show_bg(self,surface):
        theme = self.config.theme


        for row in range(ROWS):
            for column in range(COLUMNS):
                # color
                color = theme.bg.light  if (row+column) % 2 == 0 else theme.bg.dark
                # rect
                rect = (column * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if column == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(f'{ROWS - row}', 1, color)
                    lbl_pos = (5,5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row+column) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(column), 1, color)
                    lbl_pos = (column * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)


    def show_pieces(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.board.squares[row][column].has_piece():
                    piece = self.board.squares[row][column].piece
                      
                    if piece is not self.dragger.piece:  
                        img = pygame.image.load(piece.image)
                        img_center = column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.image_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.image_rect)

    def show_moves(self,surface):

        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                #color
                color = theme.moves.light if (move.final.row + move.final.column) % 2 == 0 else theme.moves.dark
                #rect
                rect =(move.final.column * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE) #оси х и у соответственно
                #blit 
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                #color
                color = theme.trace.light if (pos.row + pos.column) % 2 == 0 else theme.trace.dark
                #rect
                rect = (pos.column * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                #blit 
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            #color
            color = (180,180,180)
            #rect
            rect = (self.hovered_sqr.column * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            #blit 
            pygame.draw.rect(surface, color, rect, width = 3)


    # other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, column):
        try:
            self.hovered_sqr = self.board.squares[row][column]
        except IndexError:
            pass

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured = False):
        if captured:
            self.config.capt_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()