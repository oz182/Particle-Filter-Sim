# The agent (Robot) will be an object that's doing the movement.

# Robot's Input data:
#   - Proximity sensor: Distance from an identifier beacon.
#   - Self velocity
#   - Position and ID of the beacons in the environment

# For calculating the distance (proximity sensor), I'll have to use the robot's actual position.
# This position will not be used in the overall algorithm.


class Agent:
    def __init__(self, BeaconsList):
        self.BeaconsList = BeaconsList

        pass
