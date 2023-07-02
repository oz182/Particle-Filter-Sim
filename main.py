# Particle Filter algorithm simulation

from Environment import *
from Agent import *
from ParticleFilter import *
from Simulation import *

TIME_INTERVAL = 0.01


def arrived_to_goal(robot, env):
    DistToGoal_X = abs(robot.position[0] - env.EndTerminal[0])
    DistToGoal_Y = abs(robot.position[1] - env.EndTerminal[1])

    if (DistToGoal_X <= 2) and (DistToGoal_Y <= 2):  # 2 is a tolerance distance for counting as reaching to goal
        # If arrived to goal
        return 1
    else:
        return 0


def main():
    # Create a new environment, add obstacles and goal.
    envFrame = Env(40, 30)
    envFrame.set_terminals(3, 3, 38, 28)  # Ax, Ay, Bx,
    envFrame.generate_uniform_random_beacons(10)  # from the assignment: 10 beacons

    envFrame.generate_uniform_random_path(2000)  # Input number of waypoints for the path

    robot = Agent(envFrame.StartTerminal, envFrame.beacons, envFrame.PathSteps)  # Initialize the agent instance

    # Create the particle filter instance and initialize the particles
    PF = ParticleFilter(400, [envFrame.width, envFrame.height])
    PF.initialize_particles()

    # The main algorithm loop
    while not arrived_to_goal(robot, envFrame):

        robot.acquire_sensors_data()

        # Estimate position using particle filter - function "run_pf_iteration"

        robot.move()

        simulation(envFrame, robot, PF)

    print("The agent has reached the target!!")
    plt.show()  # Make the graph stay on the screen after the simulation has ended


if __name__ == "__main__":
    main()
