import matplotlib.pyplot as plt
import mplcyberpunk  # The IDE shows this library as unused but it does used in line 4

TIME_INTERVAL = 1  # Global constant

plt.style.use("cyberpunk")
fig, ax = plt.subplots(figsize=(10, 10))


def simulation(env, agent, ParticleFilter, Iter):
    ax.clear()
    ax.set_xlim([0, env.width])
    ax.set_ylim([0, env.height])

    # Plot particles
    for particle in ParticleFilter.particles:
        plt.plot(particle.pos[0], particle.pos[1], marker='o', markersize=1, markeredgecolor="white",
                 markerfacecolor="red")

    # Plot the terminals
    plt.plot(env.StartTerminal[0], env.StartTerminal[1], marker="s", markersize=10, markeredgecolor="blue",
             markerfacecolor="green")
    plt.plot(env.EndTerminal[0], env.EndTerminal[1], marker="s", markersize=10, markeredgecolor="blue",
             markerfacecolor="green")

    # Plot Beacons
    for beacon in env.beacons:
        plt.plot(beacon.x, beacon.y, marker='o', markersize=15, markeredgecolor="black", markerfacecolor="red")

    # Plot path
    # for step in env.PathSteps:
    # plt.plot(step[0], step[1], marker='o', markersize=5, markeredgecolor="black", markerfacecolor="green")
    x_values = []
    y_values = []
    for step in env.PathSteps:
        x_values.append(step[0])
        y_values.append(step[1])
    plt.plot(x_values, y_values, 'black')

    # Plot Agent
    plt.plot(agent.position[0], agent.position[1], marker='*', markersize=10, markeredgecolor="red",
             markerfacecolor="yellow")

    # Plot the estimated position as a trajectory
    x_values = []
    y_values = []

    for i, step in enumerate(ParticleFilter.ParticlesMeanPosList):
        x_values.append(step[0])
        y_values.append(step[1])
    x_values[0] = env.StartTerminal[0]
    y_values[0] = env.StartTerminal[1]
    plt.plot(x_values, y_values, 'red')

    ax.minorticks_on()
    ax.grid(which='major', color='#000000', linestyle='--', alpha=0.5)
    ax.grid(which='minor', color='#000000', linestyle=':', alpha=0.4)
    # mplcyberpunk.add_glow_effects()  # This line makes some weird color effect... Unnecessary
    plt.draw()
    plt.pause(0.01)

    # Activate for saving the figures of the simulation
    # frame_path = f"frame_{Iter}.png"  # Provide a file path for each frame
    # fig.savefig(frame_path)
