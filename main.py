# Particle Filter algorithm simulation

from Environment import *
from Agent import *
from ParticleFilter import *
from Simulation import *


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
    # envFrame.set_pre_defined_beacons()

    envFrame.generate_uniform_random_path(2000)  # Input number of waypoints for the path
    # envFrame.set_pre_defined_path()

    robot = Agent(envFrame.StartTerminal, envFrame.beacons, envFrame.PathSteps)  # Initialize the agent instance

    # Create the particle filter instance and initialize the particles
    PF = ParticleFilter(400, [envFrame.width, envFrame.height])
    PF.initialize_particles()

    # The main algorithm loop
    # In this loop the agent is moving along the path, and its position is estimated using the
    # particle filter algorithm.
    while not arrived_to_goal(robot, envFrame):
        # Estimate position using particle filter - function "run_pf_iteration"
        # Gets the filter object, and sensors measurements - Odometer data, and distance from all the beacons.
        run_filter_iteration(PF, robot.OdometerVel_x, robot.OdometerVel_y, robot.BeaconsDistances)

        robot.move()  # move the robot along the path

        robot.proximity_reading()
        robot.odometer_reading()

        simulation(envFrame, robot, PF)

        input("Press any key to continue>>>")  # Uncomment to control iterations

    print("The agent has reached the target!!")
    plt.show()  # Make the graph stay on the screen after the simulation has ended


if __name__ == "__main__":
    main()
