import numpy as np
import openseespy.opensees as ops
import scipy.linalg as slin
from math import asin, sqrt
import matplotlib.pyplot as plt


class Analysis(object):
    def __init__(self, model, otrs=None, uniform=True, complete=False):
        ops.wipeAnalysis()
        self._analyze = False
        self._numFloor = model.getNumFloor()
        self._numBay = model.getNumBays()
        self._uniform = uniform

        self._Px = model._loads.getPx()
        self._Py = model._loads.getPy()
        self._Mz = model._loads.getMz()

        self._QuasiPy = model._loads.getQuasiPy()
        self._QuasiMz = model._loads.getQuasiMz()

        self._Ke = self.getElasticStiffnessMatrix()
        self._spacing = model._spacing
        self._model = model
        self._ULS = model._loads.getULS()
        self._Char = model._loads.getCharacteristic()
        self._Quasi = model._loads.getQuasi()
        self._L_bay = model.getL_bay()
        self._forceMatrix = np.zeros((self._numFloor+1,self._numBay+1))
        self._complete = complete
        self._outrigger = model._outrigger

        self._K = None
        self._Kgeo = None

        self._maxIDR = None
        self._maxIDR_floor = None
        self._topFloorDisp = None
        self._displacement = []
        self._otrs = otrs
        self._forceElements = None

        if self._otrs != None:

            if (self._otrs._complete):
                self._otrs.findAllBeamsColumns()
            else:
                pass

            self._forceElements = otrs._forceElements

            numbFloor = 2

            columns = [((1000 + numbFloor - 1) + i * (self._numFloor)) for i in range(self._numBay + 1)]

            if (self._complete == False): # vi har en outrigger skal kun legge inn bunsøyler
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


        else: # ikke outrigger
            forceElements = {}
            forceElements["beams"] = {}
            forceElements["walls"] = {}
            forceElements["columns"] = {}
            forceElements["ORelements"] = {}

            if (self._complete == False):

                numbFloor = 2

                columns = [((1000 + numbFloor - 1) + i * (self._numFloor)) for i in range(self._numBay + 1)]

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
                                forceElements["columns"][str(column)] = []
                            else:
                                forceElements["walls"][str(column)] = []

                        else:
                            if ((i == columnNr2 or i == columnNr1) and self._outrigger):
                                forceElements["walls"][str(column)] = []
                            else:
                                forceElements["columns"][str(column)] = []

                else:
                    for i, column in enumerate(columns):
                        if i == 0 or i == self._numBay:
                            forceElements["walls"][str(column)] = []
                        else:
                            forceElements["columns"][str(column)] = []

            else:
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
                                forceElements["columns"][str(eleTag)] = []
                            else:
                                forceElements["walls"][str(eleTag)] = []

                        else:
                            if ((i == columnNr2 or i == columnNr1) and self._outrigger):
                                forceElements["s"][str(eleTag)] = []
                            else:
                                forceElements["columns"][str(eleTag)] = []

                        eleTag = eleTag + 1

                eleTag = 2001
                for j in range(1, self._numFloor + 1):
                    for i in range(1, self._numBay + 1):
                        if i == 1:
                            forceElements["beams"][str(eleTag)] = []
                            eleTag = eleTag + 1

                        elif i == self._numBay:
                            forceElements["beams"][str(eleTag)] = []
                            eleTag = eleTag + 1

                        else:
                            forceElements["beams"][str(eleTag)] = []
                            eleTag = eleTag + 1


            self._forceElements = forceElements


        self._beams = model._beams

        # Create TimeSeries, this shows how the loads will be applied
        ops.timeSeries("Constant", 1)  # Gravity loads are constant, can also be linear
        ops.timeSeries("Linear", 2)

        # The vertical load distributed along the horizontal member can be represented
        # by nodal forces and moments. The nodal forces are distributed equally to the
        # two end nodes, the nodal bending moments are equal and opposite
        # We do that for the Characteristic loads applied to the beams




    def elasticBucklingAnalysis(self):
        # We have calculated the stiffness matrix before applying load, now we need
        # to calculate after applying loads so we can get goemetric stiffness matrix
        # Remove all load patterns and analysis results
        ops.wipeAnalysis()

        # Apply ULS load
        self.setULS_DeadAndLiveLoad()

        # The Convergance parameters
        ops.system("FullGeneral")
        ops.numberer("RCM")
        ops.constraints("Plain")
        ops.integrator("LoadControl", 0.)
        ops.algorithm("Newton")
        ops.test('NormDispIncr', 1.0e-6, 1000)
        ops.analysis("Static")

        # Solve
        ok = ops.analyze(1)

        # Check the analysis
        if ok != 0:
            print("Analysis failed")

        # K is the stiffness matrix of the model after loading = Ke - Kgeo (K = Ke - Kgeo)
        # Where Kgeo is the geometric stiffness matrix, which depends upon the deformed
        # geometry of the structure and the axial forces in the members
        N = ops.systemSize()
        K = ops.printA('-ret')
        K = np.array(K)
        self._K = K
        K.shape = (N, N)


        # We can calculate the geometric stiffness matrix now :
        Kgeo = self._Ke - K
        self._Kgeo = Kgeo

        # Eigenvalue solution
        lam, x = slin.eig(self._Ke, Kgeo)

        # Sort the positive eigenvalues
        lamSort = np.sort(lam[lam > 0])
        print('The buckling factor : ' + str(round(lamSort[0].real,2)))

        ops.remove("loadPattern", 1)




    def getBuildingMass(self, plot = True):
        # We have calculated the stiffness matrix before applying load, now we need
        # to calculate after applying loads so we can get goemetric stiffness matrix
        # Remove all load patterns and analysis results
        ops.wipeAnalysis()

        # Apply ULS load
        self.setQuasiLoad()

        N_steps = 10  # When applying the loads, apply it in several steps
        # Convergance parameters
        ops.system("BandGeneral")
        ops.numberer("RCM")
        ops.constraints("Plain")
        ops.integrator("LoadControl", 1. / N_steps)
        ops.algorithm("Newton")
        ops.test('NormDispIncr', 1.0e-6, 1000)
        # tolerance criteria = 1.0e-6
        # max number of iterations = 1000

        ops.analysis("Static")

        # Perform the analysis
        # The number inside the brackets multiplied by load increment  should = 1
        ok = ops.analyze(N_steps)  # ok will be 0 if the analysis was successful

        if ok != 0:
            print("Analysis failed")

        mass = self.getNodalForce(plot)

        ops.remove("loadPattern", 1)

        ops.wipeAnalysis()

        return mass


    def getLaterDisplacements(self,wind,deadAndLive, ULS = False, plot=True):
        # Remove all load patterns and analysis results
        ops.wipeAnalysis()

        if (wind == False and deadAndLive == False):
            return print("ERROR, you need to set loads")

        # Apply char dead and live loads (nodal vertical forces and bending moments)
        if (ULS):
            # Apply lateral wind load
            if (wind):
                self.setWindLoad()

            # Apply lateral ULS load
            if (deadAndLive):
                self.setULS_DeadAndLiveLoad()
        else:
            # Apply lateral wind load
            if (wind):
                self.setWindLoad()

            # Apply lateral SLS load
            if (deadAndLive):
                self.setDeadAndLiveLoad()


        if (plot):
            print("\nLaterDisplacementsAnalysis")
        self.solveModel()

        ops.remove("loadPattern", 1)
        ops.remove("loadPattern", 2)

        self.getNodalForce(plot)

        self.getRelevantForces()


        # Top floor displacement
        Top_point = (self._numBay + 1) * (self._numFloor + 1)
        Top_ux = ops.nodeDisp(Top_point, 1)  # Displacement in x direction in mm
        if (plot):
            print('The top floor displacement : ' + str(round(Top_ux,3)) + ' mm')

        self._topFloorDisp = round(Top_ux,3)

        # Mode shape
        mode_number = 1
        Mode = []
        for i in range(0, self._numFloor + 1):
            top = ops.nodeEigenvector(Top_point, mode_number, 1)
            Mode.append(abs(ops.nodeEigenvector(Top_point - i * (self._numBay + 1), mode_number, 1) / top))

        # Inter-storey drift in mm

        displacement = []
        node = self._numBay + 1
        for i in range(0, self._numFloor+1):
            disp = ops.nodeDisp(node, 1)
            displacement.append((i, disp))
            node += (self._numBay + 1)

        self._displacement = displacement
        y = [displacement[i][0]*self._model._floor_h for i in range(len(displacement))]
        x = [displacement[i][1] for i in range(len(displacement))]

        IDR = [x[i+1]-x[i] for i in range(len(x)-1)]

        # plt.plot(x,y,'--bo')
        # plt.show()

        if (plot):
            print('Max IDR : ' + str(round(max(IDR),2)) + ' mm',"\n")

        self._maxIDR = round(max(IDR),2)
        floor1 = IDR.index(max(IDR))
        self._maxIDR_floor = (floor1, floor1+1)

        self._analyze = False

        ops.wipeAnalysis()



    def getElasticStiffnessMatrix(self):
        ops.system('FullGeneral')  # generates the LinearSOE and LinearSolver objects
        ops.numberer("RCM")
        ops.constraints("Plain")
        ops.integrator('LoadControl', 0)  #
        ops.algorithm("Newton")
        ops.analysis('Static')


        # Solve without any loads
        ok = ops.analyze(1)

        if ok != 0:
            print("Analysis failed")

        # Get the elastic stiffness before applying any loads
        N = ops.systemSize()
        Ke = ops.printA('-ret')
        Ke = np.array(Ke)
        Ke.shape = (N, N)
        ops.wipeAnalysis()
        return Ke


    def setDeadAndLiveLoad(self):
        ops.pattern("Plain", 1, 1)

        if (self._uniform):
            char = self._Char*self._spacing/(-1000)
            for etag in self._beams:
                ops.eleLoad('-ele', etag, '-type', '-beamUniform', char,  0.)

            eleTag = 1
            for j in range(1, self._numFloor + 1):
                for i in range(0, self._numBay + 1):
                    if i == 0:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', char, 0.)
                    elif i == self._numBay:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', char*-1, 0.)
                    else:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', char*-1, 0.)

                        eleTag = eleTag + 1

                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', char, 0.)

                    eleTag = eleTag + 1

        else:
            for j in range(1, self._numFloor + 1):
                for i in range(1, self._numBay + 1):

                    if i == 1:
                        end1 = (self._numBay + 1) * j + 2001
                        end2 = int(str(end1 + 1) + str(1))
                        ops.load(end1, 0., -self._Py / 2, -self._Mz)
                        ops.load(end2, 0., -self._Py / 2, self._Mz)


                    elif i == self._numBay:
                        end2 = (self._numBay + 1) * j + 2001 + i
                        end1 = int(str(end2 - 1) + str(2))
                        ops.load(end1, 0., -self._Py / 2, -self._Mz)
                        ops.load(end2, 0., -self._Py / 2, self._Mz)


                    else:
                        end2 = int(str((self._numBay + 1) * j + 2001 + i) + str(1))
                        end1 = int(str((self._numBay + 1) * j + 2001 + i - 1) + str(2))
                        ops.load(end1, 0., -self._Py / 2, -self._Mz)
                        ops.load(end2, 0., -self._Py / 2, self._Mz)


    def setQuasiLoad(self):
        ops.pattern("Plain", 1, 1)

        if (self._uniform):
            quasi = self._Quasi*self._spacing/(-1000)
            for etag in self._beams:
                ops.eleLoad('-ele', etag, '-type', '-beamUniform', quasi,  0.)

            eleTag = 1
            for j in range(1, self._numFloor + 1):
                for i in range(0, self._numBay + 1):
                    if i == 0:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', quasi, 0.)
                    elif i == self._numBay:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', quasi * -1, 0.)
                    else:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', quasi * -1, 0.)

                        eleTag = eleTag + 1

                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', quasi, 0.)

                    eleTag = eleTag + 1

        else:
            for j in range(1, self._numFloor + 1):
                for i in range(1, self._numBay + 1):

                    if i == 1:
                        end1 = (self._numBay + 1) * j + 2001
                        end2 = int(str(end1 + 1) + str(1))
                        ops.load(end1, 0., -self._QuasiPy / 2, -self._QuasiMz)
                        ops.load(end2, 0., -self._QuasiPy / 2, self._QuasiMz)


                    elif i == self._numBay:
                        end2 = (self._numBay + 1) * j + 2001 + i
                        end1 = int(str(end2 - 1) + str(2))
                        ops.load(end1, 0., -self._QuasiPy / 2, -self._QuasiMz)
                        ops.load(end2, 0., -self._QuasiPy / 2, self._QuasiMz)


                    else:
                        end2 = int(str((self._numBay + 1) * j + 2001 + i) + str(1))
                        end1 = int(str((self._numBay + 1) * j + 2001 + i - 1) + str(2))
                        ops.load(end1, 0., -self._QuasiPy / 2, -self._QuasiMz)
                        ops.load(end2, 0., -self._QuasiPy / 2, self._QuasiMz)



    def setWindLoad(self):
        ops.pattern("Plain", 2, 2)
        nodeTag = self._numBay + 2
        for i in range(1, self._numFloor + 1):
            if i == self._numFloor:
                ops.load(nodeTag, self._Px / 2, 0, 0.)
                #print("Px =",self._Px/1000,"kN")
                #print("Px/2 =",self._Px/2/1000,"kN","(top floor)")

            else:
                ops.load(nodeTag, self._Px, 0, 0.)

            nodeTag = nodeTag + self._numBay + 1



    def setULS_DeadAndLiveLoad(self):
        ops.pattern("Plain", 1, 1)

        S = self._spacing
        ULS = self._ULS
        if (self._uniform):
            ult = S*ULS/(-1000)
            for etag in self._beams:
                ops.eleLoad('-ele', etag, '-type', '-beamUniform', ult, 0.)

            eleTag = 1
            for j in range(1, self._numFloor + 1):
                for i in range(0, self._numBay + 1):
                    if i == 0:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', ult, 0.)
                    elif i == self._numBay:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', ult * -1, 0.)
                    else:
                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', ult * -1, 0.)

                        eleTag = eleTag + 1

                        ops.eleLoad('-ele', eleTag, '-type', '-beamUniform', ult, 0.)

                    eleTag = eleTag + 1

        else:
            # Apply ultimate loads (gravity)
            Py = (ULS / 1000) * S * self._L_bay  # ULS point load (dead and live loads)
            Mz = ((ULS / 1000) * S) * self._L_bay ** 2 / 12  # Moment due to dead and live load

            for j in range(1, self._numFloor + 1):
                for i in range(1, self._numBay + 1):

                    if i == 1:
                        end1 = (self._numBay + 1) * j + 2001
                        end2 = int(str(end1 + 1) + str(1))
                        ops.load(end1, 0., -Py / 2, -Mz)
                        ops.load(end2, 0., -Py / 2, Mz)


                    elif i == self._numBay:
                        end2 = (self._numBay + 1) * j + 2001 + i
                        end1 = int(str(end2 - 1) + str(2))
                        ops.load(end1, 0., -Py / 2, -Mz)
                        ops.load(end2, 0., -Py / 2, Mz)


                    else:
                        end2 = int(str((self._numBay + 1) * j + 2001 + i) + str(1))
                        end1 = int(str((self._numBay + 1) * j + 2001 + i - 1) + str(2))
                        ops.load(end1, 0., -Py / 2, -Mz)
                        ops.load(end2, 0., -Py / 2, Mz)



    def getNodalForce(self,plot=True):
        ops.reactions('-dynamic', '-rayleigh')
        nodeTag = 1
        for j in range(0, self._numFloor+1):
            for i in range(0, self._numBay+1):
                force = round(ops.nodeReaction(nodeTag,2),4)
                self._forceMatrix[j][i] = force
                nodeTag += 1

        sum = 0
        if (plot):
            print("Reaction Forces:")
            for i in range(0, self._numBay + 1):
                print("Node",str(i+1)+":", round(self._forceMatrix[0][i]/1000,2), end=" kN\t")
                sum += self._forceMatrix[0][i]
            print()
        else:
            for i in range(0, self._numBay + 1):
                sum += self._forceMatrix[0][i]

        mass = round(sum/1000,0)
        if (plot):
            if mass != 0:
                print("Total building mass =", round(sum/1000,0),"kN")

        return mass

    def getMaxIDR(self):
        return self._maxIDR

    def getTopFloorDisp(self):
        return self._topFloorDisp

    def getMaxIDRfloor(self):
        return self._maxIDR_floor

    def getDisplacementVector(self):
        return self._displacement

    def getforceElements(self):
        return self._forceElements

    def solveModel(self):

        N_steps = 10              # When applying the loads, apply it in several steps
        # Convergance parameters
        ops.system("BandGeneral") # eller BandGeneral -> får ikke hentet K-matrise
        '''
        This command is used to construct a Full General linear system of equation object. 
        As the name implies, the class utilizes NO space saving techniques to cut down on the amount of memory used. 
        If the matrix is of size, nxn, then storage for an nxn array is sought from memory when the program runs. 
        When a solution is required, the Lapack routines DGESV and DGETRS are used.'''

        ops.numberer("RCM")
        '''
        This command is used to construct an RCM degree-of-freedom numbering object 
        to provide the mapping between the degrees-of-freedom at the nodes and the equation numbers. 
        An RCM numberer uses the reverse Cuthill-McKee scheme to order the matrix equations.'''

        ops.constraints("Plain")
        '''
        This command is used to construct a Plain constraint handler. 
        A plain constraint handler can only enforce homogeneous single point constraints (fix command) and multi-point 
        constraints constructed where the constraint matrix is equal to the identity (equalDOF command). 
        The following is the command to construct a plain constraint handler:'''

        ops.integrator("LoadControl" , 1/N_steps)
        '''
        This command is used to construct the Integrator object. 
        The Integrator object determines the meaning of the terms in the system of equation object Ax=B.
        The change in applied loads that this causes depends on the active load pattern 
        (those load pattern not set constant) and the loads in the load pattern. 
        If the only active load acting on the Domain are in load pattern with a Linear time series
         with a factor of 1.0, this integrator is the same as the classical load control method.'''

        ops.algorithm("Newton")
        '''
        This command is used to construct a SolutionAlgorithm object, 
        which determines the sequence of steps taken to solve the non-linear equation.
        Create a Newton-Raphson algorithm. The Newton-Raphson method is the most widely
         used and most robust method for solving nonlinear algebraic equations.'''


        ops.test('NormDispIncr', 1.0e-6, 1000)
        '''
        This command is used to construct the LinearSOE and LinearSolver objects
         to store and solve the test of equations in the analysis.
        Create a NormUnbalance test, which uses the norm of the left hand side
         solution vector of the matrix equation to determine if convergence has been reached.
         '''
        # tolerance criteria = 1.0e-6
        # max number of iterations = 1000


        ops.analysis("Static")
        '''
        This command is used to construct the Analysis object, 
        which defines what type of analysis is to be performed.'''

        # Perform the analysis
        # The number inside the brackets multiplied by load increment  should = 1
        ok=ops.analyze(N_steps)   # ok will be 0 if the analysis was successful

        if ok != 0:
            print("Analysis failed")
        self._analyze = True



    def getRelevantForces(self):
        if self._forceElements == None:
            return

        columnDict = self._forceElements["columns"]
        beamDict = self._forceElements["beams"]
        ORelementsDict = self._forceElements["ORelements"]
        wallDict = self._forceElements["walls"]

        for column in columnDict.keys():
            forces = ops.eleForce(int(column))
            for force in forces:
                columnDict[column].append(round(force))

        for beam in beamDict.keys():
            forces = ops.eleForce(int(beam))
            for force in forces:
                beamDict[beam].append(round(force))

        for OR in ORelementsDict.keys():
            forces = ops.eleForce(int(OR))
            for force in forces:
                ORelementsDict[OR].append(round(force))

        for wall in wallDict.keys():
            forces = ops.eleForce(int(wall))
            for force in forces:
                wallDict[wall].append(round(force))
