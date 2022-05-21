def Shear_check(b,h,f_vd, V):
    k_cr = 0.8
    b_ef = b * 0.8
    tau_vd = 1.5 * V / (b_ef * h)
    checkShear = tau_vd / f_vd

    shear_utilization = abs(checkShear)
    shear_utilizationtype = "shear"

    return(shear_utilization, shear_utilizationtype)
