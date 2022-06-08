import numpy as np
import openseespy.opensees as ops
from math import asin, sqrt, sin, cos, atan


class OutRiggerSystem(object):

    def __init__(self, model, complete=False, ULS=False, reduction=True):
        self._numFloor = model.getNumFloor()
        self._numBay = model.getNumBays()
        self._L_bay = model.getL_bay()
        self._floor_h = model.getFloor_h()
        self._element = model._element
        self._eleTag = 6001
        self._grid = model._grid
        self._model = model
        self._zerolinkElementTag = model._zerolinkElementTag
        self._outrigger = model._outrigger
        self._complete = complete
        self._ULS = ULS
        self._reduction = reduction

        self._angle = atan(self._floor_h / self._L_bay)

        self._length = (self._floor_h ** 2 + (self._L_bay) ** 2) ** 0.5

        self._Kaxd = model._element._Kaxd

        E_GL30c = model._element.getE_beam()

        Ad = model._element.getAt()

        Diagonal_stiffness = ((E_GL30c * Ad) / self._length) / 1000

        Equv_stiffness_SLS = (1 / self._Kaxd + 1 / Diagonal_stiffness + 1 / self._Kaxd) ** -1
        self._Reduction_diagonal_SLS = Equv_stiffness_SLS / Diagonal_stiffness

        Equv_stiffness_ULS = (1 / ((2 / 3) * self._Kaxd) + 1 / Diagonal_stiffness + 1 / ((2 / 3) * self._Kaxd)) ** -1
        self._Reduction_diagonal_ULS = Equv_stiffness_ULS / Diagonal_stiffness

        if (self._ULS):
            if (self._reduction):
                self._reductionFactor = self._Reduction_diagonal_ULS
            else:
                self._reductionFactor = 1
        else:
            if (self._reduction):
                self._reductionFactor = self._Reduction_diagonal_SLS
            else:
                self._reductionFactor = 1
        self._diagonal_stiffness = self._reductionFactor*Diagonal_stiffness

        self._addedFloors = []
        self._addedBays = []
        self._nodesUsed = []
        self._nodesUsedZeroLink = []

        factor = 1
        E_Hor = factor * 164000  # [N/mm]
        E_Ver = factor * 164000  # [N/mm]
        E_Along = factor * 268243  # [N/mm]

        ops.uniaxialMaterial('Elastic', 1001, E_Hor)
        ops.uniaxialMaterial('Elastic', 1002, E_Ver)
        ops.uniaxialMaterial('Elastic', 1003, E_Along)

        self._reductionFactor = 1
        self._system = 1
        self._forceElements = {}
        self._forceElements["beams"] = {}
        self._forceElements["columns"] = {}
        self._forceElements["ORelements"] = {}
        self._forceElements["walls"] = {}

    def getDiagonalStiffness(self):
        return self._diagonal_stiffness


    def addDoublicantPoints(self, nodeTag, orientation):
        # Add doublicant points to allow for zero link elements
        start = nodeTag - 3000
        floor = np.floor(start / (self._numBay + 1)) + 1

        if start % (self._numBay + 1):
            xLoc = ((start % (self._numBay + 1)) - 1) * self._L_bay
            yLoc = self._floor_h * (floor - 1)
        else:
            xLoc = self._L_bay * self._numBay
            yLoc = self._floor_h * (floor - 2)

        if (start in self._grid["left"]):
            ops.node(nodeTag, xLoc, yLoc)
            ops.equalDOF(int(start), int(nodeTag), 1, 2)


        elif (start in self._grid["right"]):
            ops.node(nodeTag, xLoc, yLoc)
            ops.equalDOF(int(start), int(nodeTag), 1, 2)


        else:
            if (orientation == "L"):
                ops.node(int(str(int(nodeTag)) + str(1)), xLoc, yLoc)
                ops.equalDOF(int(start), int(str(int(nodeTag)) + str(1)), 1, 2)

            if (orientation == "R"):
                ops.node(int(str(int(nodeTag)) + str(2)), xLoc, yLoc)
                ops.equalDOF(int(start), int(str(int(int(nodeTag))) + str(2)), 1, 2)




    def setHorizontalOutrigger(self, numbFloor):
        flip = True

        self._addedFloors.append(numbFloor)

        if (numbFloor <= self._numFloor):
            startPos = (self._numBay + 1) * (numbFloor - 1) + 1
        else:
            print("illegal floor address")
            return

        startPos += 3000
        transfTag = 1
        releaseClause = ('-release', 3)
        for i in range(1, self._numBay + 1):
            bay = (i)

            if (flip):
                if i == 1:
                    end1 = int(startPos)
                    if (end1 not in self._nodesUsed):
                        self.addDoublicantPoints(end1, "R")
                        self._nodesUsed.append(end1)

                    end2 = int(str(int(startPos) + (self._numBay + 2)) + str(1))
                    if (end2 not in self._nodesUsed):
                        self.addDoublicantPoints(startPos + (self._numBay + 2), "L")
                        self._nodesUsed.append(end2)

                    if ((bay in self._addedBays and numbFloor in self._addedFloors) == False):
                        ops.element('ElasticTimoshenkoBeam', self._eleTag, end1, end2, self._element.getE_beam(),
                                    self._element.getG_beam(), self._element.getAt() * self._reductionFactor,
                                    self._element.getIt(), self._element.getAty(), transfTag)

                        self._forceElements["ORelements"][str(self._eleTag)] = []

                    self._eleTag = self._eleTag + 1
                    startPos += 1

                elif i == self._numBay:
                    end1 = int(str(int(startPos)) + str(2))
                    if (end1 not in self._nodesUsed):
                        self.addDoublicantPoints(startPos, "R")
                        self._nodesUsed.append(end1)

                    end2 = int(startPos) + (self._numBay + 2)
                    if (end2 not in self._nodesUsed):
                        self.addDoublicantPoints(end2, "L")
                        self._nodesUsed.append(end2)

                    if ((bay in self._addedBays and numbFloor in self._addedFloors) == False):
                        ops.element('ElasticTimoshenkoBeam', self._eleTag, end1, end2, self._element.getE_beam(),
                                    self._element.getG_beam(), self._element.getAt() * self._reductionFactor,
                                    self._element.getIt(), self._element.getAty(), transfTag)

                        self._forceElements["ORelements"][str(self._eleTag)] = []

                    self._eleTag = self._eleTag + 1

                else:
                    end1 = int(str(int(startPos)) + str(2))
                    if (end1 not in self._nodesUsed):
                        self.addDoublicantPoints(startPos, "R")
                        self._nodesUsed.append(end1)

                    end2 = int(str(int(startPos) + (self._numBay + 2)) + str(1))
                    if (end2 not in self._nodesUsed):
                        self.addDoublicantPoints(startPos + (self._numBay + 2), "L")
                        self._nodesUsed.append(end2)

                    if ((bay in self._addedBays and numbFloor in self._addedFloors) == False):
                        ops.element('ElasticTimoshenkoBeam', self._eleTag, end1, end2, self._element.getE_beam(),
                                    self._element.getG_beam(), self._element.getAt() * self._reductionFactor,
                                    self._element.getIt(), self._element.getAty(), transfTag)

                        self._forceElements["ORelements"][str(self._eleTag)] = []

                    self._eleTag = self._eleTag + 1
                    startPos += 1

        if (self._complete):
            self.findAllBeamsColumns()
        else:
            self.findBeamsColums(numbFloor)

        # self.setBeamConnections()



    def findBeamsColums(self, numbFloor):

        columns = [((1000 + numbFloor) + i * (self._numFloor)) for i in range(self._numBay + 1)]

        if (self._outrigger):
            if (self._numBay + 1) < 5:
                if (self._numBay + 1) % 2 == 0:
                    columnNr1 = int((self._numBay + 1) / 2)
                    columnNr2 = int((self._numBay + 1) / 2) - 1
                else:
                    columnNr1 = int((self._numBay + 1) / 2)
                    columnNr2 = columnNr1
            else:
                if (self._numBay + 1) % 2 == 0:
                    columnNr1 = int((self._numBay + 1) / 2)
                    columnNr2 = int((self._numBay + 1) / 2) - 1
                else:
                    columnNr1 = int((self._numBay + 1) / 2) - 1
                    columnNr2 = int((self._numBay + 1) / 2) + 1

            for i, column in enumerate(columns):
                if i == 0 or i == self._numBay:
                    if (self._outrigger):
                        self._forceElements["columns"][str(column)] = []
                    else:
                        self._forceElements["walls"][str(column)] = []

                else:
                    if ((i == columnNr2 or i == columnNr1) and self._outrigger):
                        self._forceElements["walls"][str(column)] = []
                    else:
                        self._forceElements["columns"][str(column)] = []

        else:
            for i, column in enumerate(columns):
                if i == 0 or i == self._numBay:
                    self._forceElements["walls"][str(column)] = []
                else:
                    self._forceElements["columns"][str(column)] = []

        if (numbFloor <= self._numFloor):
            startPos = (self._numBay + 1) * (numbFloor - 1) + 1
        else:
            print("illegal floor address")
            return

        floor = np.floor(startPos / (self._numBay + 1)) + 1

        startBeam = int((floor - 2) * self._numBay + 2001)

        beams = [(startBeam + i) for i in range(self._numBay)]

        for beam in beams:
            self._forceElements["beams"][str(beam)] = []



    def findAllBeamsColumns(self):
        if (self._numBay + 1) < 5:
            if (self._numBay + 1) % 2 == 0:
                columnNr1 = int((self._numBay + 1) / 2)
                columnNr2 = int((self._numBay + 1) / 2) - 1
            else:
                columnNr1 = int((self._numBay + 1) / 2)
                columnNr2 = columnNr1
        else:
            if (self._numBay + 1) % 2 == 0:
                columnNr1 = int((self._numBay + 1) / 2)
                columnNr2 = int((self._numBay + 1) / 2) - 1
            else:
                columnNr1 = int((self._numBay + 1) / 2) - 1
                columnNr2 = int((self._numBay + 1) / 2) + 1

        eleTag = 1001
        for j in range(0, self._numBay + 1):
            for i in range(0, self._numFloor):
                if j == 0 or j == self._numBay:
                    if (self._outrigger):
                        self._forceElements["columns"][str(eleTag)] = []
                    else:
                        self._forceElements["walls"][str(eleTag)] = []

                else:
                    if ((i == columnNr2 or i == columnNr1) and self._outrigger):
                        self._forceElements["walls"][str(eleTag)] = []
                    else:
                        self._forceElements["columns"][str(eleTag)] = []

                eleTag = eleTag + 1

        eleTag = 2001
        for j in range(1, self._numFloor + 1):
            for i in range(1, self._numBay + 1):
                if i == 1:
                    self._forceElements["beams"][str(eleTag)] = []
                    eleTag = eleTag + 1

                elif i == self._numBay:
                    self._forceElements["beams"][str(eleTag)] = []
                    eleTag = eleTag + 1

                else:
                    self._forceElements["beams"][str(eleTag)] = []
                    eleTag = eleTag + 1

    def setVerticalOutrigger(self, bayNumber):
        self._addedBays.append(bayNumber)

        if (bayNumber <= self._numBay):
            startPos = (self._numBay + 1) + bayNumber
        else:
            print("illegal bay address")
            return

        startPos += 3000
        transfTag = 1
        releaseClause = ('-release', 3)
        for i in range(1, self._numFloor):
            floor = (i + 1)

            if (startPos - 3000 in self._grid["left"]):
                end1 = int(startPos)
                if (end1 not in self._nodesUsed):
                    self.addDoublicantPoints(end1, "R")
                    self._nodesUsed.append(end1)

                end2 = int(str(startPos + (self._numBay + 2)) + str(1))
                if (end2 not in self._nodesUsed):
                    self.addDoublicantPoints(int(startPos) + (self._numBay + 2), "L")
                    self._nodesUsed.append(end2)

                if ((floor in self._addedFloors and bayNumber in self._addedBays) == False):
                    ops.element('ElasticTimoshenkoBeam', self._eleTag, end1, end2, self._element.getE_beam(),
                                self._element.getG_beam(), self._element.getAb() * self._reductionFactor,
                                self._element.getIb(), self._element.getAby(), transfTag)

                self._eleTag = self._eleTag + 1
                startPos += (self._numBay + 1)


            elif ((startPos - 3000 + 1) in self._grid["right"]):
                end1 = int(str(int(startPos)) + str(2))
                if (end1 not in self._nodesUsed):
                    self.addDoublicantPoints(int(startPos), "R")
                    self._nodesUsed.append(end1)

                end2 = int(startPos) + (self._numBay + 2)
                if (end2 not in self._nodesUsed):
                    self.addDoublicantPoints(end2, "L")
                    self._nodesUsed.append(end2)

                if ((floor in self._addedFloors and bayNumber in self._addedBays) == False):
                    ops.element('ElasticTimoshenkoBeam', self._eleTag, end1, end2, self._element.getE_beam(),
                                self._element.getG_beam(), self._element.getAb() * self._reductionFactor,
                                self._element.getIb(), self._element.getAby(), transfTag)

                self._eleTag = self._eleTag + 1
                startPos += (self._numBay + 1)

            else:
                end1 = int(str(int(startPos)) + str(2))
                if (end1 not in self._nodesUsed):
                    self.addDoublicantPoints(int(startPos), "R")
                    self._nodesUsed.append(end1)

                end2 = int(str(int(startPos) + (self._numBay + 2)) + str(1))
                if (end2 not in self._nodesUsed):
                    self.addDoublicantPoints(int(startPos) + (self._numBay + 2), "L")
                    self._nodesUsed.append(end2)

                if ((floor in self._addedFloors and bayNumber in self._addedBays) == False):
                    ops.element('ElasticTimoshenkoBeam', self._eleTag, end1, end2, self._element.getE_beam(),
                                self._element.getG_beam(), self._element.getAb() * self._reductionFactor,
                                self._element.getIb(), self._element.getAby(), transfTag)

                self._eleTag = self._eleTag + 1
                startPos += (self._numBay + 1)

        self.setBeamConnections()


    def setBeamConnections(self):
        nodes = []
        for node in self._nodesUsed:
            if node not in self._nodesUsedZeroLink:
                self._nodesUsedZeroLink.append(node)
                nodes.append(node)

        for nodeTag in nodes:
            strNodeTag = str(nodeTag)
            if len(strNodeTag) == 5:
                strNodeTag2 = strNodeTag[:-1]
                end = strNodeTag[4]
            else:
                strNodeTag2 = strNodeTag[:]

            nodeTag = int(strNodeTag)

            start = int(strNodeTag2) - 3000

            if (start in self._grid["left"]):
                end1 = nodeTag
                end2 = start
                # ops.fix(end1, 1, 1, 0)
                ops.element('zeroLength', self._zerolinkElementTag, int(end1), int(end2), '-mat', 1001, 1002, '-dir', 1,
                            2)

                self._zerolinkElementTag = self._zerolinkElementTag + 1


            elif (start in self._grid["right"]):
                end1 = nodeTag
                end2 = start
                # ops.fix(end1, 1, 1, 0)
                ops.element('zeroLength', self._zerolinkElementTag, int(end1), int(end2), '-mat', 1001, 1002, '-dir', 1,
                            2)

                self._zerolinkElementTag = self._zerolinkElementTag + 1


            else:

                if (end == "1"):
                    end1 = nodeTag
                    end2 = start
                    # ops.fix(end1, 1, 1, 0)
                    ops.element('zeroLength', self._zerolinkElementTag, int(end1), int(end2), '-mat', 1001, 1002,
                                '-dir', 1, 2)

                    self._zerolinkElementTag = self._zerolinkElementTag + 1

                if (end == "2"):
                    end1 = nodeTag
                    end2 = start
                    # ops.fix(end1, 1, 1, 0)
                    ops.element('zeroLength', self._zerolinkElementTag, int(end1), int(end2), '-mat', 1001, 1002,
                                '-dir', 1, 2)

                    self._zerolinkElementTag = self._zerolinkElementTag + 1


