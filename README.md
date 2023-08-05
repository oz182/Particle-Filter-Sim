# Particle-Filter-Sim
Python simulation for particle filter algorithm.

This project is sparated into modules, where each module has its own related object.

<img width="699" alt="Screenshot 2023-08-05 at 19 46 49" src="https://github.com/oz182/Particle-Filter-Sim/assets/91877982/2d9902f4-7929-46a7-863b-36c9cc574e07">

## Perception and information fusion algorithm
The implemented perception algorithm in this project is a particle filter. Particle filters are probabilistic algorithms used in robotics for localization, estimating a robot's position in an unknown environment. It represents the robot's belief with particles, each denoting a potential state. The algorithm has two main steps: prediction (motion model) and update (sensor measurements). Particles are propagated with noise in prediction, and in the update, they are weighted based on how well they match sensor data. Efficient resampling refines the estimate. Particle filters excel in handling uncertainties and non-linearities.


<img width="793" alt="Screenshot 2023-08-05 at 19 49 15" src="https://github.com/oz182/Particle-Filter-Sim/assets/91877982/e418a9cb-4696-4a30-8585-2e7077e00ee8">

## Particle filter algorithm’s presentation
These specific algorithms below (all related to the particle filter), are located in my module ParticleFilter.py which can be found in my GitHub project

<img width="351" alt="image" src="https://github.com/oz182/Particle-Filter-Sim/assets/91877982/30186344-1e96-4934-9891-5cf9481a0feb">

<img width="347" alt="image" src="https://github.com/oz182/Particle-Filter-Sim/assets/91877982/1a838900-a61e-4919-9939-83a4abb0679a">

<img width="350" alt="image" src="https://github.com/oz182/Particle-Filter-Sim/assets/91877982/bb0fe1bb-9cab-4a62-8767-b4cab7a5dc64">

# Results

![ezgif com-gif-maker](https://github.com/oz182/Particle-Filter-Sim/assets/91877982/48f66c1a-ce87-4b3e-95b0-a452fd924984)

![FilterGif](https://github.com/oz182/Particle-Filter-Sim/assets/91877982/e2053bee-3ff7-4ef3-8f93-fe128da32f98)

