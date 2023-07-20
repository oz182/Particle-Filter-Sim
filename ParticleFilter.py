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
        self.ParticlesPosList = []

        self.PartiPos = []

    def initialize_particles(self):
        # Initialize the particles randomly within the map boundaries
        for _ in range(self.num_particles):
            particle = Particle(self.num_particles)
            particle.pos = np.random.uniform(low=[0, 0], high=self.map_size)  # Uniform distribution around the map size
            # particle.pos = np.random.uniform(low=[0, 0], high=[10, 10])
            self.particles.append(particle)

    def predict(self, vel_x, vel_y):
        # Update the particles based on the agent's movement
        for par in self.particles:
            par.pos[0] += vel_x * TIME_INTERVAL
            par.pos[1] += vel_y * TIME_INTERVAL

    def update_weights(self, BeaconsDistances):
        # Update the weights based on the observed data.
        self.ParticlesPosList = []
        self.ParticlesWeightsList = []
        self.Particles_SumOfWeights = 1.0

        IsNearBeacon = False

        for particle in self.particles:
            particle.ParticleLikelihood = 1.0  # Initialize particle's likelihood

            for data in BeaconsDistances:
                if data[1] is not None:
                    # 'data' is a list inside the 'BeaconsDistances' list.
                    # This list structure (data) is: [ [id,dist,pos], [], ... ] (dist - robot to beacon)
                    # dist of particle to beacon:

                    # Dist_par_beac = np.linalg.norm(abs(np.array(particle.pos) - np.array(data[2])))
                    Dist_par_beac = np.power((particle.pos[0] - data[2][0]) ** 2 +
                                             (particle.pos[1] - data[2][1]) ** 2, 0.5)

                    # Likelihood calculation, based on p(z|x), z - dist of beacon to robot,
                    # x - dist of particle to beacon
                    particle.ParticleLikelihood *= stats.norm(Dist_par_beac, 10).pdf(data[1])
                    # particle.ParticleLikelihood *= stats.norm(data[1], 0.4).pdf(Dist_par_beac)

                    IsNearBeacon = True

            if not IsNearBeacon:
                particle.ParticleLikelihood = 0.0

            # The next line: p(x|z) where z is the measurement and x is the state
            particle.weight *= particle.ParticleLikelihood
            particle.weight += 1e-300  # Avoid round-off to zero

            self.ParticlesWeightsList.append(particle.weight)
            self.ParticlesPosList.append(particle.pos)

        self.Particles_SumOfWeights = sum(self.ParticlesWeightsList)

        # Normalize the weights
        self.ParticlesWeightsList = np.array(self.ParticlesWeightsList) / self.Particles_SumOfWeights

    def systematic_resampling(self):

        N = self.num_particles

        CDF_weights = np.cumsum(self.ParticlesWeightsList)  # Cumulative Sum of weights
        u1 = np.random.uniform(0, 1.0 / N, 1)[0]

        i = 0

        for j in range(0, N):
            u_j = u1 + (float(j) / N)

            while u_j > CDF_weights[i]:
                i += 1

            # self.ResampledParticles.append(self.ParticlesPosList[i])
            self.particles[j].pos = self.ParticlesPosList[i]
            self.particles[j].weight = 1.0 / N

    #  ------- Other good tries ------------------
    # self.particles[j].weight = self.ParticlesWeightsList[i]

    # for par in self.ResampledParticles:
    # par.weight = 1.0 / N

    # self.particles = self.ResampledParticles
    # self.ResampledParticles = []

    def calc_n_eff(self):
        return 1. / np.sum(np.square(self.ParticlesWeightsList))

    def estimate_state(self):
        # Compute the estimated state based on the weighted average of particles
        # For now it is used only in the 'simple_resample' function
        ParticlesPosList = []
        for par in self.particles:
            ParticlesPosList.append(par.pos)

        mean = np.average(ParticlesPosList, weights=self.ParticlesWeightsList, axis=0)
        var = np.var(ParticlesPosList, axis=0)
        return mean, var

    def test_func(self):
        for par in self.particles:
            print(par.pos)


def run_filter_iteration(ParticleFilterObj, vel_x, vel_y, BeaconsDistances):
    # This function starts one filter iteration

    ParticleFilterObj.predict(vel_x, vel_y)
    ParticleFilterObj.update_weights(BeaconsDistances)

    if ParticleFilterObj.calc_n_eff() <= (ParticleFilterObj.num_particles * 0.5):
        ParticleFilterObj.systematic_resampling()

    # ParticleFilterObj.test_func()


class Particle:
    def __init__(self, NumOfParticles):
        self.pos = []
        self.weight = 1.0 / NumOfParticles
        self.ParticleLikelihood = 1.0
