# Particle Filter algorithm simulation

from Environment import *
from Simulation import *


def main():
    # Create a new environment, add obstacles and goal.
    envFrame = Env(40, 30)
    envFrame.set_terminals(3, 3, 38, 28)  # Ax, Ay, Bx,
    envFrame.generate_beacons(10)  # from the assignment: 10 beacons

    simulation(envFrame)


if __name__ == "__main__":
    main()
