
# Import the needed libraries
import xlwings as xw
import pandas as pd
from scipy.optimize import curve_fit 
import numpy as np
from sklearn.metrics import r2_score

# Connect to the excel sheet containing the data
WorkBook=xw.Book('Merged_2.xlsx')

# Creat lists containing number of floors
Floors_12=list(np.arange(13))
Floors_10=list(np.arange(11))
Floors_8=list(np.arange(9))
Floors_6=list(np.arange(7))
Floors_4=list(np.arange(5))

# Reverse the list containing the number of floors
Floors_12.sort(reverse=True)
Floors_10.sort(reverse=True)
Floors_8.sort(reverse=True)
Floors_6.sort(reverse=True)
Floors_4.sort(reverse=True)

# Define the Z/H
ZH_12floors = [i/12 for i in Floors_12]
ZH_10floors = [i/10 for i in Floors_10]
ZH_8floors = [i/8 for i in Floors_8]
ZH_6floors = [i/6 for i in Floors_6]
ZH_4floors = [i/4 for i in Floors_4]

#a=list(map(lambda x:x**0.5,ZH_12floors))

# 12 floors
sheet=WorkBook.sheets[0]
df=sheet.range('M4:Y1727').options(pd.DataFrame,index=False,header=False).value
df=df.dropna()
Mode=df.T

score=[]

for i in range(len(df)):
    if (df[0][i]==1):
        #Get the first mode shape
        mode=Mode.iloc[:,i]

        # Defining the function that we will use to fit our data
        def func(ZH,c):
            return ZH**c

        # Initial guess of the C
        p0=[0]

        # Fit the Curve
        popt, pcov=curve_fit(func, ZH_12floors, mode,p0)

        # Calculate the mode shape using the fitted exponent
        MODE = list(map(lambda x: x ** popt[0], ZH_12floors))

# 10 floors
    if (df[2][i]==1):
        #Get the first mode shape
        mode=Mode.iloc[2:,i]

        # Defining the function that we will use to fit our data
        def func(ZH,c):
            return ZH**c

        # Initial guess of the C
        p0=[0]

        # Fit the Curve
        popt, pcov=curve_fit(func, ZH_10floors, mode,p0)

        # Calculate the mode shape using the fitted exponent
        MODE=list(map(lambda x:x**popt[0],ZH_10floors))

# 8 floors
    if (df[4][i] == 1):
        #Get the first mode shape
        mode=Mode.iloc[4:,i]

        # Defining the function that we will use to fit our data
        def func(ZH,c):
            return ZH**c

        # Initial guess of the C
        p0=[0]

        # Fit the Curve
        popt, pcov=curve_fit(func, ZH_8floors, mode,p0)

        # Calculate the mode shape using the fitted exponent
        MODE=list(map(lambda x:x**popt[0],ZH_8floors))

# 6 floors
    if (df[6][i] == 1):
        #Get the first mode shape
        mode=Mode.iloc[6:,i]

        # Defining the function that we will use to fit our data
        def func(ZH,c):
            return ZH**c

        # Initial guess of the C
        p0=[0]

        # Fit the Curve
        popt, pcov=curve_fit(func, ZH_6floors, mode,p0)

        # Calculate the mode shape using the fitted exponent
        MODE=list(map(lambda x:x**popt[0],ZH_6floors))

        Power_6.append(popt[0])
        score.append(r2_score(MODE,mode))

# 4 floors
    if (df[8][i] == 1):
        #Get the first mode shape
        mode=Mode.iloc[8:,i]

        # Defining the function that we will use to fit our data
        def func(ZH,c):
            return ZH**c

        # Initial guess of the C
        p0=[0]

        # Fit the Curve
        popt, pcov=curve_fit(func, ZH_4floors, mode,p0)

        # Calculate the mode shape using the fitted exponent
        MODE=list(map(lambda x:x**popt[0],ZH_4floors))

    punkt = 'AT'+str(i+4)

    score.append(r2_score(MODE, mode))

    WorkBook.sheets[0].range(punkt).options(transpose=True).value = popt[0]


print('Average R2 = '+str(sum(score)/len(score)))
