class ConnectionLine(list):
    def __init__(self):
        self.referencePoint = []
        self.finishingPoint = []

    def newConnection(self, referencePoint, finishingPoint):
        self.append(referencePoint, finishingPoint)

    def remConnection(self, referencePoint, finishingPoint):
        self.pop(referencePoint, finishingPoint)
