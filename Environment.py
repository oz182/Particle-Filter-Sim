# This class defines the environment including:
# Terminals - Start point and End point of the path
# Beacons - Are waypoints which the agent is able to assist for positioning

class Env:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.beacons = []  # a list of objects
        self.StartTerminal = ()
        self.EndTerminal = ()

    def add_beacon(self, NewBeacon):
        # Add an obstacle to the environment
        self.beacons.append(NewBeacon)

    def generate_beacons(self, NumberOfBeacons):
        # The function will generate the beacons
        # In the assignment, I've been asked to generate the beacons in a uniform density over a rectangular region

        # Output: ----------------
        #
        pass

    def set_terminals(self, Ax, Ay, Bx, By):
        self.StartTerminal = (Ax, Ay)
        self.EndTerminal = (Bx, By)
        pass


class beacon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
