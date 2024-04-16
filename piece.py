import pygame
import os 
class Piece():
    
    def __init__(self,type,team,value,image=None, image_rect=None):
        self.team = team
        self.type = type
        self.image = image
        self.set_image()
        self.image_rect = image_rect
        self.value = value
        self.moves = []
        self.moved = False
    
    def set_image(self):
        self.image = os.path.join( f'alpha/{self.team}_{self.type}.png')
    
    def add_move(self,move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Piece):
    
    def __init__(self,team):
        self.dir =-1 if team == 'white' else 1
        self.en_passant = False
        super().__init__('pawn', team, 1) 

class Knight(Piece):
    
    def __init__(self,team):
        super().__init__('knight', team, 3)
    
class Bishop(Piece):
    
    def __init__(self,team):
        super().__init__('bishop', team, 3)

class Rook(Piece):
    
    def __init__(self,team):
        super().__init__('rook', team, 5)

class King(Piece):
    
    def __init__(self,team):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', team, 10000)

class Queen(Piece):
    
    def __init__(self,team):
        super().__init__('Queen', team, 9)   