# The agent (Robot) will be an object that's doing the movement.

# Robot's Input data:
#   - Proximity sensor: Distance from an identifier beacon.
#   - Self velocity
#   - Position and ID of the beacons in the environment

# For calculating the distance (proximity sensor), I'll have to use the robot's actual position.
# This position will not be used in the overall algorithm.

import numpy as np

from main import TIME_INTERVAL


class Agent:
    def __init__(self, initial_position, BeaconsList):
        self.position = list(initial_position)
        self.OdometerVel = 20
        self.BeaconsList = BeaconsList
        self.DistFromBeacons = []

    def move(self):
        # Update the agent's position based on the given deltas
        self.position[0] += (self.OdometerVel * TIME_INTERVAL)
        self.position[1] += (self.OdometerVel * TIME_INTERVAL)

    def acquire_sensors_data(self):
        # Simulate sensing the agent's position by adding noise
        # Moreover, sense all the other data (speed, distance from waypoints)

        true_position = self.position
        sensed_position = np.random.normal(loc=true_position, scale=[0.1, 0.1])  # Example noise

        for beacon in self.BeaconsList:
            # distance = agent.measure_distance(waypoint)
            # waypoint_distances.append(distance)
            pass

        return sensed_position
