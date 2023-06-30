# Particle Filter algorithm simulation

from Environment import *
from Agent import *
from ParticleFilter import *
from Simulation import *


def main():
    # Create a new environment, add obstacles and goal.
    envFrame = Env(40, 30)
    envFrame.set_terminals(3, 3, 38, 28)  # Ax, Ay, Bx,
    envFrame.generate_beacons(10)  # from the assignment: 10 beacons

    envFrame.generate_random_path(100)  # Input number of waypoints for the path

    robot = Agent(envFrame.StartTerminal, envFrame.beacons)

    PF = ParticleFilter(400, [envFrame.width, envFrame.height])
    PF.initialize_particles()

    simulation(envFrame, robot, PF)


if __name__ == "__main__":
    main()
