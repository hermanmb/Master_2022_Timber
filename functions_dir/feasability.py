import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FormatStrFormatter


def feasabilityPlot_singleOutrigger(ordbok):
    fig, ax = plt.subplots(figsize=(8, 6), dpi=500)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xticks([0.06, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5])
    ax.set_yticks([0.02, 0.04, 0.06, 0.08, 0.1, 0.14, 0.2, 0.3, 0.5])
    ax.set_xlabel('Fundamental frequency in Hz', fontsize=14)
    ax.set_ylabel('Acceleration in m/s' + '$^2$', fontsize=14)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # Plot ISO criteria
    # The numbers
    ldiagx = [0.06, 1]
    ldiagy1 = [0.21, 0.06]
    ldiagy2 = [0.14, 0.04]
    horix = [1, 2]
    horiy1 = [0.06, 0.06]
    horiy2 = [0.04, 0.04]
    hdiagx = [2, 5]
    hdiagy1 = [0.06, 0.15]
    hdiagy2 = [0.04, 0.1]
    yline = [0, 0.5]
    minx = [0.06, 0.06]
    maxx = [5, 5]
    xline = [0.06, 5]
    miny = [0, 0]
    maxy = [0.5, 0.5]

    # Plot offices
    ax.plot(ldiagx, ldiagy1, 'k-', linewidth=1, label='Offices')
    ax.plot(horix, horiy1, 'k-', linewidth=1)
    ax.plot(hdiagx, hdiagy1, 'k-', linewidth=1)

    # Plot residential
    ax.plot(ldiagx, ldiagy2, 'k--', linewidth=1.8, label='Residential')
    ax.plot(horix, horiy2, 'k--', linewidth=1.8)
    ax.plot(hdiagx, hdiagy2, 'k--', linewidth=1.8)

    # Formatting the axis '%.2f'
    ax.set_xlim(left=0.06, right=5)
    ax.set_ylim(bottom=0.02, top=0.5)
    ax.grid()

    length = len(ordbok)
    for floor, i in enumerate(ordbok):
        freq = i[0]
        acc = i[1]
        if floor == 0:
            plt.scatter(freq, acc, alpha=1, marker='*',s=100, label= "no OR")
        elif floor == (length//2 -2) :
            plt.scatter(freq, acc, alpha=1, label="floor: " + str(floor + 1))
        elif floor == (length // 2 -1):
            plt.scatter(freq, acc, alpha=1, label="floor: " + str(floor + 1))
        elif floor == (length // 2 ):
            plt.scatter(freq, acc, alpha=1, label="floor: " + str(floor + 1))
        else:
            plt.scatter(freq, acc, alpha=0.3)


    plt.legend(loc = 1,title='Basisframe 10 floors')
    plt.savefig('placement_single_outrigger.jpg',dpi=500)
    plt.show()

def feasabilityPlot_innerVSoutter(ordbok):
    fig, ax = plt.subplots(figsize=(8, 6), dpi=500)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xticks([0.06, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5])
    ax.set_yticks([0.02, 0.04, 0.06, 0.08, 0.1, 0.14, 0.2, 0.3, 0.5])
    ax.set_xlabel('Fundamental frequency in Hz', fontsize=14)
    ax.set_ylabel('Acceleration in m/s' + '$^2$', fontsize=14)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # Plot ISO criteria
    # The numbers
    ldiagx = [0.06, 1]
    ldiagy1 = [0.21, 0.06]
    ldiagy2 = [0.14, 0.04]
    horix = [1, 2]
    horiy1 = [0.06, 0.06]
    horiy2 = [0.04, 0.04]
    hdiagx = [2, 5]
    hdiagy1 = [0.06, 0.15]
    hdiagy2 = [0.04, 0.1]
    yline = [0, 0.5]
    minx = [0.06, 0.06]
    maxx = [5, 5]
    xline = [0.06, 5]
    miny = [0, 0]
    maxy = [0.5, 0.5]

    # Plot offices
    ax.plot(ldiagx, ldiagy1, 'k-', linewidth=1, label='Offices')
    ax.plot(horix, horiy1, 'k-', linewidth=1)
    ax.plot(hdiagx, hdiagy1, 'k-', linewidth=1)

    # Plot residential
    ax.plot(ldiagx, ldiagy2, 'k--', linewidth=1.8, label='Residential')
    ax.plot(horix, horiy2, 'k--', linewidth=1.8)
    ax.plot(hdiagx, hdiagy2, 'k--', linewidth=1.8)

    # Formatting the axis '%.2f'
    ax.set_xlim(left=0.06, right=5)
    ax.set_ylim(bottom=0.02, top=0.5)
    ax.grid()

    length = len(ordbok)
    len_p_sim = int((length-1)/2)
    ii = 0
    floor = 0
    for i in range(len_p_sim+1):
        ram = ordbok[ii]
        freq = ram[0]
        acc = ram[1]
        if floor == 0:
            plt.scatter(freq, acc, alpha=1, color='b', marker='*',s=100, label="No Outrigger")
        elif floor == ((len_p_sim+1) // 2 - 2):
            plt.scatter(0,0,color='r',alpha=1,label="Internal Outrigger")
            plt.scatter(freq, acc, alpha=1, color='r', label="floor: " + str(floor + 1))
        elif floor == ((len_p_sim+1) // 2 - 1):
            plt.scatter(freq, acc, alpha=1, color='r', label="floor: " + str(floor + 1))
        elif floor == ((len_p_sim+1) // 2):
            plt.scatter(freq, acc, alpha=1, color='r', label="floor: " + str(floor + 1))
        else:
            pass#plt.scatter(freq, acc, alpha=0.3, color='r', )
        ii+=1
        floor+=1

    floor = 0
    for i in range(len_p_sim):
        ram = ordbok[ii]
        freq = ram[0]
        acc = ram[1]
        if floor == ((len_p_sim) // 2 - 2):
            plt.scatter(0,0,color='m',alpha=1,label="External Outrigger")
            plt.scatter(freq, acc, alpha=1, color='m', label="floor: " + str(floor+2))
        elif floor == ((len_p_sim) // 2 - 1):
            plt.scatter(freq, acc, alpha=1, color='m', label="floor: " + str(floor+2))
        elif floor == ((len_p_sim) // 2):
            plt.scatter(freq, acc, alpha=1, color='m', label="floor: " + str(floor+2))
        else:
            pass#plt.scatter(freq, acc, alpha=0.3, color='m', )
        ii+=1
        floor+=1

    plt.legend(loc=1, title='Basisframe 10 floors')
    plt.savefig('performance_inner_outter.jpg', dpi=500)
    plt.show()



def feasabilityPlot_doubleOutrigger(ordbok,numFloor):
    fig, ax = plt.subplots(figsize=(8, 6), dpi=500)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xticks([0.06, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5])
    ax.set_yticks([0.02, 0.04, 0.06, 0.08, 0.1, 0.14, 0.2, 0.3, 0.5])
    ax.set_xlabel('Fundamental frequency in Hz', fontsize=14)
    ax.set_ylabel('Acceleration in m/s' + '$^2$', fontsize=14)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # Plot ISO criteria
    # The numbers
    ldiagx = [0.06, 1]
    ldiagy1 = [0.21, 0.06]
    ldiagy2 = [0.14, 0.04]
    horix = [1, 2]
    horiy1 = [0.06, 0.06]
    horiy2 = [0.04, 0.04]
    hdiagx = [2, 5]
    hdiagy1 = [0.06, 0.15]
    hdiagy2 = [0.04, 0.1]
    yline = [0, 0.5]
    minx = [0.06, 0.06]
    maxx = [5, 5]
    xline = [0.06, 5]
    miny = [0, 0]
    maxy = [0.5, 0.5]

    # Plot offices
    ax.plot(ldiagx, ldiagy1, 'k-', linewidth=1, label='Offices')
    ax.plot(horix, horiy1, 'k-', linewidth=1)
    ax.plot(hdiagx, hdiagy1, 'k-', linewidth=1)

    # Plot residential
    ax.plot(ldiagx, ldiagy2, 'k--', linewidth=1.8, label='Residential')
    ax.plot(horix, horiy2, 'k--', linewidth=1.8)
    ax.plot(hdiagx, hdiagy2, 'k--', linewidth=1.8)

    # Formatting the axis '%.2f'
    ax.set_xlim(left=0.06, right=5)
    ax.set_ylim(bottom=0.02, top=0.5)
    ax.grid()

    length = len(ordbok)
    for floor, i in enumerate(ordbok):
        freq = i[0]
        acc = i[1]
        if floor == 0:
            plt.scatter(freq, acc, alpha=1, marker='*',s=100, label= "no OR, "+str(numFloor)+" floors")
        else:
            plt.scatter(freq, acc, alpha=1, label="floor: " + str(i[2]) + " og " + str(i[3]))

    plt.legend(loc = 1)
    plt.show()


def feasabilityPlot_optimizing(ordbok, type):
    fig, ax = plt.subplots(figsize=(8, 6), dpi=500)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xticks([0.06, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5])
    ax.set_yticks([0.02, 0.04, 0.06, 0.08, 0.1, 0.14, 0.2, 0.3, 0.5])
    ax.set_xlabel('Fundamental frequency in Hz', fontsize=14)
    ax.set_ylabel('Acceleration in m/s' + '$^2$', fontsize=14)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # Plot ISO criteria
    # The numbers
    ldiagx = [0.06, 1]
    ldiagy1 = [0.21, 0.06]
    ldiagy2 = [0.14, 0.04]
    horix = [1, 2]
    horiy1 = [0.06, 0.06]
    horiy2 = [0.04, 0.04]
    hdiagx = [2, 5]
    hdiagy1 = [0.06, 0.15]
    hdiagy2 = [0.04, 0.1]
    yline = [0, 0.5]
    minx = [0.06, 0.06]
    maxx = [5, 5]
    xline = [0.06, 5]
    miny = [0, 0]
    maxy = [0.5, 0.5]

    # Plot offices
    ax.plot(ldiagx, ldiagy1, 'k-', linewidth=1, label='Offices')
    ax.plot(horix, horiy1, 'k-', linewidth=1)
    ax.plot(hdiagx, hdiagy1, 'k-', linewidth=1)

    # Plot residential
    ax.plot(ldiagx, ldiagy2, 'k--', linewidth=1.8, label='Residential')
    ax.plot(horix, horiy2, 'k--', linewidth=1.8)
    ax.plot(hdiagx, hdiagy2, 'k--', linewidth=1.8)

    # Formatting the axis '%.2f'
    ax.set_xlim(left=0.06, right=5)
    ax.set_ylim(bottom=0.02, top=0.5)
    ax.grid()

    for indeks, i in enumerate(ordbok):
        freq = i[0]
        acc = i[1]
        if indeks == 0:
            plt.scatter(freq, acc, color='b', alpha=1, marker='*',s=100, label= "IV-shaped " + str(round(ordbok[indeks][2], 2)))
        else:
            plt.scatter(freq, acc, color='r', alpha=0.3, label= type +" " + str(round(ordbok[indeks][2], 2)))


    plt.legend(loc = 1)
    plt.show()


from matplotlib.ticker import FormatStrFormatter


def ISOcrit1(fig=None, ax=None):
    # Create the Figure
    if (fig == None and ax == None):
        fig, ax = plt.subplots(figsize=(8, 6), dpi=500)
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_xticks([0.06, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5])
        ax.set_yticks([0.02, 0.04, 0.06, 0.08, 0.1, 0.14, 0.2, 0.3, 0.5])
        ax.set_xlabel('Fundamental frequency in Hz', fontsize=14)
        ax.set_ylabel('Acceleration in m/s' + '$^2$', fontsize=14)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        # Plot ISO criteria
        # The numbers
        ldiagx = [0.06, 1]
        ldiagy1 = [0.21, 0.06]
        ldiagy2 = [0.14, 0.04]
        horix = [1, 2]
        horiy1 = [0.06, 0.06]
        horiy2 = [0.04, 0.04]
        hdiagx = [2, 5]
        hdiagy1 = [0.06, 0.15]
        hdiagy2 = [0.04, 0.1]
        yline = [0, 0.5]
        minx = [0.06, 0.06]
        maxx = [5, 5]
        xline = [0.06, 5]
        miny = [0, 0]
        maxy = [0.5, 0.5]

        # Plot offices
        ax.plot(ldiagx, ldiagy1, 'k-', linewidth=1, label='Offices')
        ax.plot(horix, horiy1, 'k-', linewidth=1)
        ax.plot(hdiagx, hdiagy1, 'k-', linewidth=1)

        # Plot residential
        ax.plot(ldiagx, ldiagy2, 'k--', linewidth=1.8, label='Residential')
        ax.plot(horix, horiy2, 'k--', linewidth=1.8)
        ax.plot(hdiagx, hdiagy2, 'k--', linewidth=1.8)

        # Formatting the axis '%.2f'
        ax.set_xlim(left=0.06, right=5)
        ax.set_ylim(bottom=0.02, top=0.5)

    else:
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_xticks([0.06, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5])
        ax.set_yticks([0.02, 0.04, 0.06, 0.08, 0.1, 0.14, 0.2, 0.3, 0.5])
        ax.set_xlabel('Fundamental frequency in Hz', fontsize=14)
        ax.set_ylabel('Acceleration in m/s' + '$^2$', fontsize=14)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        # Plot ISO criteria
        # The numbers
        ldiagx = [0.06, 1]
        ldiagy1 = [0.21, 0.06]
        ldiagy2 = [0.14, 0.04]
        horix = [1, 2]
        horiy1 = [0.06, 0.06]
        horiy2 = [0.04, 0.04]
        hdiagx = [2, 5]
        hdiagy1 = [0.06, 0.15]
        hdiagy2 = [0.04, 0.1]
        yline = [0, 0.5]
        minx = [0.06, 0.06]
        maxx = [5, 5]
        xline = [0.06, 5]
        miny = [0, 0]
        maxy = [0.5, 0.5]

        # Plot offices
        ax.plot(ldiagx, ldiagy1, 'k-', linewidth=1, label='Offices')
        ax.plot(horix, horiy1, 'k-', linewidth=1)
        ax.plot(hdiagx, hdiagy1, 'k-', linewidth=1)

        # Plot residential
        ax.plot(ldiagx, ldiagy2, 'k--', linewidth=1.8, label='Residential')
        ax.plot(horix, horiy2, 'k--', linewidth=1.8)
        ax.plot(hdiagx, hdiagy2, 'k--', linewidth=1.8)

        # Formatting the axis '%.2f'
        ax.set_xlim(left=0.06, right=5)
        ax.set_ylim(bottom=0.02, top=0.5)

    # Add a grid
    ax.grid()
