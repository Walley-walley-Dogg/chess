from Square import *
from const import *
from piece import *
from Move import Move
from sound import Sound
import os
import copy
class Board():
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0,] for column in range(8)]    
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self,piece,move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.column].isempty()

        #console board move update
        self.squares[initial.row][initial.column].piece = None
        self.squares[final.row][final.column].piece = piece

        
        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.column - initial.column
            if diff != 0 and en_passant_empty:
                #console board move update
                self.squares[initial.row][initial.column + diff].piece = None
                self.squares[final.row][final.column].piece = piece
                if not testing:
                    sound = Sound(os.path.join('alpha/sounds/capture_sound.wav'))
                    sound.play()
            
            else:
                # повышение пешек
                self.check_promotion(piece, final)

        #рокировка
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.column - initial.column
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        #move
        piece.moved = True

        #clear valid moves
        piece.clear_moves()

        #set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.column].piece = Queen(piece.team)

    def castling(self, initial, final):
        return abs(initial.column - final.column) == 2


    def set_true_en_passant(self, piece):
        
        if not isinstance(piece,Pawn):
            return

        for row in range(ROWS):
            for col in range(COLUMNS):
                if isinstance (self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False

        piece.en_passant = True


        

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move,testing=True)

        for row in range(ROWS):
            for col in range(COLUMNS):
                if temp_board.squares[row][col].has_rival_piece(piece.team):
                    p = temp_board.squares[row][col].piece # p = piece
                    temp_board.calc_moves(p,row,col, bool = False)
                    for m in p.moves: # m = move
                        if isinstance(m.final.piece, King):
                            return True

        return False

    def calc_moves(self, piece, row, column, bool = True):
        '''
            просчитывает возможные движения определенной фигуры на определенной позиции
        '''
        
        def pawn_moves():
            #ходы пешки
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir*(1+steps))
            for possible_move_row in range(start,end,piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][column].isempty():
                        # create initial and final squares
                        initial = Square(row,column)
                        final = Square(possible_move_row,column)
                        #create new move
                        move = Move(initial,final)

                        #check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                        else: 
                            #append new move
                            piece.add_move(move)
                    #если клетка перед пешкой заблокирована
                    else: break
                #не в диапозоне
                else: break
            
            #diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [column-1,column+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.team):
                        # create initial and final squares
                        initial = Square(row,column)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row,possible_move_col, final_piece)
                        #create new move
                        move = Move(initial,final)
                        
                        #check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                        else: 
                            #append new move
                            piece.add_move(move)

            # en passant moves
            r = 3 if piece.team == 'white' else 4
            fr = 2 if piece.team == 'white' else 5
            # left en passant
            if Square.in_range(column-1) and row == r:
                if self.squares[row][column-1].has_rival_piece(piece.team):
                    p = self.squares[row][column-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final squares
                            initial = Square(row,column)
                            final = Square(fr,column-1, p)
                            #create new move
                            move = Move(initial,final)
                            
                            #check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)
                            else: 
                                #append new move
                                piece.add_move(move)
            # right en passant
            if Square.in_range(column+1) and row == r:
                if self.squares[row][column+1].has_rival_piece(piece.team):
                    p = self.squares[row][column+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final squares
                            initial = Square(row,column)
                            final = Square(fr,column+1, p)
                            #create new move
                            move = Move(initial,final)
                            
                            #check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)
                            else: 
                                #append new move
                                piece.add_move(move)



        def knight_moves():
            # если конь стоит в центре, то у него будет 8 возможных движений
            possible_moves = [
                (row-2,column+1),
                (row+2,column+1),
                (row-1,column+2),
                (row+1,column+2),
                (row+2,column-1),
                (row+1,column-2),
                (row-1,column-2),
                (row-2,column-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_column = possible_move
                
                if Square.in_range(possible_move_row,possible_move_column):
                    if self.squares[possible_move_row][possible_move_column].isempty_or_rival(piece.team):
                        #создание клеток для движения фигуры
                        initial = Square(row,column)
                        final_piece = self.squares[possible_move_row][possible_move_column].piece
                        final = Square(possible_move_row,possible_move_column, final_piece) #PIECE = PIECE
                        # создание нового движения
                        move = Move(initial, final)
                        
                        #check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                            else: break
                        else: 
                            #append new move
                            piece.add_move(move)

        def straightline_moves(increments):
            for increment in increments:
                row_inc, col_inc = increment
                possible_move_row = row + row_inc
                possible_move_col = column + col_inc

                while True:
                    if Square.in_range(possible_move_row,possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row,column)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row,possible_move_col, final_piece)
                        #create possible new move
                        move = Move(initial,final)
                        
                        # empty = go on looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)
                            else: 
                                #append new move
                                piece.add_move(move)

                        # has rival piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.team):
                            #check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)
                            else: 
                                #append new move
                                piece.add_move(move)
                            break

                        # has team mate = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.team):
                            break                      

                    #not in range
                    else: break

                    # incrementing incs
                    possible_move_row = possible_move_row + row_inc
                    possible_move_col = possible_move_col + col_inc

        def king_moves():
            adjs = [
                (row-1,column+0), #up
                (row+1,column+0), #down
                (row+0,column+1), #right
                (row+0,column-1), #left
                (row-1,column+1), #up-right
                (row-1,column-1), #up-left
                (row+1,column+1), #down-right
                (row+1,column-1) #down-left
            ]  

            #normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.team):
                        #создание клеток для движения фигуры
                        initial = Square(row,column)
                        final = Square(possible_move_row,possible_move_col) #PIECE = PIECE
                        # создание нового движения
                        move = Move(initial, final)
                        #check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                            else: break
                        else: 
                            #append new move
                            piece.add_move(move)

            #castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4): # c - column
                            if self.squares[row][c].has_piece(): # castling is impossible
                                break

                            if c == 3:
                                piece.left_rook = left_rook

                                #rook move
                                initial = Square(row,0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                #king move
                                initial = Square(row,column)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                #check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        #append new move to king
                                        piece.add_move(moveK)
                                else: 
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    #append new move king
                                    piece.add_move(moveK)



                #king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5,7): # c - column
                            if self.squares[row][c].has_piece(): # castling is impossible
                                break

                            if c == 6:
                                piece.right_rook = right_rook

                                #rook move
                                initial = Square(row,7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                

                                #king move
                                initial = Square(row,column)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                #check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        #append new move to king
                                        piece.add_move(moveK)
                                else: 
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    #append new move king
                                    piece.add_move(moveK)

        if isinstance(piece,Pawn): 
            pawn_moves()
        
        elif isinstance(piece,Knight): 
            knight_moves()
        
        elif isinstance(piece,Queen): 
            straightline_moves([
                (-1,1), #вверх и направо
                (-1,-1), #вверх и налево
                (1,1), # вниз и направо
                (1,-1), # вниз и налево
                (-1,0), # up
                (1,0), #down
                (0,-1), #right
                (0,1) #left
            ])
        
        elif isinstance(piece,Bishop): 
            straightline_moves([
                (-1,1), #вверх и направо
                (-1,-1), #вверх и налево
                (1,1), # вниз и направо
                (1,-1) # вниз и налево
            ])

        elif isinstance(piece,Rook) : 
            straightline_moves([
                (-1,0), # up
                (1,0), #down
                (0,-1), #right
                (0,1) #left
            ])
        
        elif isinstance(piece,King): 
            king_moves()
    
    def _create(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.squares[row][column] = Square(row,column)
    
    def _add_pieces(self,team):
        
        row_pawn, row_behind = (6,7) if team == 'white' else (1,0)
        
        #pawns
        for column in range(8):
            self.squares[row_pawn][column] = Square(row_pawn, column, Pawn(team))
        
        #knights
        self.squares[row_behind][1] = Square(row_behind, 1, Knight(team))
        self.squares[row_behind][6] = Square(row_behind, 6, Knight(team))
        
        #bishops
        self.squares[row_behind][2] = Square(row_behind, 2, Bishop(team))
        self.squares[row_behind][5] = Square(row_behind, 5, Bishop(team))  
          
        
        #rooks
        self.squares[row_behind][0] = Square(row_behind, 0, Rook(team))
        self.squares[row_behind][7] = Square(row_behind, 7, Rook(team))

        #king
        self.squares[row_behind][4] = Square(row_behind, 4, King(team))
        
        #queen
        self.squares[row_behind][3] = Square(row_behind, 3, Queen(team))