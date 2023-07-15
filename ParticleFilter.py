# A particle will be defined as an object.
# The attributes and function will be described below

import numpy as np
from numpy.random import uniform
from scipy import stats

from Simulation import TIME_INTERVAL


class ParticleFilter:
    def __init__(self, num_particles, map_size):
        self.num_particles = num_particles
        self.particles = []
        self.Particle_SumOfWeights = 1.0
        self.map_size = map_size
        self.ParticlesWeightsList = []
        self.ParticleLikelihood = 1.0

    def initialize_particles(self):
        # Initialize the particles randomly within the map boundaries
        for _ in range(self.num_particles):
            particle = Particle(self.num_particles)
            particle.pos = np.random.uniform(low=[0, 0], high=self.map_size)  # Uniform distribution around the map size
            self.particles.append(particle)

    def predict(self, vel_x, vel_y):
        # Update the particles based on the agent's movement
        for par in self.particles:
            par.pos[0] += vel_x * TIME_INTERVAL
            par.pos[1] += vel_y * TIME_INTERVAL

    def update_weights(self, BeaconsDistances):
        # Update the weights based on the observed data.
        self.ParticlesWeightsList = []
        self.Particle_SumOfWeights = 1.0

        for particle in self.particles:
            self.ParticleLikelihood = 1.0  # Initialize particle's likelihood

            for data in BeaconsDistances:
                if data[1] is not None:

                    # 'data' is a list inside the 'BeaconsDistances' list.
                    # This list structure (data) is: [ [id,dist,pos], [], ... ]
                    # dist of particle to beacon:
                    Dist_par_beac = np.linalg.norm(np.array(particle.pos) - np.array(data[2]))

                    # Likelihood calculation, based on P(z|x), z - dist of beacon to robot,
                    # x - dist of particle to beacon
                    self.ParticleLikelihood *= stats.norm(Dist_par_beac, 50)
                    # TODO This value of 50 should be the std. TBD

            # The next line: p(x|z) where z is the measurement and x is the state
            particle.weight *= self.ParticleLikelihood

            self.Particle_SumOfWeights += particle.weight
            self.ParticlesWeightsList.append(particle.weight)

            # Normalize the weight
            particle.weight = particle.weight / len(self.ParticlesWeightsList)

    def resample(self, NumOfParticles):
        # Resample the particles based on their weights
        for particle in self.particles:
            particle.pos = np.random.choice(NumOfParticles,
                                            p=self.ParticlesWeightsList)  # Uniform distribution around the map size
            particle.weight = 1 / NumOfParticles

        """
        indices = np.random.choice(range(self.num_particles), size=self.num_particles, p=self.weights)
        self.particles = [self.particles[i] for i in indices]
        self.weights = np.ones(self.num_particles) / self.num_particles
        """

    def estimate_state(self):
        # Compute the estimated state based on the weighted average of particles - importance sampling
        estimated_state = np.average(self.particles, weights=self.weights, axis=0)
        return estimated_state


def run_filter_iteration(ParticleFilterObj, vel_x, vel_y, BeaconsDistances):
    # This function starts one filter iteration

    ParticleFilterObj.predict(vel_x, vel_y)
    ParticleFilterObj.update_weights(BeaconsDistances)
    # ParticleFilterObj.resample(ParticleFilterObj.num_particles)
    # ParticleFilterObj.estimate_state()


class Particle:
    def __init__(self, NumOfParticles):
        self.pos = []
        self.weight = 1 / NumOfParticles
