
def Buckling_check(l,b,  h, f_c0k, E_5, f_c0d, sigma_axial, sigma_myd_1, sigma_myd_2, f_md):

    L_k_y = l
    lamda_y = L_k_y / (((h**2)/12)**0.5)
    lamda_rel_y = lamda_y / 3.14 * (f_c0k / E_5)**0.5
    if lamda_rel_y < 0.3:
        buckling_utilization_y = 0
    else:
        beta_c = 0.1
        k_y = 0.5 * (1 + beta_c * (lamda_rel_y - 0.3) + lamda_rel_y ** 2)
        k_c_y = 0.8 #1 / (k_y + (k_y ** 2 - lamda_rel_y ** 2) ** 0.5)
        buckling_utilization_y = sigma_axial / (k_c_y * f_c0d) + abs(max((sigma_myd_1), abs(sigma_myd_2))) / f_md
        buckling_utilization_y = abs(buckling_utilization_y)

    ## Buckling out of plane ##

    L_k_z = l
    lamda_z = L_k_z / (((b**2)/12)**0.5)
    lamda_rel_z = lamda_z / 3.14 * (f_c0k / E_5)**0.5
    if lamda_rel_z < 0.3:
        buckling_utilization_z = 0
    else:
        beta_c = 0.1
        k_z = 0.5 * (1 + beta_c * (lamda_rel_z - 0.3) + lamda_rel_z ** 2)
        k_c_z = 1 / (k_z + (k_z ** 2 - lamda_rel_z ** 2) ** 0.5)
        buckling_utilization_z = sigma_axial / (k_c_z * f_c0d) + abs(max((sigma_myd_1), abs(sigma_myd_2))) / f_md * 0.7
        buckling_utilization_z = abs(buckling_utilization_z)

    if buckling_utilization_z > buckling_utilization_y:
        buckling_utilization = buckling_utilization_z
        buckling_utilizationtype = "buckling about weak axis"
    else:
        buckling_utilization = buckling_utilization_y
        buckling_utilizationtype = "buckling about strong axis"

    return(buckling_utilization, buckling_utilizationtype)


def Buckling_check_Outrigger(l, b, h, f_c0k, E_5, f_c0d, sigma_axial, sigma_myd_1, sigma_myd_2, f_md):

    L_k_y = l
    lamda_y = L_k_y / (((h**2)/12)**0.5)
    lamda_rel_y = lamda_y / 3.14 * (f_c0k / E_5)**0.5
    if lamda_rel_y < 0.3:
        buckling_utilization_y = 0
    else:
        beta_c = 0.1
        k_y = 0.5 * (1 + beta_c * (lamda_rel_y - 0.3) + lamda_rel_y ** 2)
        k_c_y = 1 / (k_y + (k_y ** 2 - lamda_rel_y ** 2) ** 0.5)
        buckling_utilization_y = sigma_axial / (k_c_y * f_c0d) + abs(max((sigma_myd_1), abs(sigma_myd_2))) / f_md
        buckling_utilization_y = abs(buckling_utilization_y)

    ## Buckling out of plane ##

    L_k_z = l
    lamda_z = L_k_z / (((b**2)/12)**0.5)
    lamda_rel_z = lamda_z / 3.14 * (f_c0k / E_5)**0.5
    if lamda_rel_z < 0.3:
        buckling_utilization_z = 0
    else:
        beta_c = 0.1
        k_z = 0.5 * (1 + beta_c * (lamda_rel_z - 0.3) + lamda_rel_z ** 2)
        k_c_z = 1 / (k_z + (k_z ** 2 - lamda_rel_z ** 2) ** 0.5)
        buckling_utilization_z = sigma_axial / (k_c_z * f_c0d) + abs(max((sigma_myd_1), abs(sigma_myd_2))) / f_md * 0.7
        buckling_utilization_z = abs(buckling_utilization_z)

    if buckling_utilization_z > buckling_utilization_y:
        buckling_utilization = buckling_utilization_z
        buckling_utilizationtype = "buckling about weak axis"
    else:
        buckling_utilization = buckling_utilization_y
        buckling_utilizationtype = "buckling about strong axis"

    return(buckling_utilization, buckling_utilizationtype)