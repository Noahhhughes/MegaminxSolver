class Side:

    def __init__(self, bigColor):
        self.bigColor = bigColor
        self.neighborColor = [None] * 5
        self.nodeVal = [[None] * 3 for i in range(10)]
        self.oppColor = ""


    def set_bigColor(self, bigColor):
        self.bigColor = bigColor

    def set_oppColor(self, oppColor):
        self.oppColor = oppColor

    def set_neighborColor(self, neighborColor):
        self.neighborColor = neighborColor

    def set_nodeVal(self, nodeVal):
        self.nodeVal = nodeVal
