import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
q = 1.6e-19      # Charge of particle
m = 1.67e-27     # Mass of particle
dt = 1e-10       # Time step
num_steps = 1000 # Number of time steps to simulate

# Initial conditions
r0 = np.array([0, 0, 0])    # Initial position
v0 = np.array([0, 0, 1e6]) # Initial velocity

# Electric field function (in V/m)
def E(x, y, z):
    return np.array([0, 0, 1e7]) 

# Magnetic field function (in T)
def B(x, y, z):
    return np.array([1e-4*np.cos(z/10), 1e-4*np.sin(z/10), 0])

# Initialize arrays to store position, velocity, and acceleration
r = np.zeros((num_steps, 3))
v = np.zeros((num_steps, 3))
a = np.zeros((num_steps, 3))

# Set initial position and velocity
r[0] = r0
v[0] = v0

# Run simulation
for i in range(1, num_steps):
    # Calculate acceleration using Lorentz force equation
    a[i] = (q/m) * (E(*r[i-1]) + np.cross(v[i-1], B(*r[i-1])))

    # Update position using Taylor series expansion
    r[i] = r[i-1] + v[i-1]*dt + 0.5*a[i-1]*dt**2

    # Update velocity using central difference approximation
    v[i] = v[i-1] + 0.5*(a[i] + a[i-1])*dt

    # Check for NaN or Inf values in position, velocity, or acceleration
    if np.isnan(r[i]).any() or np.isinf(r[i]).any() or np.isnan(v[i]).any() or np.isinf(v[i]).any() or np.isnan(a[i]).any() or np.isinf(a[i]).any():
        print("Particle's position, velocity, or acceleration is NaN or Inf. Stopping simulation.")
        break

# Plot trajectory
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(r[:,0], r[:,1], r[:,2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

# Plot velocity and acceleration
t = np.arange(0, num_steps*dt, dt)
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(t, v[:,0], label='v_x')
ax[0].plot(t, v[:,1], label='v_y')
ax[0].plot(t, v[:,2], label='v_z')
ax[0].set_ylabel('Velocity (m/s)')
ax[0].legend()
ax[1].plot(t, a[:,0], label='a_x')
ax[1].plot(t, a[:,1], label='a_y')
ax[1].plot(t, a[:,2], label='a_z')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Acceleration (m/s^2)')
ax[1].legend()
plt.show()

# Plot trajectory and electric/magnetic fields
fig = plt.figure

