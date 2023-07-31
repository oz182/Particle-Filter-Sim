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

        self.ParticlesMeanPos = 0
        self.ParticlesMeanPosList = []
        self.ParticlesVarPos = 0
        self.IsResampled = False

        self.SquaredError = 0
        self.SquaredErrorList = []
        self.MeanSqErr = 0  # Refers to Mean square error

    def initialize_particles(self):
        # Initialize the particles randomly within the map boundaries
        for _ in range(self.num_particles):
            particle = Particle(self.num_particles)
            # Uniform distribution around the map size
            particle.pos = np.random.uniform(low=[0, 0],
                                             high=[self.map_size[0], self.map_size[1]])
            # particle.pos = np.random.uniform(low=[0, 0], high=[10, 10])
            self.particles.append(particle)

    def predict(self, vel_x, vel_y):
        # Update the particles based on the agent's movement
        for i, par in enumerate(self.particles):
            par.pos[0] += (vel_x + np.random.normal(0, 1)) * TIME_INTERVAL
            par.pos[1] += (vel_y + np.random.normal(0, 1)) * TIME_INTERVAL

        # Weird bug: This for loop iterates on a list of object.
        # Turns out that when the position value of some objects is the same,
        # the for loop updates them both at the same time.

    def update_weights(self, BeaconsDistances):
        # Update the weights based on the observed data.
        self.ParticlesPosList = []
        self.ParticlesWeightsList = []
        self.Particles_SumOfWeights = 1.0

        for particle in self.particles:
            # particle.weight = 1.0
            particle.ParticleLikelihood = 1.0  # Initialize particle's likelihood

            for data in BeaconsDistances:
                if data[1] is not None:
                    # 'data' is a list inside the 'BeaconsDistances' list.
                    # This list structure (data) is: [ [id,dist,pos], [], ... ] (dist = robot to beacon)
                    # dist of particle to beacon:

                    # Dist_par_beac = np.linalg.norm(abs(np.array(particle.pos) - np.array(data[2])))
                    Dist_par_beac = np.power((particle.pos[0] - data[2][0]) ** 2 +
                                             (particle.pos[1] - data[2][1]) ** 2, 0.5)

                    # Likelihood calculation, based on p(z|x), z - dist of beacon to robot,
                    # x - dist of particle to beacon
                    particle.ParticleLikelihood *= stats.norm(Dist_par_beac, 0.4).pdf(data[1])

            # The weight calculation
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

        for j in range(0, N - 1):
            u_j = u1 + float(j) / N

            while u_j > CDF_weights[i]:
                i += 1

            # self.ResampledParticles.append(self.ParticlesPosList[i])
            self.particles[j].pos = self.ParticlesPosList[i] + (i * 1e-300)  # This addition is only to over come the
            # object for loop bug in the prediction function (Explanation in the function).
            self.particles[j].weight = 1.0 / N  # In the literature, the weights are redefined to 1/N

        self.IsResampled = True

    def calc_n_eff(self):
        return 1. / np.sum(np.square(np.array(self.ParticlesWeightsList)))

    def estimate_state(self, RobotPos):
        # Compute the estimated state based on the weighted average of particles

        self.ParticlesMeanPos = np.mean((np.array(self.ParticlesPosList)), axis=0)
        self.ParticlesMeanPosList.append(self.ParticlesMeanPos)

        self.ParticlesVarPos = np.var((np.array(self.ParticlesPosList)), axis=0)  # Not sure if this value is needed

        self.SquaredError = np.linalg.norm(self.ParticlesMeanPos - np.array(RobotPos)) ** 2
        self.SquaredErrorList.append(self.SquaredError)

        self.MeanSqErr = np.array(self.SquaredErrorList).mean()


def run_filter_iteration(ParticleFilterObj, vel_x, vel_y, BeaconsDistances, RobotPos):
    # This function starts one filter iteration

    ParticleFilterObj.predict(vel_x, vel_y)  # Can be called from main
    ParticleFilterObj.update_weights(BeaconsDistances)

    """ The part of the N_eff test, turns out to be not so relevant in my case
    if ParticleFilterObj.calc_n_eff() >= (ParticleFilterObj.num_particles * 0.5):
        ParticleFilterObj.systematic_resampling()
    """
    ParticleFilterObj.systematic_resampling()

    # Measure the mean position of the particles, and the variation
    ParticleFilterObj.estimate_state(RobotPos)


class Particle:
    def __init__(self, NumOfParticles):
        self.pos = []
        self.weight = 1.0 / NumOfParticles
        self.ParticleLikelihood = 1.0
