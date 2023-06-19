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

    plt.grid()
    plt.draw()
    plt.show()
    plt.pause(0.01)
