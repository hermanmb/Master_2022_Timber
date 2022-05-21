def displayForces(forceElements,floor_h,L_bay,system):

    if system == 3:
        L_diagonal = (floor_h ** 2 + (L_bay / 2) ** 2) ** 0.5
        cosine = (L_bay / 2) / L_diagonal
    else:
        L_diagonal = (floor_h ** 2 + L_bay ** 2) ** 0.5
        cosine = (L_bay) / L_diagonal

    keys = ['columns', 'beams', 'ORelements', 'walls']

    for i, key in enumerate(keys):
        print('########################')
        print(key)
        print('*from left to right')
        elements = forceElements[key]
        for element in elements.keys():
            if i == 2:
                print('------------------------')
                print('|' + '\t' + key[:-1] + " " + str(element))
                print('------------------------')
                forces = elements[element]
                Fx = forces[1]/1000
                Fy = forces[0]/1000
                N = round(Fy/cosine,2)

                print(f'| N = {N} kN')
                print(f'| Nx = {Fx} kN')
                print(f'| Ny = {Fy} kNm')
                print()

            elif i == 1:
                print('------------------------')
                print('|' + '\t' + key[:-1] + " " + str(element))
                print('------------------------')
                forces = elements[element]
                Fx = forces[0] / 1000
                Fy = forces[1] / 1000
                Mz1 = int(forces[2] / 1000) / 1000
                Mz2 = int(forces[5] / 1000) / 1000

                print(f'| Fx = {Fx} kN')
                print(f'| Fy = {Fy} kN')
                print(f'| Mz1 = {Mz1} kNm')
                print(f'| Mz2 = {Mz2} kNm')
                print()

            else:
                print('------------------------')
                print('|'+'\t'+key[:-1]+" "+str(element))
                print('------------------------')
                forces = elements[element]
                Fx = forces[1]/1000
                Fy = forces[0]/1000
                Mz1 = int(forces[2]/1000)/1000
                Mz2 = int(forces[5]/1000)/1000

                print(f'| Fx = {Fx} kN')
                print(f'| Fy = {Fy} kN')
                print(f'| Mz1 = {Mz1} kNm')
                print(f'| Mz2 = {Mz2} kNm')

                print()
    print('########################')

    '''
    #####################
    COLUMNS
    *from left to right
    ---------------------
    |   column 1        |
    ---------------------
    | Fx = {forces1} kN |
    | Fy = {forces1} kN |
    | Mz = {forces1} kNm |
    '''


def getBeamMoments(forceElements):

    moments = []
    keys = ['columns', 'beams', 'ORelements', 'walls']

    elements = forceElements['beams']
    for element in elements.keys():
        forces = elements[element]
        Mz1 = int(forces[2] / 1000) / 1000
        Mz2 = int(forces[5] / 1000) / 1000
        moments.append(Mz1)
        moments.append(Mz2)

    return moments