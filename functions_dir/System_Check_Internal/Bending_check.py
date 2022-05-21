
def Bending_check(M_1, M_2, b, h, F, A, f_md, f_c0d, f_t0d,load, l,spacing, variant):


    if variant == "beams":
        M_3 = (-load * spacing * l ** 2 / 8) * 10 ** -3

        sigma_myd_1 = 6 * M_1 / (b * h ** 2)
        sigma_myd_2 = 6 * M_2 / (b * h ** 2)
        sigma_myd_3 = 6 * M_3 / (b * h ** 2)

        sigma_axial = -F / A

    ## Bending Control and axial controls##

    ## Aksialtrykk og moment som gir trykk##

        if sigma_axial < 0 and min(sigma_myd_1, sigma_myd_2, sigma_myd_3) < 0:
            Bending_Compression = abs(min(sigma_myd_1, sigma_myd_2)) / f_md + abs(sigma_axial) / f_c0d

            bending_utilization = Bending_Compression
            bending_utilizationtype = "Compression and moment"

        ## Aksialstrekk og moment som gir strekk##

        elif sigma_axial > 0 and max(sigma_myd_1, sigma_myd_2, sigma_myd_3) > 0:
            Bending_Tension = abs(max(sigma_myd_1, sigma_myd_2, sigma_myd_3)) / f_md + abs(sigma_axial) / f_t0d

            bending_utilization = Bending_Tension
            bending_utilizationtype = "Tension and moment"

        elif sigma_axial < 0:
            Compression_axial = (abs(sigma_axial) / f_c0d)
            bending_utilization = Compression_axial
            bending_utilizationtype = "Pure Compression"


        else:
            Tension_axial = abs(sigma_axial) / f_t0d
            bending_utilization = Tension_axial
            bending_utilizationtype = "Pure Tension"

        Pure_bending = max(abs(sigma_myd_1), abs(sigma_myd_2), abs(sigma_myd_3)) / f_md

        if Pure_bending > bending_utilization:
            bending_utilization = Pure_bending
            bending_utilizationtype = "Pure Bending"

    else:
        sigma_myd_1 = 6 * M_1 / (b * h ** 2)
        sigma_myd_2 = 6 * M_2 / (b * h ** 2)
        sigma_axial = -F / A

        ## Bending Control and axial controls##

            ## Aksialtrykk og moment som gir trykk##

        if sigma_axial < 0 and min(sigma_myd_1, sigma_myd_2) < 0:
            Bending_Compression = abs(min(sigma_myd_1, sigma_myd_2)) / f_md + abs(sigma_axial) / f_c0d

            bending_utilization = Bending_Compression
            bending_utilizationtype = "Compression and moment"

        ## Aksialstrekk og moment som gir strekk##

        elif sigma_axial > 0 and max(sigma_myd_1, sigma_myd_2 ) > 0:
            Bending_Tension = abs(max(sigma_myd_1, sigma_myd_2) )/ f_md + abs(sigma_axial) / f_t0d

            bending_utilization = Bending_Tension
            bending_utilizationtype = "Tension and moment"


        elif sigma_axial < 0:
                Compression_axial = abs(sigma_axial) / f_c0d
                bending_utilization = Compression_axial
                bending_utilizationtype = "Pure Compression"


        else:
                Tension_axial = abs(sigma_axial) / f_t0d
                bending_utilization = Tension_axial
                bending_utilizationtype = "Pure Tension"


        Pure_bending = max(abs(sigma_myd_1), abs(sigma_myd_2)) / f_md

        if Pure_bending > bending_utilization:
                bending_utilization = Pure_bending
                bending_utilizationtype = "Pure Bending"

    return (bending_utilization, bending_utilizationtype)



