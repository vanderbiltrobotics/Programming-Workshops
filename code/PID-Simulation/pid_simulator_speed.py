
# Required packages
from matplotlib import pyplot as plt
from math import *
import random

# Length of simulation
timesteps = 10000   # in milliseconds
time_array = [i / 1000.0 for i in range(timesteps)]

# --- DEFINE SOME TARGET VALUE ARRAYS --- #

# Constant target value
target_const = [10.0 for i in range(timesteps)]

# Value changes once halfway through
target_step = [10.0 for i in range(timesteps / 2)] + [5.0 for i in range(timesteps / 2)]

# Value follows a low frequency sine wave
target_sine_lf = [5 + 5.0 * sin((i / 1000.0) * (2 * pi / 5)) for i in range(timesteps)]

# Value follows a higher frequency sine wave
target_sine_hf = [5 + 5.0 * sin((i / 1000.0) * (2 * pi / 1)) for i in range(timesteps)]

# Value wanders randomly
target_wandering = []
wand_val = 0.0
for i in range(timesteps):
    wand_val = wand_val + random.normalvariate(0, 0.1)
    if wand_val > 10.0:
        wand_val = 10.0
    if wand_val < -10.0:
        wand_val = -10.0
    target_wandering.append(wand_val)


# --- FUNCTION TO RUN THE SIMULATION --- #


def run_simulation(target_array, time_array, p_gain, i_gain, d_gain):

    # Current position - we want this to equal the target position
    position = 0

    # Keep track of data for graphing
    position_hist = []
    error_hist = []

    # PID variables
    integrator_sum = 0
    prev_error = 0

    # Run simulation
    for step in range(len(time_array)):

        # Calculate error for this time step
        error = target_array[step] - position            # error in meters

        # Update PID variables
        integrator_sum += error                       # cumulative error in meters
        error_slope = (error - prev_error) / 0.001    # slope in m / s
        prev_error = error

        # Use PID gains to update applied force
        set_speed = (P_gain * error)
        set_speed += (I_gain * integrator_sum)
        set_speed += (D_gain * error_slope)

        # Update position
        position = position + (set_speed * 0.001)

        # Store data
        error_hist.append(error)
        position_hist.append(position)

    # Plot results
    plt.plot(time_array, target_array)
    plt.plot(time_array, position_hist)
    plt.show()


# --- TEST THE SIMULATION WITH DIFFERENT TARGETS AND GAINS --- #

P_gain = 20.0
I_gain = 0.0
D_gain = 0.0

run_simulation(target_step, time_array, P_gain, I_gain, D_gain)


