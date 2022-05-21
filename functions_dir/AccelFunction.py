from scipy.interpolate import interp1d
import math

from functions_dir.ExponentFunction import *

def accelFunction(numBay, L_bay, numFloor, floor_h, spacing, numFrames, freq, mass, eigenVector,damp = 0.019,Vb0 = 26):
    # Inputs
    n = numFloor # number of stories
    H = floor_h*n/1000  # Total heigth
    b = (numFrames-1)*spacing/1000  # Cross wind dimension of the building in m
    d = L_bay*(numBay)/1000  # Parallel to the wind dimension of the building in m

    Kr = 0.24  # Terrain factor from NA
      # Fundamental Basic Wind Veolcity V_b_,0
    Cdir = 1  # Directional factor Cdir
    Cseason = 1  # Seasonal factor Cseason
    # n
    # k
    Cprop = 0.73  # Return period in years
    C0 = 1  # Orography factor
    Kl = 1  # Turbulenace factor
    TF = 4  # Terrain category
    r = 0  # Radius of bulding edges
    rho = 1.25  # Air density rho
    Zt = 200  # Z_t: Recommended value = 200 m
    Lt = 300  # L_t: Recommended value = 300 m

    freq = freq  # First mode fundamental frequency n_1_x
    m = mass  # All the masses

      # Strudtural Damping

    phi = eigenVector[-2]  # Normalized mode sahpe at the point of interest phi

    exp = findingBestExponent(eigenVector, numFloor)

    Z0 = 1
    Zmin = 16

    ##################################Calculations################################

    i = 0
    Zs = max(0.6 * H, Zmin)
    Vb = Vb0 * Cdir * Cseason * Cprop
    Crzs = Kr * (np.log(max(Zmin, Zs) / Z0))
    Vmzs = Vb * Crzs
    Ivzs = Kl / (C0 * np.log(max(Zmin, Zs) / Z0))
    alpha = 0.67 + 0.05 * np.log(Z0)
    Lzs = Lt * (max(Zmin, Zs) / 200) ** alpha
    db = (0.1, 0.2, 0.6, 0.7, 1, 2, 5, 10, 50, 1000)
    ct0 = (2, 2, 2.35, 2.4, 2.1, 1.65, 1, 0.9, 0.9, 0.9)
    f1 = interp1d(db, ct0)
    x = d / b
    Ct0 = f1(x) + 0

    if r / b >= 0.2:
        opsai_r = 0.2
    else:
        opsai_r = 1 - 2.5 * (r / d)

    if H >= 50:
        lamda = min(1.4 * H / b, 70)
    elif H < 15:
        lamda = min(2 * H / b, 70)
    else:
        f2 = interp1d((50, 15), (min(1.4 * H / b, 70), min(2 * H / b, 70)))
        lamda = f2(H) + 0

    if lamda <= 1:
        opsai_lamda = 0.6
    elif lamda > 200:
        opsai_lamda = 7
    else:
        f3 = interp1d((1, 10, 70, 200), (0.6, 0.7, 0.933, 1))
        opsai_lamda = f3(lamda) + 0

    Cf = Ct0 * opsai_r * opsai_lamda

    B = ((1 + 0.9 * ((b + H) / Lzs) ** 0.63) ** -1) ** 0.5
    fL = freq * Lzs / Vmzs
    SL = 6.8 * fL / (1 + 10.2 * fL) ** (5 / 3)

    me = m / H   # 11758.5
    damp_a = (Cf * rho * Vmzs * b) / (2 * freq * (me))
    damp_s = 2 * math.pi * damp / (1 + damp ** 2) ** -0.5
    damp_L = damp_a + damp_s
    eita_h = 4.6 * H * fL / Lzs
    eita_b = 4.6 * b * fL / Lzs
    Rh = 1 / eita_h - (1 / (2 * eita_h ** 2)) * (1 - math.exp(-2 * eita_h))
    Rb = 1 / eita_b - (1 / (2 * eita_b ** 2)) * (1 - math.exp(-2 * eita_b))
    R = ((math.pi ** 2) * SL * Rh * Rb / (2 * damp_L)) ** 0.5
    Kx = ((2 * exp + 1) * ((exp + 1) * (np.log(Zs / Z0) + 0.5) - 1)) / (((exp + 1) ** 2) * np.log(Zs / Z0))
    sigma = ((Cf * rho * b * Ivzs * Vmzs ** 2) / me) * R * Kx * phi
    Kp = max(((2 * np.log(freq * 600)) ** 0.5) + 0.6 / (2 * np.log(freq * 600)) ** 0.5, 3)
    CsCd = (1 + 2 * Kp * Ivzs * (B ** 2 + R ** 2) ** 0.5) / (1 + 7 * Ivzs)
    acc = Kp * sigma

    return acc

