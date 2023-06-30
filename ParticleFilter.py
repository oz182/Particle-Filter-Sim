# A particle will be defined as an object.
# The attributes and function will be described below

import numpy as np
from numpy.random import uniform


class ParticleFilter:
    def __init__(self, num_particles, map_size):
        self.num_particles = num_particles
        self.particles = []
        self.weights = np.ones(num_particles) / num_particles
        self.map_size = map_size

    def initialize_particles(self):
        # Initialize the particles randomly within the map boundaries
        for _ in range(self.num_particles):
            particle = np.random.uniform(low=[0, 0], high=self.map_size)
            self.particles.append(particle)

    def predict(self, delta_x, delta_y):
        # Update the particles based on the agent's movement
        for i in range(self.num_particles):
            self.particles[i][0] += delta_x
            self.particles[i][1] += delta_y

    def update_weights(self, sensed_position):
        # Update the weights based on the observed data
        for i in range(self.num_particles):
            particle = self.particles[i]
            self.weights[i] = self.calculate_likelihood(particle, sensed_position)

        # Normalize the weights
        self.weights /= np.sum(self.weights)

    def calculate_likelihood(self, particle, sensed_position):
        # Calculate the likelihood of the particle given the sensed position
        # You can use a distance-based likelihood calculation, for example
        # Return the likelihood value
        pass

    def resample(self):
        # Resample the particles based on their weights
        indices = np.random.choice(range(self.num_particles), size=self.num_particles, p=self.weights)
        self.particles = [self.particles[i] for i in indices]
        self.weights = np.ones(self.num_particles) / self.num_particles

    def estimate_state(self):
        # Compute the estimated state based on the weighted average of particles
        estimated_state = np.average(self.particles, weights=self.weights, axis=0)
        return estimated_state
