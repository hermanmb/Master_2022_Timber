from scipy.optimize import curve_fit
import numpy as np


def findingBestExponent(eigenVector, numFloor):
    # Creat lists containing number of floors
    Floors = list(np.arange(numFloor+1))

    # Reverse the list containing the number of floors
    Floors.sort(reverse=True)
    eigenVector.sort(reverse=True)

    # Define the Z/H
    ZH_floors = [i / numFloor for i in Floors]

    # a=list(map(lambda x:x**0.5,ZH_12floors))

    # Defining the function that we will use to fit our data
    def func(ZH, c):
        return ZH ** c

    # Initial guess of the C
    p0 = [0]

    # Get the first mode shape
    mode = eigenVector

    # Fit the Curve
    popt, pcov = curve_fit(func, ZH_floors, mode, p0)

    # Calculate the mode shape using the fitted exponent
    MODE = list(map(lambda x: x ** popt[0], ZH_floors))

    return popt[0]
