class Square():

    ALPHACOLS ={0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}



    def __init__(self,row,column, piece = None):
        self.row = row
        self.column = column
        self.piece = piece
        try:
            self.alphacol = self.ALPHACOLS[column]
        except KeyError:
            pass
    def __eq__(self, other):
        return self.row == other.row and self.column == other.column     

    def has_piece(self):
        return self.piece != None

    def isempty(self):
        return not self.has_piece() #if a square has piece return true

    def has_team_piece(self,team):
        return self.has_piece() and self.piece.team == team

    def has_rival_piece(self,team):
        return self.has_piece() and self.piece.team != team

    def isempty_or_rival(self,color):
        return self.isempty() or self.has_rival_piece(color) 

    @staticmethod
    def in_range(*arguments):
        for arg in arguments:
            if arg<0 or arg>7:
                return False
            
        return True
   
    @staticmethod
    def get_alphacol(column):
        ALPHACOLS ={0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[column]

