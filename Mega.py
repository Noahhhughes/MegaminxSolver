class Mega:

    def __init__(self,):
        self.sides = [None] * 12
        self.depth = 0
        self.heuristicVal = 0
        self.priority = 0

    def set_megaNum(self, megaNum):
        self.megaNum = megaNum

    def set_depth(self, depth):
        self.depth = depth

    def set_heuristicVal(self, heuristicVal):
        self.heuristicVal = heuristicVal

    def set_sides(self, sides):
        self.sides = sides

    def set_priority(self, priority):
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
