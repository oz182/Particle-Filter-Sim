# The agent (Robot) will be an object that's doing the movement.

# Robot's Input data:
#   - Proximity sensor: Distance from an identifier beacon.
#   - Self velocity
#   - Position and ID of the beacons in the environment

# For calculating the distance (proximity sensor), I'll have to use the robot's actual position.
# This position will not be used in the overall algorithm.

import numpy as np

from Simulation import TIME_INTERVAL


class Agent:
    def __init__(self, initial_position, BeaconsList, PathSteps):
        self.position = list(initial_position)
        self.OdometerVel_x = 0
        self.OdometerVel_y = 0
        self.BeaconsList = BeaconsList
        self.BeaconsDistances = []
        self.PathSteps = PathSteps  # A list contains the step's coordinates on the path
        self.PositionInPath = 0

    def move(self):
        self.position[0] = self.PathSteps[self.PositionInPath][0]
        self.position[1] = self.PathSteps[self.PositionInPath][1]

        self.PositionInPath += 1

    def proximity_reading(self):
        # Simulate the proximity sensor data, with noise Reading.
        # can be acquire only if the beacon is in the proximity sensor's range (define to be 2 in the assignment)
        ProxSensorRange = 2
        Prox_noise_mean = 0
        Prox_noise_var = 0.4
        ProxSensorNoise = np.random.normal(Prox_noise_mean, np.sqrt(Prox_noise_var))

        for beacon in self.BeaconsList:
            # The distance between a beacon and the robot is calculated as the normal vector between two points.
            # The command 'norm' can get only numpy array, that why the casting
            DistFromBeacon = np.linalg.norm(abs(np.array(beacon.pos) - np.array(self.position)))
            if DistFromBeacon <= ProxSensorRange:
                self.BeaconsDistances.append([beacon.id, (DistFromBeacon + ProxSensorNoise)])
            else:
                self.BeaconsDistances.append([beacon.id, None])

        # The function updates the self values of the agent's object.
        # It creates a list of beacons id and distance in the following form: ([id, dist], [is, dist], ..)

    def odometer_reading(self):
        #  Get the velocity by the equation: (Current_pos - Prev_pos) / dt
        #  Integral on the delta position
        vel_x = (self.PathSteps[self.PositionInPath][0] - self.PathSteps[self.PositionInPath - 1][0]) / TIME_INTERVAL
        vel_y = (self.PathSteps[self.PositionInPath][1] - self.PathSteps[self.PositionInPath - 1][1]) / TIME_INTERVAL

        #  The odometer reading with the given noise added: a zero-mean Gaussian with variance 0.1.
        Odometer_noise_mean = 0
        Odometer_noise_var = 0.1
        self.OdometerVel_x = vel_x + np.random.normal(Odometer_noise_mean, np.sqrt(Odometer_noise_var))
        self.OdometerVel_y = vel_y + np.random.normal(Odometer_noise_mean, np.sqrt(Odometer_noise_var))


