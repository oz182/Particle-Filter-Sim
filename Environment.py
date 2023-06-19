# This class defines the environment including:
# Terminals - Start point and End point of the path
# Beacons - Are waypoints which the agent is able to assist for positioning

import random


class Env:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.beacons = []  # a list of objects
        self.StartTerminal = ()
        self.EndTerminal = ()

    def add_custom_beacon(self, NewBeacon):
        # Add a beacon and manually choose it's position in the environment
        self.beacons.append(NewBeacon)

    def generate_beacons(self, NumberOfBeacons):
        # The function will generate the beacons
        # In the assignment, I've been asked to generate the beacons in a uniform density over a rectangular region

        for i in range(NumberOfBeacons):
            x_pos = random.uniform(0, self.width)
            y_pos = random.uniform(0, self.height)

            beacon_obj = beacon(i, x_pos, y_pos)  # 'i' serves as the id of the beacon
            self.beacons.append(beacon_obj)

            print(beacon_obj.x, beacon_obj.y)

    def set_terminals(self, Ax, Ay, Bx, By):
        self.StartTerminal = (Ax, Ay)
        self.EndTerminal = (Bx, By)
        pass


class beacon:
    def __init__(self, id_number, x, y):
        self.id = id_number
        self.x = x
        self.y = y
