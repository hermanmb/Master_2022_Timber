
from model_dir.elements import StandardElement
from functions_dir.System_Check_Internal.Shear_check import *
from functions_dir.System_Check_Internal.Parameters_Glulam import *
from functions_dir.System_Check_Internal.Bending_check import *
from functions_dir.System_Check_Internal.Buckling_check import *
from functions_dir.System_Check_Internal.Check_Walls import *



def Design_Check (elements, forceelement,floor_h, num_floor, L_bay, load,spacing):

    prinT = False

    bending_utilization_last_beam = 0
    shear_utilization_last_beam = 0

    bending_utilization_last_column = 0
    shear_utilization_last_column = 0
    buckling_utilization_last_column = 0

    bending_utilization_last_OR = 0
    buckling_utilization_last_OR = 0

    wall_utilization_last_wall = 0

    beam = [None, None]
    column = [None, None, None]
    wall = [None]
    outrigger = [None, None]

    ## Loop ##

    for variant in forceelement.keys():

        forces = forceelement[variant]

        for element in forces.keys():
            element_forces = forces[element]

        ####################################Start#############################################################


            ##################################   Beams     ######################################################
            #####################################################################################################

            if variant == "beams":

                b = elements.getBb()
                h = elements.getHb()

                l = L_bay

                F = element_forces[0]
                V = (load*L_bay/1000*spacing/1000)/2*1000
                M_1 = element_forces[2]
                M_2 = element_forces[5]

                f_md, f_vd, f_c90d, f_c0d, f_t90d, f_t0d, sigma_axial, sigma_myd_1, sigma_myd_2, E_5, E_mean, A, f_c0k = Parameters_Glulam(b,h,M_1, M_2, F)

                shear_utilization, shear_utilizationtype = Shear_check(b,h,f_vd,V)

                bending_utilization, bending_utilizationtype = Bending_check(M_1, M_2, b, h, F, A, f_md, f_c0d, f_t0d, load, l, spacing, variant)

                buckling_utilization, buckling_utilizationtype = Buckling_check(l,b, h, f_c0k, E_5, f_c0d, sigma_axial, sigma_myd_1, sigma_myd_2, f_md)


                if bending_utilization > bending_utilization_last_beam:
                    bending_utilization_last_beam = bending_utilization

                    BB = {"Type:" : variant, "Element:" : element, "utilizationtype:" : bending_utilizationtype, "ratio:" : bending_utilization}

                    beam[0] = ((bending_utilizationtype, bending_utilization))

                if shear_utilization > shear_utilization_last_beam:
                    shear_utilization_last_beam = shear_utilization

                    BS = {"Type:" : variant, "Element:" : element, "utilizationtype:" : shear_utilizationtype, "ratio:" : shear_utilization}

                    beam[1] = ((shear_utilizationtype, shear_utilization))


            ##################################   Columns   #####################################################
            ####################################################################################################

            if variant == "columns":

                b = elements.getBc()
                h = elements.getHc()

                l = floor_h

                F = element_forces[1]
                V = element_forces[0]
                M_1 = element_forces[2]
                M_2 = element_forces[5]

                f_md, f_vd, f_c90d, f_c0d, f_t90d, f_t0d, sigma_axial, sigma_myd_1, sigma_myd_2, E_5, E_mean, A, f_c0k = Parameters_Glulam(b,h,M_1, M_2, F)

                shear_utilization, shear_utilizationtype = Shear_check(b,h,f_vd,V)

                bending_utilization, bending_utilizationtype = Bending_check(M_1, M_2, b, h, F, A, f_md, f_c0d, f_t0d, l, load, spacing, variant)

                buckling_utilization, buckling_utilizationtype = Buckling_check(l,b, h, f_c0k, E_5, f_c0d, sigma_axial, sigma_myd_1, sigma_myd_2, f_md)


                if abs(buckling_utilization) > buckling_utilization_last_column:
                    buckling_utilization_last_column = buckling_utilization

                    CBU = {"Type:" : variant, "Element:" : element, "utilizationtype:" : buckling_utilizationtype, "ratio:" : buckling_utilization}

                    column[0] = ((buckling_utilizationtype,buckling_utilization))

                if bending_utilization > bending_utilization_last_column:
                    bending_utilization_last_column = bending_utilization

                    CB = {"Type:" : variant, "Element:" : element, "utilizationtype:" : bending_utilizationtype, "ratio:" : bending_utilization}

                    column[1] = ((bending_utilizationtype, bending_utilization))

                if shear_utilization > shear_utilization_last_column:
                    shear_utilization_last_column = shear_utilization

                    CS =  {"Type:" : variant, "Element:" : element, "utilizationtype:" : shear_utilizationtype, "ratio:" : shear_utilization}

                    column[2] = ((shear_utilizationtype, shear_utilization))

            ##################################   OR_elements   ###################################################
            ######################################################################################################

            if variant == "ORelements":

                b = elements.getBt()
                h = elements.getHt()

                l = (L_bay**2+floor_h**2)**0.5
                cosine = (L_bay) / l

                F = element_forces[0]/cosine
                V = 0
                M_1 = 0
                M_2 = 0


                f_md, f_vd, f_c90d, f_c0d, f_t90d, f_t0d, sigma_axial, sigma_myd_1, sigma_myd_2, E_5, E_mean, A, f_c0k = Parameters_Glulam(b,h,M_1, M_2, F)

                ## shear_utilization, shear_utilizationtype = Shear_check(b,h,f_vd,V)

                bending_utilization, bending_utilizationtype = Bending_check(M_1, M_2, b, h, F, A, f_md, f_c0d, f_t0d, load, l, spacing, variant)

                buckling_utilization, buckling_utilizationtype = Buckling_check_Outrigger(l, b, h, f_c0k, E_5, f_c0d, sigma_axial, sigma_myd_1, sigma_myd_2, f_md)


                if buckling_utilization > buckling_utilization_last_OR:
                    buckling_utilization_last_OR = buckling_utilization

                    ORBU = {"Type:" : variant, "Element:" : element, "utilizationtype:" : buckling_utilizationtype, "ratio:" : buckling_utilization}

                    outrigger[0] = ((buckling_utilizationtype, buckling_utilization))


                if bending_utilization > bending_utilization_last_OR:
                    bending_utilization_last_OR = bending_utilization_last_OR

                    ORB = {"Type:" : variant, "Element:" : element, "utilizationtype:" : bending_utilizationtype, "ratio:" : bending_utilization}

                    outrigger[1] = ((bending_utilizationtype, bending_utilization))

            if variant == "walls":
                b = elements.getBw()
                h = elements.getHw()

                l = floor_h

                F = element_forces[1]
                V = element_forces[0]
                M_1 = element_forces[2]
                M_2 = element_forces[5]

                wall_utilization, wall_utilizationtype = Check_Walls(l, b, F, h)

                if wall_utilization > wall_utilization_last_wall:
                    wall_utilization_last_wall = wall_utilization

                    WBU = {"Type:" : variant, "Element:" : element, "utilizationtype:" : wall_utilizationtype, "ratio:" : wall_utilization}

                    wall[0] = ((wall_utilizationtype, wall_utilization))

    if (prinT):
        print(num_floor)
        print(CB)
        print(CS)
        print(CBU)
        print(BB)
        print(BS)
        print(WBU)

        print("#####################################")

    return (beam, column, wall, outrigger)




if __name__ == '__main__':
    elements = StandardElement()

    Bank = {}

    Bank["ORelements"] = []
    Bank["beams"] = []
    Bank["columns"] = []
    Bank["walls"] = []



    #forceelement = {'beams': {'20131': [35400, -11072, -5321228, -35400, 11072, -16822490], '20132': [303987, 9166, -431553, -303987, -9166, 29417798], '20141': [319396, -14435, -30973254, -319396, 14435, -14676068], '20142': [170992, 10466, 14676068, -170992, -10466, 18424057], '20151': [214155, -8710, -40171897, -214155, 8710, 12625448], '20152': [-375796, -9169, 4628594, 375796, 9169, -22966829], '2010': [-199594, -112, -41417138, 199594, 112, 40839947], '2011': [-285912, -2349, -64543514, 285912, 2349, 49688999], '2012': [54767, -8624, -60412929, -54767, 8624, 15889498]}, 'columns': {'1005': [106078, 795533, -411864255, -106078, -795533, 40591170], '1015': [13242, 1184646, -32394704, -13242, -1184646, -13951272], '1025': [15767, 1174502, -23214984, -15767, -1174502, -31971121], '1035': [238962, 860427, -581308439, -238962, -860427, -255057398]}, 'ORelements': {'6001': [188939, 188939, 0, -188939, -188939, 0], '6002': [-79648, 79648, 0, 79648, -79648, 0], '6003': [-7198, -7198, 0, 7198, 7198, 0], '6004': [141206, -141206, 0, -141206, 141206, 0], '6005': [-250678, -250678, 0, 250678, 250678, 0], '6006': [339273, -339273, 0, -339273, 339273, 0]}}
    #Design_Check(elements, forceelement, floor_h= 3500, num_floor=12, L_bay=7000)
