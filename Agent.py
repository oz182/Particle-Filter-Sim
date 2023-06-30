# The agent (Robot) will be an object that's doing the movement.

# Robot's Input data:
#   - Proximity sensor: Distance from an identifier beacon.
#   - Self velocity
#   - Position and ID of the beacons in the environment

# For calculating the distance (proximity sensor), I'll have to use the robot's actual position.
# This position will not be used in the overall algorithm.

import numpy as np


class Agent:
    def __init__(self, initial_position, BeaconsList):
        self.position = initial_position
        self.BeaconsList = BeaconsList

    def move(self, delta_x, delta_y):
        # Update the agent's position based on the given deltas
        self.position[0] += delta_x
        self.position[1] += delta_y

    def sense(self):
        # Simulate sensing the agent's position by adding noise
        true_position = self.position
        sensed_position = np.random.normal(loc=true_position, scale=[0.1, 0.1])  # Example noise

        return sensed_position
