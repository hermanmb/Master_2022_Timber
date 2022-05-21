import openseespy.opensees as ops
from math import asin, sqrt
import openseespy.postprocessing.Get_Rendering as opsplt


class Model(object):

    def __init__(self,simulation,numBay,numFloor,floor_h,spacing, L_bay,Loads,StandardElement,pinned,outrigger = False):

        self._numBay = numBay
        self._numFloor = numFloor
        self._L_bay = L_bay
        self._floor_h = floor_h
        self._loads = Loads
        self._element = StandardElement
        self._spacing = spacing
        self._loads.setLoadings(self._floor_h, self._L_bay, self._spacing)
        self._grid = {}
        self._grid["left"] = []
        self._grid["midle"] = []
        self._grid["right"] = []
        self._zerolinkElementTag = 3001
        self._eigenVector = []
        self._outrigger = outrigger
        self._beams = []

        hc = StandardElement.getHc()
        hw = StandardElement.getHw()


        if (outrigger):
            StandardElement.setHw(hc)
        self._columfactor = hw/hc


        ops.model('basic', '-ndm', 2, '-ndf', 3)

        ops.geomTransf(simulation, 1)

        self._Q = 0
        self._Mass = 0
        self._Mass_x = 0
        self._Freq = []
        self._numEigen = 3

        self.setRotationalStiffness()

        # Setting grids
        self.addMainGrid()
        self.addOffsetGrid()
        self.addDoublicantPoints()
        self.addRotationalStiffnessPointsAtBase()

        # Setting Beams and Columns
        self.addColumnsAndWalls()
        self.addBeams()
        approximationValue = 100
        self.addRigidZones(approximationValue)

        # Setting Connectiones
        self.setBeamConnections()

        #ops.fix(1, 1, 1, 1)
        #ops.fix(2, 1, 1, 0)
        #ops.fix(3, 1, 1, 0)

        if (pinned):
            self.setColumnConnectionsPinned()

        else:
            self.setColumnConnectionsFixed()


        # Creating Loads
        self.loadCalculations()
        self.massCalculation()




    def plotModel(self):
        opsplt.plot_model("nodes", "elements")
        #opsplt.plot_model("nodes")
        #opsplt.plot_model("elements")
        #opsplt.plot_model()


    def addMainGrid(self):
        # Main grid
        yLoc = 0.
        nodeTag = 1
        for j in range(0, self._numFloor + 1):
            xLoc = 0.
            for i in range(0, self._numBay + 1):
                if i == 0:
                    self._grid["left"].append(nodeTag)
                elif i == self._numBay:
                    self._grid["right"].append(nodeTag)
                else:
                    self._grid["midle"].append(nodeTag)

                ops.node(nodeTag, xLoc, yLoc)
                xLoc = xLoc + self._L_bay
                nodeTag = nodeTag + 1

            yLoc = yLoc + self._floor_h



    def addOffsetGrid(self):
        # Add offsets to allow for rigid zone
        yLoc = self._floor_h
        nodeTag = 1001 + self._numBay + 1
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

        for j in range(0, self._numFloor):
            xLoc = 0.

            for i in range(0, self._numBay + 1):

                if i == 0:
                    ops.node(nodeTag, xLoc + self._element.getHw() / 2, yLoc)
                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1

                elif i == self._numBay:
                    ops.node(nodeTag, xLoc - self._element.getHw() / 2, yLoc)
                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1

                else:
                    if ((i == columnNr2 or i == columnNr1) and self._outrigger):
                        ops.node(int(str(nodeTag) + str(1)), xLoc - self._element.getHc()*self._columfactor / 2, yLoc)
                        ops.node(int(str(nodeTag) + str(2)), xLoc + self._element.getHc()*self._columfactor / 2, yLoc)
                    else:
                        ops.node(int(str(nodeTag) + str(1)), xLoc - self._element.getHc() / 2, yLoc)
                        ops.node(int(str(nodeTag) + str(2)), xLoc + self._element.getHc() / 2, yLoc)

                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1


            yLoc = yLoc + self._floor_h


    def addDoublicantPoints(self):
        # Add doublicant points to allow for zero link elements
        yLoc = self._floor_h
        nodeTag = 2001 + self._numBay + 1
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

        for j in range(0, self._numFloor):
            xLoc = 0.

            # 1000-punktene er slave til 2000-punktene som er koblet til bjelkene
            for i in range(0, self._numBay + 1):
                if i == 0:
                    ops.node(nodeTag, xLoc + self._element.getHw() / 2, yLoc)
                    ops.equalDOF(nodeTag, nodeTag - 1000, 1, 2)

                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1
                elif i == self._numBay:
                    ops.node(nodeTag, xLoc - self._element.getHw() / 2, yLoc)
                    ops.equalDOF(nodeTag, nodeTag - 1000, 1, 2)

                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1
                else:
                    if ((i == columnNr2 or i == columnNr1) and self._outrigger):
                        ops.node(int(str(nodeTag) + str(1)), xLoc - self._element.getHc()*self._columfactor / 2, yLoc)
                        ops.equalDOF(int(str(nodeTag) + str(1)), int(str(nodeTag - 1000) + str(1)), 1, 2)

                        ops.node(int(str(nodeTag) + str(2)), xLoc + self._element.getHc()*self._columfactor / 2, yLoc)
                        ops.equalDOF(int(str(nodeTag) + str(2)), int(str(nodeTag - 1000) + str(2)), 1, 2)

                    else:
                        ops.node(int(str(nodeTag) + str(1)), xLoc - self._element.getHc() / 2, yLoc)
                        ops.equalDOF(int(str(nodeTag) + str(1)), int(str(nodeTag - 1000) + str(1)), 1, 2)

                        ops.node(int(str(nodeTag) + str(2)), xLoc + self._element.getHc() / 2, yLoc)
                        ops.equalDOF(int(str(nodeTag) + str(2)), int(str(nodeTag - 1000) + str(2)), 1, 2)

                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1


            yLoc = yLoc + self._floor_h


    def addRotationalStiffnessPointsAtBase(self):
        yLoc = 0.
        nodeTag = 1001
        xLoc = 0.
        for i in range(0, self._numBay + 1):
            ops.node(nodeTag, xLoc, yLoc)
            ops.equalDOF(nodeTag, nodeTag - 1000, 1, 2)
            # allowing us to pin the base points

            xLoc = xLoc + self._L_bay
            nodeTag = nodeTag + 1



    def loadCalculations(self):
        self._loads.setLoadings(self._floor_h,self._L_bay,self._spacing)


    def massCalculation(self):
        if (self._loads.getLateral_load() == 0):
            self.loadCalculations()

        Q = self._loads.getQuasi() / 1000  # N/mm2
        #print("Q",Q)
        self._Q = Q

        g = 9810  # mm/sec2
        Mass = Q * self._spacing * self._L_bay * self._numBay / g
        #print("Mass",Mass)
        Mass_x = Mass / (self._numBay)  # Mass per node in ton
        #print("Mass_x",Mass_x)
        self._Mass = Mass
        self._Mass_x = Mass_x



    def setRotationalStiffness(self):
        # Rotational stiffnesese
        # Beams:
        Kb = self._element.getKrb() * 10 ** 6  # N.mm/rad
        # Columns and walls
        Kc = self._element.getKrc() * 10 ** 6  # N.mm/rad
        # Columns and walls
        Kw = self._element.getKrw() * 10 ** 6  # N.mm/rad


        ops.uniaxialMaterial('Elastic', 1, Kb)
        ops.uniaxialMaterial('Elastic', 2, Kc)
        ops.uniaxialMaterial('Elastic', 3, Kw)



    def addColumnsAndWalls(self):
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
        transfTag = 1
        for j in range(0, self._numBay + 1):

            end1 = j + 1
            end2 = end1 + self._numBay + 1

            for i in range(0, self._numFloor):
                if j == 0 or j == self._numBay:
                    ops.element('ElasticTimoshenkoBeam', eleTag, end1, end2, self._element.getE_wall(),
                                self._element.getG_wall(), self._element.getAw(),
                                self._element.getIw(), self._element.getAwy(), transfTag)
                else:
                    if ((i == columnNr2 or i == columnNr1) and self._outrigger):
                        ops.element('ElasticTimoshenkoBeam', eleTag, end1, end2, self._element.getE_wall(),
                                self._element.getG_wall(), self._element.getAc()*self._columfactor,
                                self._element.getIc()*self._columfactor**3, self._element.getAcy()*self._columfactor, transfTag)
                    else:
                        ops.element('ElasticTimoshenkoBeam', eleTag, end1, end2, self._element.getE_column(),
                                    self._element.getG_column(), self._element.getAc(),
                                    self._element.getIc(), self._element.getAcy(), transfTag)

                end1 = end2
                end2 = end2 + self._numBay + 1
                eleTag = eleTag + 1


    def addBeams(self):
        eleTag = 2001
        transfTag = 1
        for j in range(1, self._numFloor + 1):
            for i in range(1, self._numBay + 1):
                self._beams.append(eleTag)
                if i == 1:
                    end1 = (self._numBay + 1) * j + 2001
                    end2 = int(str(end1 + 1) + str(1))
                    ops.element('ElasticTimoshenkoBeam', eleTag, end1, end2, self._element.getE_beam(),
                                self._element.getG_beam(), self._element.getAb(),
                                self._element.getIb(), self._element.getAby(), transfTag)
                    eleTag = eleTag + 1

                elif i == self._numBay:
                    end2 = (self._numBay + 1) * j + 2001 + i
                    end1 = int(str(end2 - 1) + str(2))
                    ops.element('ElasticTimoshenkoBeam', eleTag, end1, end2, self._element.getE_beam(),
                                self._element.getG_beam(), self._element.getAb(),
                                self._element.getIb(), self._element.getAby(), transfTag)
                    eleTag = eleTag + 1

                else:
                    end2 = int(str((self._numBay + 1) * j + 2001 + i) + str(1))
                    end1 = int(str((self._numBay + 1) * j + 2001 + i - 1) + str(2))
                    ops.element('ElasticTimoshenkoBeam', eleTag, end1, end2, self._element.getE_beam(),
                                self._element.getG_beam(), self._element.getAb(),
                                self._element.getIb(), self._element.getAby(), transfTag)
                    eleTag = eleTag + 1


    def addRigidZones(self,approximationValue):
        eleTag = 1
        transfTag = 1
        for j in range(1, self._numFloor + 1):
            end1 = (self._numBay + 1) * j + 1
            for i in range(0, self._numBay + 1):

                if i == 0 or i == self._numBay:
                    end2 = end1 + 1000
                    ops.element('elasticBeamColumn', eleTag, end1, end2,
                                self._element.getAb() * approximationValue, 13e3,
                                self._element.getIb() * approximationValue, transfTag)


                else:
                    end2 = int(str(end1 + 1000) + str(1))
                    ops.element('elasticBeamColumn', eleTag, end1, end2,
                                self._element.getAb() * approximationValue, 13e3,
                                self._element.getIb() * approximationValue, transfTag)

                    eleTag = eleTag + 1

                    end2 = int(str(end1 + 1000) + str(2))
                    ops.element('elasticBeamColumn', eleTag, end1, end2,
                                self._element.getAb() * approximationValue, 13e3,
                                self._element.getIb() * approximationValue, transfTag)

                end1 = end1 + 1
                eleTag = eleTag + 1



    def setBeamConnections(self):
        yLoc = self._floor_h
        nodeTag = 2001 + self._numBay + 1

        for j in range(0, self._numFloor):
            xLoc = 0.
            for i in range(0, self._numBay + 1):
                if i == 0:
                    ops.element('zeroLength', self._zerolinkElementTag, nodeTag, nodeTag - 1000, '-mat', 1, '-dir', 6)

                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1

                elif i == self._numBay:
                    ops.element('zeroLength', self._zerolinkElementTag, nodeTag, nodeTag - 1000, '-mat', 1, '-dir', 6)

                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1

                else:
                    ops.element('zeroLength', self._zerolinkElementTag, int(str(nodeTag) + str(1)), \
                                int(str(nodeTag - 1000) + str(1)), '-mat', 1, '-dir', 6)

                    self._zerolinkElementTag = self._zerolinkElementTag + 1

                    ops.element('zeroLength', self._zerolinkElementTag, int(str(nodeTag) + str(2)), \
                                int(str(nodeTag - 1000) + str(2)), '-mat', 1, '-dir', 6)

                    xLoc = xLoc + self._L_bay
                    nodeTag = nodeTag + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1

            yLoc = yLoc + self._floor_h



    def setColumnConnectionsFixed(self):
        #setting the connections from the beams to the ground
        end1 = 1
        end2 = end1 + 1000

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

        for i in range(0, self._numBay + 1):
            if (self._outrigger):
                if i == self._numBay or i == 0:
                    ops.fix(end2, 1, 1, 1)
                    # setting correct rotation stiffness to walls
                    ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 2, '-dir', 6)
                    end1 = end1 + 1
                    end2 = end2 + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1
                else:
                    if ((i == columnNr2 or i == columnNr1)):
                        ops.fix(end2, 1, 1, 1)
                        ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 3, '-dir', 6)
                        end1 = end1 + 1
                        end2 = end2 + 1
                        self._zerolinkElementTag = self._zerolinkElementTag + 1
                    else:
                        ops.fix(end2, 1, 1, 1)
                        ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 2, '-dir', 6)
                        end1 = end1 + 1
                        end2 = end2 + 1
                        self._zerolinkElementTag = self._zerolinkElementTag + 1

            else:
                if i == self._numBay or i == 0:
                    ops.fix(end2, 1, 1, 1)
                    ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 3, '-dir', 6)
                    end1 = end1 + 1
                    end2 = end2 + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1
                else:
                    ops.fix(end2, 1, 1, 1)
                    ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 2, '-dir', 6)
                    end1 = end1 + 1
                    end2 = end2 + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1


    def setColumnConnectionsPinned(self):
        #setting the connections from the beams to the ground
        end1 = 1
        end2 = end1 + 1000

        if (self._numBay + 1)<5:
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


        for i in range(0, self._numBay + 1):
            if (self._outrigger):
                if i == self._numBay or i == 0:
                    ops.fix(end2, 1, 1, 0)
                    # setting correct rotation stiffness to walls
                    ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 2, '-dir', 6)
                    end1 = end1 + 1
                    end2 = end2 + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1
                else:
                    if ((i == columnNr2 or i == columnNr1)):
                        ops.fix(end2, 1, 1, 0)
                        ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 3, '-dir', 6)
                        end1 = end1 + 1
                        end2 = end2 + 1
                        self._zerolinkElementTag = self._zerolinkElementTag + 1
                    else:
                        ops.fix(end2, 1, 1, 0)
                        ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 2, '-dir', 6)
                        end1 = end1 + 1
                        end2 = end2 + 1
                        self._zerolinkElementTag = self._zerolinkElementTag + 1

            else:
                if i == self._numBay or i == 0:
                    ops.fix(end2, 1, 1, 0)
                    ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 3, '-dir', 6)
                    end1 = end1 + 1
                    end2 = end2 + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1
                else:
                    ops.fix(end2, 1, 1, 0)
                    ops.element('zeroLength', self._zerolinkElementTag, end1, end2, '-mat', 2, '-dir', 6)
                    end1 = end1 + 1
                    end2 = end2 + 1
                    self._zerolinkElementTag = self._zerolinkElementTag + 1



    def setNodalMass(self,otrs):
        applied_mass = 0
        if (otrs == None):
            # adding modal mass to the main grid
            nodeTag = self._numBay + 2
            for j in range(1, self._numFloor + 1):
                for i in range(1, self._numBay + 2):
                    if i == 1 or i == self._numBay + 1:
                        ops.mass(nodeTag, self._Mass_x / 2, 0.000001, 0.000001)
                        applied_mass += self._Mass_x / 2
                    else:
                        ops.mass(nodeTag, self._Mass_x, 0.000001, 0.000001)
                        applied_mass += self._Mass_x

                    nodeTag = nodeTag + 1
        elif (otrs._system == 1):
            # adding modal mass to the main grid
            nodeTag = self._numBay + 2
            for j in range(1, self._numFloor + 1):
                for i in range(1, self._numBay + 2):
                    if i == 1 or i == self._numBay + 1:
                        ops.mass(nodeTag, self._Mass_x / 2, 0.000001, 0.000001)
                        applied_mass += self._Mass_x / 2
                    else:
                        ops.mass(nodeTag, self._Mass_x, 0.000001, 0.000001)
                        applied_mass += self._Mass_x

                    nodeTag = nodeTag + 1

        elif (otrs._system == 2 ):
            # adding modal mass to the main grid
            nodeTag = self._numBay + 2
            for j in range(1, self._numFloor + 1):
                for i in range(1, self._numBay + 2):
                    if i == 1 or i == self._numBay + 1:
                        ops.mass(nodeTag, self._Mass_x / 2, 0.000001, 0.000001)
                        applied_mass += self._Mass_x / 2
                    else:
                        ops.mass(nodeTag, self._Mass_x, 0.000001, 0.000001)
                        applied_mass += self._Mass_x

                    nodeTag = nodeTag + 1

        elif (otrs._system == 3):
            # adding modal mass to the main grid
            nodeTag = self._numBay + 2
            for j in range(1, self._numFloor + 1):
                if j in otrs._addedFloors:
                    for i in range(1, self._numBay + 2):
                        if i == 1 or i == self._numBay + 1:
                            #print(nodeTag,"faar masse:",self._Mass_x / 4)
                            ops.mass(nodeTag, self._Mass_x / 4, 0.000001, 0.000001)
                            applied_mass += self._Mass_x / 4
                        else:
                            #print(nodeTag,"faar masse:",self._Mass_x / 2)
                            ops.mass(nodeTag, self._Mass_x / 2, 0.000001, 0.000001)
                            applied_mass += self._Mass_x / 2

                        nodeTag = nodeTag + 1

                else:
                    for i in range(1, self._numBay + 2):
                        if i == 1 or i == self._numBay + 1:
                            #print(nodeTag,"faar masse:",self._Mass_x / 2)
                            ops.mass(nodeTag, self._Mass_x / 2, 0.000001, 0.000001)
                            applied_mass += self._Mass_x / 2

                        else:
                            #print(nodeTag,"faar masse:",self._Mass_x)
                            ops.mass(nodeTag, self._Mass_x, 0.000001, 0.000001)
                            applied_mass += self._Mass_x

                        nodeTag = nodeTag + 1


            for nodeTag in otrs._usedMidPoints:
                #print(nodeTag,"faar masse:",self._Mass_x / 2)
                ops.mass(nodeTag, self._Mass_x / 2, 0.000001, 0.000001)
                applied_mass += self._Mass_x / 2



        else:
            print("OutriggerSystem Error")

        # applied_mass*(numFrames-1)*1000 = TOTALMASS [kg]


    def eigenValues(self,otrs = None):
        self.setNodalMass(otrs)
        eigenValues = ops.eigen(self._numEigen)
        PI = 2 * asin(1.0)

        for i in range(0, self._numEigen):
            lamb = eigenValues[i]
            period = 2 * PI / sqrt(lamb)
            freq = 1 / period
            self._Freq.append(freq)

        node = 1
        eigenVector = []
        for i in range(0,self._numFloor+1):
            eigenVector.append(ops.nodeEigenvector(node,1,1))
            node += (self._numBay + 1)

        first = eigenVector[-1]
        for i in range(0,self._numFloor+1):
            eigenVector[i] = eigenVector[i]/first

        first = eigenVector[0]
        for i in range(0,self._numFloor+1):
            eigenVector[i] = eigenVector[i] - first

        self._eigenVector = eigenVector

        #print('The first mode freq: ' + str(round(self._Freq[0], 8)) + ' Hz')

        return self._eigenVector

    def plotModeShapes(self):
        for i in range(1,self._numEigen+1):
            opsplt.plot_modeshape(i, 30000)


    def getNumBays(self):
        return self._numBay

    def getNumFloor(self):
        return self._numFloor

    def getL_bay(self):
        return self._L_bay

    def getFloor_h(self):
        return self._floor_h

    def getFreq(self):
        return round(self._Freq[0], 6)



















