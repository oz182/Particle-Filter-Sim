# This class defines the environment including:
# Terminals - Start point and End point of the path
# Beacons - Are waypoints which the agent is able to assist for positioning

import random
import networkx as nx


class Env:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.beacons = []  # a list of objects
        self.StartTerminal = []
        self.EndTerminal = []

        self.PathSteps = []

    def add_custom_beacon(self, NewBeacon):
        # Add a beacon and manually choose it's position in the environment
        self.beacons.append(NewBeacon)

    def generate_beacons(self, NumberOfBeacons):
        # The function will generate the beacons
        # In the assignment, I've been asked to generate the beacons in a uniform density over a rectangular region

        for i in range(NumberOfBeacons):
            x_pos = random.uniform(0, self.width - 5)
            y_pos = random.uniform(0, self.height - 5)

            beacon_obj = beacon(i, x_pos, y_pos)  # 'i' serves as the id of the beacon
            self.beacons.append(beacon_obj)

    def generate_random_path(self, NumberOfSteps):
        # The function will generate the waypoints that will eventually build the path. In this function
        # the path is constructed randomly.

        TempSteps = []

        for i in range(NumberOfSteps):
            x_pos = random.uniform(5, self.width - 5)
            y_pos = random.uniform(5, self.height - 5)

            Step = [x_pos, y_pos]
            TempSteps.append(Step)

        G = nx.Graph()

        # Add start and goal nodes
        G.add_node("start", pos=self.StartTerminal)
        G.add_node("goal", pos=self.EndTerminal)

        # Add obstacle nodes
        for i, step in enumerate(TempSteps):
            G.add_node(f"waypoint{i}", pos=step)

        # Connect nodes within a certain distance
        for u, u_attr in G.nodes(data=True):
            for v, v_attr in G.nodes(data=True):
                if u != v:
                    u_pos = u_attr["pos"]
                    v_pos = v_attr["pos"]
                    distance = ((u_pos[0] - v_pos[0]) ** 2 + (u_pos[1] - v_pos[1]) ** 2) ** 0.5
                    if distance <= 10.0:  # Adjust the distance threshold as needed
                        G.add_edge(u, v)

        # Find the shortest path
        Shortest_path = nx.shortest_path(G, "start", "goal")

        for node in Shortest_path:
            self.PathSteps.append(G.nodes[node]["pos"])

    def set_terminals(self, Ax, Ay, Bx, By):
        self.StartTerminal = (Ax, Ay)
        self.EndTerminal = (Bx, By)
        pass


class beacon:
    def __init__(self, id_number, x, y):
        self.id = id_number
        self.x = x
        self.y = y


class path:
    def __init__(self, StartPos, GoalPos, ObstacleList):
        self.StartPos = StartPos
        self.GoalPos = GoalPos
        self.ObstacleList = ObstacleList


#  The Comment section below is an example of using the NetworkX library


"""
    def generate_path(self):
        G = nx.Graph()

        # Add start and goal nodes
        G.add_node("start", pos=self.StartPos)
        G.add_node("goal", pos=self.GoalPos)

        # Add obstacle nodes
        for i, obstacle in enumerate(self.ObstacleList):
            G.add_node(f"obstacle{i}", pos=obstacle)

        # Connect nodes within a certain distance
        for u, u_attr in G.nodes(data=True):
            for v, v_attr in G.nodes(data=True):
                if u != v:
                    u_pos = u_attr["pos"]
                    v_pos = v_attr["pos"]
                    distance = ((u_pos[0] - v_pos[0]) ** 2 + (u_pos[1] - v_pos[1]) ** 2) ** 0.5
                    if distance <= 1.0:  # Adjust the distance threshold as needed
                        G.add_edge(u, v)

        # Find the shortest path
        path = nx.shortest_path(G, "start", "goal")

        # Extract path positions
        path_positions = [G.nodes[node]["pos"] for node in path]

        # Plotting
        pos = nx.get_node_attributes(G, "pos")
        plt.figure(figsize=(8, 8))
        nx.draw(G, pos, with_labels=True, node_color="lightgray", node_size=500, font_size=10)
        nx.draw_networkx_nodes(G, pos, nodelist=["start", "goal"], node_color="green", node_size=500)
        nx.draw_networkx_nodes(G, pos, nodelist=path[1:-1], node_color="blue", node_size=500)
        nx.draw_networkx_edges(G, pos)
        plt.plot([start[0]], [start[1]], marker="o", markersize=10, color="green")
        plt.plot([goal[0]], [goal[1]], marker="o", markersize=10, color="green")
        plt.plot([x for x, _ in path_positions], [y for _, y in path_positions], marker="o", markersize=10,
                 color="blue")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Path Planning")
        plt.grid(True)
        plt.show()

        pass

    pass
"""
