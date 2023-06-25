import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8))


def simulation(env):
    ax.clear()
    ax.set_xlim([0, env.width])
    ax.set_ylim([0, env.height])

    plt.plot(env.StartTerminal[0], env.StartTerminal[1], marker="s", markersize=10, markeredgecolor="blue",
             markerfacecolor="green")
    plt.plot(env.EndTerminal[0], env.EndTerminal[1], marker="s", markersize=10, markeredgecolor="blue",
             markerfacecolor="green")

    for beacon in env.beacons:
        plt.plot(beacon.x, beacon.y, marker='o', markersize=15, markeredgecolor="black", markerfacecolor="red")

    for step in env.PathSteps:
        plt.plot(step[0], step[1], marker='o', markersize=5, markeredgecolor="black", markerfacecolor="green")

    x_values = []
    y_values = []
    for step in env.PathSteps:
        x_values.append(step[0])
        y_values.append(step[1])
    plt.plot(x_values, y_values, 'black')

    ax.minorticks_on()
    ax.grid(which='major', color='#CCCCCC', linestyle='--', alpha=1)
    ax.grid(which='minor', color='#CCCCCC', linestyle=':', alpha=0.7)
    plt.style.use('dark_background')
    plt.draw()
    plt.show()
    plt.pause(0.01)
