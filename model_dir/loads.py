class Loads(object):

    def __init__(self, Dead_load, Live_load, Lateral_load_1):
        self._Dead_load = Dead_load
        self._Live_load = Live_load
        self._Lateral_load_1 = Lateral_load_1

        self._Quasi = self._Dead_load + 0.3 * self._Live_load
        self._Characteristic = self._Dead_load + 0.7 * self._Live_load
        self._ULT = 1.2 * self._Dead_load + 1.5 * self._Live_load

        self._Lateral_load = 0
        self._Px = 0.
        self._Py = 0.
        self._Mz = 0.

        self._QuasiPy = 0.
        self._QuasiMz = 0.



    def getDead_load(self):
        if (self._Dead_load==0): print("Dead Load = 0")
        return self._Dead_load

    def getLive_load(self):
        if (self._Dead_load == 0): print("Dead Load = 0")
        return self._Live_load

    def getLateral_load(self):
        if (self._Dead_load == 0): print("Dead Load = 0")
        return self._Lateral_load

    def getQuasi(self):
        if (self._Dead_load == 0): print("Dead Load = 0")
        return self._Quasi

    def getCharacteristic(self):
        if (self._Characteristic== 0): print("Characteristic Load = 0")
        return self._Characteristic

    def getULT(self):
        if (self._ULT == 0): print("ULT Load = 0")
        return self._ULT

    def getPx(self):
        if (self._Px == 0): print("Px = 0")
        return self._Px

    def getPy(self):
        if (self._Py == 0): print("Py = 0")
        return self._Py

    def getMz(self):
        if (self._Mz == 0): print("Mz = 0")
        return self._Mz


    def getQuasiPy(self):
        if (self._QuasiPy == 0): print("Py = 0")
        return self._QuasiPy

    def getQuasiMz(self):
        if (self._QuasiMz == 0): print("Mz = 0")
        return self._QuasiMz


    def setLater_load(self, spacing):
        self._Lateral_load = self._Lateral_load_1 * spacing/ 1000


    def setLoadings(self,floor_h,L_bay,spacing):
        self.setLater_load(spacing)
        self._Px = self._Lateral_load * floor_h  # Lateral point load (wind)
        self._Py = (self._Characteristic / 1000) * spacing * L_bay  # Char point load (dead and live loads)
        self._Mz = ((self._Characteristic / 1000) * spacing) * L_bay ** 2 / 12  # Moment due to char dead and live load

        self._QuasiPy = (self._Quasi / 1000) * spacing * L_bay  # Quasi point load
        self._QuasiMz = ((self._Quasi / 1000) * spacing) * L_bay ** 2 / 12  # Moment due to char quasi load
