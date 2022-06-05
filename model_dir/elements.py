class StandardElement(object):
    def __init__(self):
        # Material properties (N/mm2)
        self._E_GL30c = 13000
        self._G_GL30c = 650
        self._E_CLT = 11000
        self._G_CLT = 690

        # Beams (mm)
        self._bb = 430.
        self._hb = 540.

        # Columns (mm)
        self._bc = 430.
        self._hc = 630.

        # Walls (mm)
        self._bw = 430.
        self._hw = 3000.

        # truss (mm)
        self._bt = 430.
        self._ht = 300.

        # Rotational stiffness
        # Beams (mm)
        self._Krb = 25920 #round((self._hb / 450) ** 2 * 4500,0)  # kN.m/rad

        # Columns (mm)
        self._Krc = 10000  # kN.m/rad

        # CLT walls (mm)
        self._Krw = 200000  # kN.m/rad

        # Aksial stiffness of connectiones
        self._Kaxd = 1000



    # Beams (mm)
    def getHb(self):
        return self._hb

    def getBb(self):
        return self._bb

    def getAb(self):
        return self._bb * self._hb

    def getIb(self):
        return self._bb * self._hb**3 / 12

    def getAby(self):
        return (5 / 6)*self._bb * self._hb


    # Columns (mm)
    def getHc(self):
        return self._hc

    def getBc(self):
        return self._bc

    def getAc(self):
        return self._bc * self._hc

    def getIc(self):
        return self._bc * self._hc ** 3 / 12

    def getAcy(self):
        return (5 / 6) * self._bc * self._hc

    # Truss (mm)
    def getHt(self):
        return self._ht

    def getBt(self):
        return self._bt

    def getAt(self):
        return self._bt * self._ht

    def getIt(self):
        return self._bt * self._ht ** 3 / 12

    def getAty(self):
        return (5 / 6) * self._bt * self._ht

    # CLT walls (mm)
    def getHw(self):
        return self._hw

    def getBw(self):
        return self._bw

    def getAw(self):
        return self._bw * self._hw

    def getIw(self):
        return self._bw * self._hw ** 3 / 12

    def getAwy(self):
        return (5 / 6) * self._bw * self._hw



    # Rotational stiffness
    def getKrb(self):
        return self._Krb

    def setKrb(self, verdi):
        self._Krb = verdi

    def getKrc(self):
        return self._Krc

    def getKrw(self):
        return self._Krw

    def getKrTruss(self):
        return self._KrTruss


    # E/G-modules
    # columns
    def getE_column(self):
        return self._E_GL30c

    def getG_column(self):
        return self._G_GL30c

    # walls
    def getE_wall(self):
        return self._E_CLT

    def getG_wall(self):
        return self._G_CLT

    # beams
    def getE_beam(self):
        return self._E_GL30c

    def getG_beam(self):
        return self._G_GL30c

    # TrussSetFunctions (mm)
    def setHt(self, verdi):
        self._ht = verdi

    def setBt(self, verdi):
        self._bt = verdi

    # BeamSetFunction (mm)
    def setHb(self, verdi):
        self._hb = verdi

    def setBb(self, verdi):
        self._bb = verdi

    # ColumnSetFunction (mm)
    def setHc(self, verdi):
        self._hc = verdi

    def setBc(self, verdi):
        self._bc = verdi

    # WallSetFunction (mm)
    def setHw(self, verdi):
        self._hw = verdi

    def setBw(self, verdi):
        self._bw = verdi

