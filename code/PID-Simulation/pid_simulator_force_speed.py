
from matplotlib import pyplot as plt
from math import *
import random


# Length of simulation
timesteps = 10000   # in milliseconds
time_arr = [i / 1000.0 for i in range(timesteps)]

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

# --- OTHER PARAMS FOR THIS SIMULATION --- #

# External force acting on the object
ext_force_none = [0.0 for i in range(timesteps)]
ext_force_const = [9.81 for i in range(timesteps)]

# Mass of the object position
mass = 1.0       # in kg


# --- FUNCTION TO RUN THE SIMULATION --- #


def run_simulation(target_array, time_array, ext_force_arr,  p_gain, i_gain, d_gain):

    # Current position and velocity of object
    position = 0.0  # in meters
    velocity = 0.0  # in m / s

    # Keep track of data for graphing
    position_hist = []
    error_hist = []
    apf_hist = []

    # PID variables
    integrator_sum = 0
    prev_error = 0

    # Run simulation
    for step in range(len(time_array)):

        # Calculate error for this time step
        pos_error = target_array[step] - position            # error in meters

        # Update PID variables
        integrator_sum += pos_error                       # cumulative error in meters
        error_slope = (pos_error - prev_error) / 0.001    # slope in m / s
        prev_error = pos_error

        # Use PID gains to update applied force
        target_speed = (p_gain * pos_error)
        target_speed += (i_gain * integrator_sum)
        target_speed += (d_gain * error_slope)

        # Determine force to apply to achieve target speed
        vel_error = target_speed - velocity
        applied_force = (vel_error / 0.001) * mass

        # limit applied force
        if applied_force > 100.0:
            applied_force = 100.0
        elif applied_force < -100.0:
            applied_force = -100.0

        # Update object position and velocity
        total_force = applied_force + ext_force_arr[i]
        accel = total_force / mass
        position = position + (velocity * 0.001) + (0.5 * accel * pow(0.001, 2))
        velocity = velocity + accel * 0.001

        # Store data
        error_hist.append(pos_error)
        position_hist.append(position)
        apf_hist.append(applied_force)

    # Plot results
    plt.plot(time_array, target_array)
    plt.plot(time_array, position_hist)
    # plt.plot(time_array, apf_hist)
    plt.show()


# --- TEST THE SIMULATION WITH DIFFERENT TARGETS AND GAINS --- #

P_gain = 5.0
I_gain = 0.0
D_gain = 0.0

run_simulation(target_step, time_arr, ext_force_none, P_gain, I_gain, D_gain)
