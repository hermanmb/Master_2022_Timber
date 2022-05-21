import math
import numpy as np

def windFunction(numBay, L_bay, numFloor, floor_h, spacing, numFrames,wind):
    heightOfTheBuilding= numFloor*floor_h/1000 #[m]
    paralellToTheWindSideOfTheBuilding = L_bay*numBay/1000 #[m]
    crosswindside = spacing*(numFrames - 1)/1000
    fundamentalBasicWindVelocity = wind
    C_s = 1                 #C_s C_d lag et utregnings
    C_d = 1
    C_dir = 1
    C_season = 1
    C_prob = 1
    n = 0.5
    k = 0.2
    returnPeriod = 50
    orographyFactor = 1
    turbulanceFactor = 1
    terrainCategory = 4


    # Calculation of k_r, z_0 and Z_min factor

    if terrainCategory == 0:
        k_r = 0.16
        z_0 = 0.003
        z_min = 2
    elif terrainCategory == 1:
        k_r = 0.17
        z_0 = 0.01
        z_min = 2
    elif terrainCategory == 2:
        k_r = 0.19
        z_0 = 0.05
        z_min = 4
    elif terrainCategory == 3:
        k_r = 0.22
        z_0 = 0.3
        z_min = 8
    elif terrainCategory == 4:
        k_r = 0.24
        z_0 = 1
        z_min = 16
    else:
        return print('Wrong Terrain Category')

    # Calculation of Reference Height z_s #

    if 0.6 * heightOfTheBuilding > z_min:
        z_s = 0.6 * heightOfTheBuilding
    else:
        z_s = z_min



    # Calculation of basic Wind Velocity V_b

    v_b = fundamentalBasicWindVelocity * C_dir * C_season * C_prob

    # Calculation of external pressure coefficients for vertical walls of rectangular plan buildings
    # EN1991-1-4, Tab:4.1
    # Må interpolere her

    ratio = heightOfTheBuilding/paralellToTheWindSideOfTheBuilding

    C_pe10_D = [0.8,0.8,0.8]
    C_pe10_E = [-0.3,-0.5,-0.7]
    y = [0.25, 1, 5]

    # Zone D Windward side
    C_pe10D = np.interp(ratio, y, C_pe10_D)

    # Zone E Leeward side
    C_pe10E = np.interp(ratio,y, C_pe10_E)


    # Lack of correlation coefficient

    y = [1,5]
    x = [0.85,1]

    lackOfCorrelationCoeff = np.interp(ratio,y, x)

    # Calculation of different loads #

    #########################################################################################
    # First case

    if heightOfTheBuilding <= paralellToTheWindSideOfTheBuilding:

        z_e = heightOfTheBuilding

        if z_e <= z_min:
            C_r = k_r*math.log(z_min/z_0)
            I_v = turbulanceFactor / (orographyFactor*math.log(z_min/z_0))
        else:
            C_r = k_r*math.log(z_e/z_0)
            I_v = turbulanceFactor / (orographyFactor*math.log(z_e/z_0))

        v_m = v_b * C_r * orographyFactor
        peakVelocityPressure = ((1+7* I_v)*0.5*1.25*v_m**2)/1000
        windWardPressure = C_pe10D * peakVelocityPressure
        leewardPressure = abs(C_pe10E * peakVelocityPressure)
        w_net = windWardPressure + leewardPressure
        f_net = crosswindside*w_net*C_s*C_d
        F = f_net * (heightOfTheBuilding)*lackOfCorrelationCoeff
        BM = F*heightOfTheBuilding/2
        lateralLineLoad = F/heightOfTheBuilding

        finalWindload = lateralLineLoad / crosswindside

        return finalWindload

    #####################################################################################
    # Second case

    elif heightOfTheBuilding > 2 * paralellToTheWindSideOfTheBuilding:

        firstZoneHeight = paralellToTheWindSideOfTheBuilding
        secondZoneHeight = heightOfTheBuilding - 2 * paralellToTheWindSideOfTheBuilding
        thirdZoneHeight = paralellToTheWindSideOfTheBuilding

        # firstZone #

        z_e1 = firstZoneHeight

        if z_e1 <= z_min:
            C_r = k_r * math.log(z_min / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_min / z_0))
        else:
            C_r = k_r * math.log(z_e1 / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_e1 / z_0))

        v_m = v_b * C_r * orographyFactor
        peakVelocityPressure = ((1 + 7 * I_v) * 0.5 * 1.25 * v_m ** 2) / 1000
        windWardPressure = C_pe10D * peakVelocityPressure
        leewardPressure = abs(C_pe10E * peakVelocityPressure)
        w_net = windWardPressure + leewardPressure
        f_net = crosswindside * w_net * C_s * C_d
        F = f_net * (heightOfTheBuilding) * lackOfCorrelationCoeff
        BM = F * heightOfTheBuilding / 2
        lateralLineLoad1 = F / heightOfTheBuilding

        # secondZone #

        z_e2 = secondZoneHeight + paralellToTheWindSideOfTheBuilding

        if z_e2 <= z_min:
            C_r = k_r * math.log(z_min / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_min / z_0))
        else:
            C_r = k_r * math.log(z_e2 / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_e2 / z_0))

        v_m = v_b * C_r * orographyFactor
        peakVelocityPressure = ((1 + 7 * I_v) * 0.5 * 1.25 * v_m ** 2) / 1000
        windWardPressure = C_pe10D * peakVelocityPressure
        leewardPressure = abs(C_pe10E * peakVelocityPressure)
        w_net = windWardPressure + leewardPressure
        f_net = crosswindside * w_net * C_s * C_d
        F = f_net * (heightOfTheBuilding) * lackOfCorrelationCoeff
        BM = F * heightOfTheBuilding / 2
        lateralLineLoad2 = F / heightOfTheBuilding

        # thirdZone #

        z_e3 = heightOfTheBuilding

        if z_e3 <= z_min:
            C_r = k_r * math.log(z_min / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_min / z_0))
        else:
            C_r = k_r * math.log(z_e3 / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_e3 / z_0))

        v_m = v_b * C_r * orographyFactor
        peakVelocityPressure = ((1 + 7 * I_v) * 0.5 * 1.25 * v_m ** 2) / 1000
        windWardPressure = C_pe10D * peakVelocityPressure
        leewardPressure = abs(C_pe10E * peakVelocityPressure)
        w_net = windWardPressure + leewardPressure
        f_net = crosswindside * w_net * C_s * C_d
        F = f_net * (heightOfTheBuilding) * lackOfCorrelationCoeff
        BM = F * heightOfTheBuilding / 2
        lateralLineLoad3 = F / heightOfTheBuilding

        # modifying line load

        baseShear = lateralLineLoad1 * firstZoneHeight + lateralLineLoad2 * secondZoneHeight + lateralLineLoad3 * thirdZoneHeight
        baseMoment = lateralLineLoad1 * firstZoneHeight * z_e1/2 + lateralLineLoad2 * secondZoneHeight * (z_e1 + secondZoneHeight/2) + lateralLineLoad3 * thirdZoneHeight * (z_e2+thirdZoneHeight/2)
        lineloadBaseShear = baseShear/heightOfTheBuilding
        momentDueToLineLoad = lineloadBaseShear * (heightOfTheBuilding**2)/2
        modifyingFactor = baseMoment/momentDueToLineLoad
        averageLineLoad = lineloadBaseShear * modifyingFactor

        finalWindload = averageLineLoad / crosswindside

        return (finalWindload)
    ###########################################################################################
    # Third case

    else:

        firstZoneHeight = paralellToTheWindSideOfTheBuilding
        secondZoneHeight = heightOfTheBuilding - paralellToTheWindSideOfTheBuilding

        # firstZone #

        z_e1 = firstZoneHeight

        if z_e1 <= z_min:
            C_r = k_r * math.log(z_min / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_min / z_0))
        else:
            C_r = k_r * math.log(z_e1 / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_e1 / z_0))

        v_m = v_b * C_r * orographyFactor
        peakVelocityPressure = ((1 + 7 * I_v) * 0.5 * 1.25 * v_m ** 2) / 1000
        windWardPressure = C_pe10D * peakVelocityPressure
        leewardPressure = abs(C_pe10E * peakVelocityPressure)
        w_net = windWardPressure + leewardPressure
        f_net = crosswindside * w_net * C_s * C_d
        F = f_net * (heightOfTheBuilding) * lackOfCorrelationCoeff
        BM = F * heightOfTheBuilding / 2
        lateralLineLoad1 = F / heightOfTheBuilding

        # secondZone #

        z_e2 = heightOfTheBuilding

        if z_e2 <= z_min:
            C_r = k_r * math.log(z_min / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_min / z_0))
        else:
            C_r = k_r * math.log(z_e2 / z_0)
            I_v = turbulanceFactor / (orographyFactor * math.log(z_e2 / z_0))

        v_m = v_b * C_r * orographyFactor
        peakVelocityPressure = ((1 + 7 * I_v) * 0.5 * 1.25 * v_m ** 2) / 1000
        windWardPressure = C_pe10D * peakVelocityPressure
        leewardPressure = abs(C_pe10E * peakVelocityPressure)
        w_net = windWardPressure + leewardPressure
        f_net = crosswindside * w_net * C_s * C_d
        F = f_net * (heightOfTheBuilding) * lackOfCorrelationCoeff
        BM = F * heightOfTheBuilding / 2
        lateralLineLoad2 = F / heightOfTheBuilding

        #modifying

        baseShear = lateralLineLoad1 * firstZoneHeight + lateralLineLoad2 * secondZoneHeight
        baseMoment = lateralLineLoad1 * firstZoneHeight * z_e1/2 + lateralLineLoad2 * secondZoneHeight * (z_e1 + secondZoneHeight/2)
        lineloadBaseShear = baseShear/heightOfTheBuilding
        momentDueToLineLoad = lineloadBaseShear * (heightOfTheBuilding**2)/2
        modifyingFactor = baseMoment/momentDueToLineLoad
        averageLineLoad = lineloadBaseShear * modifyingFactor

        finalWindload = averageLineLoad/ crosswindside

        return(finalWindload)


if __name__ == '__main__':
    print(windFunction())


