class Move:

    def __init__(self,initial,final):
        # Изначальная и финальня позиция это клетки, а не тюльпаны
        self.initial = initial
        self.final = final
        
        # eq = equality
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final