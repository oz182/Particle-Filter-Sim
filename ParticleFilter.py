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
        self.ResampledParticles = []
        self.Particles_SumOfWeights = 1.0
        self.map_size = map_size
        self.ParticlesWeightsList = []

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
            particle.ParticleLikelihood = 1.0  # Initialize particle's likelihood

            for data in BeaconsDistances:
                if data[1] is not None:
                    # 'data' is a list inside the 'BeaconsDistances' list.
                    # This list structure (data) is: [ [id,dist,pos], [], ... ]
                    # dist of particle to beacon:
                    Dist_par_beac = np.linalg.norm(abs(np.array(particle.pos) - np.array(data[2])))

                    # Likelihood calculation, based on P(z|x), z - dist of beacon to robot,
                    # x - dist of particle to beacon
                    particle.ParticleLikelihood *= stats.norm(Dist_par_beac, 50).pdf(data[1])
                    # TODO This value of 50 should be the var. TBD

            # The next line: p(x|z) where z is the measurement and x is the state
            particle.weight *= particle.ParticleLikelihood

            # Normalize the weight
            particle.weight = particle.weight / self.Particle_SumOfWeights

            self.ParticlesWeightsList.append(particle.weight)
            particle.weight += 1.e-300

        self.Particles_SumOfWeights = sum(self.ParticlesWeightsList)

    def systematic_resampling(self):

        N = self.num_particles

        CDF_weights = np.cumsum(self.ParticlesWeightsList)  # Cumulative Sum of weights
        u1 = np.random.uniform(1e-10, 1.0 / N, 1)[0]

        for j in range(1, N):
            u_j = u1 + float(j - 1) / N
            i = 0

            while u_j > CDF_weights[i] and i < 398:
                i += 1

            self.particles[i].weight = (1.0 / N)
            self.ResampledParticles.append(self.particles[i])

        self.particles = self.ResampledParticles
        self.ResampledParticles = []

    def estimate_state(self):
        # Compute the estimated state based on the weighted average of particles
        # For now it is used only in the 'simple_resample' function
        ParticlesPosList = []
        for par in self.particles:
            ParticlesPosList.append(par.pos)

        mean = np.average(ParticlesPosList, weights=self.ParticlesWeightsList, axis=0)
        var = np.var(ParticlesPosList, axis=0)
        return mean, var


def run_filter_iteration(ParticleFilterObj, vel_x, vel_y, BeaconsDistances):
    # This function starts one filter iteration

    ParticleFilterObj.predict(vel_x, vel_y)
    ParticleFilterObj.update_weights(BeaconsDistances)

    ParticleFilterObj.systematic_resampling()


class Particle:
    def __init__(self, NumOfParticles):
        self.pos = []
        self.weight = 1 / NumOfParticles
        self.ParticleLikelihood = 1.0
