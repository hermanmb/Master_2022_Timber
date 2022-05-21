def Check_Walls(l, b, N, h):

    f_m_k = 26.4
    f_c_0_k = 26.4
    N_ed = N/2
    b = b/2

    E_0_mean = 9169
    E_0_05 = 7641
    G_r_mean = 100


    t_1 = b/5
    t_2 = b/5
    t_3 = b/5
    t_4 = b/5
    t_5 = b/5
    a_1 = t_1+t_2/2+t_5/2
    a_2 = t_3/2+t_2/2
    a_3 = 0
    a_4 = t_3/2+t_4/2
    a_5 = t_4+t_3/2+t_5/2

    A_x_net = (t_1+t_3+t_5)*h

    gamma_M = 1.15
    k_mod = 0.8


    gamma_1 = 1/(1+3.14**2*E_0_mean*t_1*t_2/l**2/G_r_mean)
    gamma_3 = 1
    gamma_5 = 1/(1+3.14**2*E_0_mean*t_1*t_2/l**2/G_r_mean)

    I_x_ef = h*((t_1**3/12)+(t_3**3/12)+(t_5**3/12)+(gamma_1*t_1*a_1**2)+gamma_3*t_3*a_3**2+(gamma_5*t_5*a_5**2))
    i_x_ef = (I_x_ef/A_x_net)**0.5
    lambda_y = l/i_x_ef
    lambda_rel_y = lambda_y/3.14*(f_m_k/E_0_05)**0.5
    k_y = 0.5*(1+ 0.1*(lambda_rel_y-0.3)+lambda_rel_y**2)
    k_c_y = 1/(k_y+(k_y**2-lambda_rel_y**2)**0.5)

    sigma_c_x_d = N_ed/A_x_net
    tollerance = k_mod/gamma_M*f_c_0_k*k_c_y
    wall_utilization = sigma_c_x_d/tollerance
    wall_utilization_type = "Buckling about weak axis"

    return (wall_utilization, wall_utilization_type)





