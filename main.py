import openseespy.opensees as ops

from model_dir.model import Model
from functions_dir.WindFunction import *
from functions_dir.AccelFunction import *
from functions_dir.forceDisplayer import *
from functions_dir.System_check import *

from model_dir.loads import Loads
from model_dir.elements import StandardElement
from model_dir.analysis import Analysis

otrs = None

ops.wipe()
# Choosing element
standardElements = StandardElement()
# Defining model parameters
numBay     =  3
L_bay      =  7000.   # mm
numFloor   =  10
floor_h    =  3500.    # mm
spacing    =  5000     # mm
numFrames  =  6

# Setting loads
Dead_load = 2
Live_load = 3
Lateral_load_1 = windFunction(numBay, L_bay, numFloor, floor_h, spacing, numFrames, wind=26)

loads = Loads(Dead_load, Live_load, Lateral_load_1)

from model_dir.outRiggerElementsEveryOtherDir import OutRiggerSystem

# Creating model
model = Model('Linear',
              numBay,
              numFloor,
              floor_h,
              spacing,
              L_bay,
              loads,
              standardElements,
              pinned=False,
              outrigger=False)

model.plotModel()

#model.plotModel()
# setting outrigger system
otrs = OutRiggerSystem(model, complete=True)
outriggerFloor1 = round(numFloor * 0.5)
otrs.setHorizontalOutrigger(outriggerFloor1)

model.plotModel()

# EigenValues
eigenVector = model.eigenValues(otrs) #assignes nodal masses
freq = model.getFreq()


#model.plotModeShapes()
#model.plotModeShapes()
# Start Analysis

analysis = Analysis(model, otrs, uniform=True, complete=True)


#mass2 = (Dead_load + 0.3 * Live_load)*(spacing)*(numFloor)*(numBay*L_bay)
#print("calculated mass: ", mass2)
#analysis.elasticBucklingAnalysis() # Need to run PDelta for this one
#print("totalMass|real", buildingMass*(numFrames-1)*1000/9.81) #from massfunction
#print("totalMass|dup", mass2*(numFrames-1)*1000/9.81) #direct from quasi

buildingMass = model._Mass*(numFrames-1)*numFloor*1000

analysis.getLaterDisplacements(wind=True, deadAndLive=True, ULT=True, plot=True)

forceElements = analysis.getforceElements()


ops.wipe()

if otrs != None:
    print(otrs.getDiagonalStiffness())
    displayForces(forceElements, floor_h, L_bay, otrs._system)
else:
    displayForces(forceElements, floor_h, L_bay, 1)

acc = accelFunction(numBay, L_bay, numFloor, floor_h, spacing, numFrames, freq, buildingMass, eigenVector)

print("Acceleration:", round(acc, 5))
print("Frequency", round(freq, 5))
print("Top Floor Displacement:", analysis.getTopFloorDisp())
print("MAX IDR:", analysis.getMaxIDR(), "and occurs at floors:", analysis.getMaxIDRfloor()[0], "and", analysis.getMaxIDRfloor()[1])


beam, column, wall, outrigger = Design_Check(standardElements, forceElements, floor_h, numFloor, L_bay, loads.getQuasi(), spacing)
