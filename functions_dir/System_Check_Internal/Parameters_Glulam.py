
def Parameters_Glulam(b, h, M_1, M_2, F):
    f_mk = 30
    f_t0k = 19.5
    f_t90k = 0.5
    f_c0k = 24.5
    f_c90k = 2.5
    f_vk = 3.5
    f_rgk = 1.2
    E_5 = 10800
    E_mean = 13000

    gamma_M = 1.15
    k_mod = 0.8

    A = b * h

    ## Checks ##

    if h < 600:
        k_h = min(1.1, (600 / h) ** 0.1)
    else:
        k_h = 1

    f_md = f_mk * k_mod * k_h / gamma_M
    f_t0d = f_t0k * k_mod / gamma_M
    f_t90d = f_t90k * k_mod / gamma_M
    f_c0d = f_c0k * k_mod / gamma_M
    f_c90d = f_c90k * k_mod / gamma_M
    f_vd = f_vk * k_mod / gamma_M

    ##Stresses##

    sigma_myd_1 = 6 * M_1 / (b * h ** 2)
    sigma_myd_2 = 6 * M_2 / (b * h ** 2)
    sigma_axial = -F / A

    return (f_md, f_vd, f_c90d, f_c0d, f_t90d, f_t0d, sigma_axial, sigma_myd_1, sigma_myd_2, E_5, E_mean, A, f_c0k)