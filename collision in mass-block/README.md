# Block-Spring Collision and Oscillation Simulation

This project simulates a perfectly inelastic collision between a projectile and a block attached to a spring, followed by the resulting harmonic oscillation.

## Animation

![Oscillator Visualizer](block_spring_oscillation.gif)

The animation shows:
- Block-spring system oscillating after collision
- Real-time plots of position, velocity, and acceleration
- Energy conservation verification (kinetic, potential, and total energy)
- System parameters and current values display


# Perfect Inelastic Collision 
- At perfect inelastic collision, the objects merge together at the moment of collision.

By conservation of momentum:
$$m_1v_1 + m_2v_2 = (m_1+m_2)v_f$$

So, the velocity after the impact can be shown as:
$$v_f = \frac{m_1v_1 + m_2v_2}{m_1+m_2}$$


# Harmonic Oscillator

After collision, the system follows a harmonic oscillator motion.

Position as a function of time:
$$x(t) = A\cos(\omega t)$$

where the angular frequency $\omega$ is:
$$\omega = \sqrt{\frac{k}{m_{total}}} = \sqrt{\frac{k}{m_1+m_2}}$$

Velocity and acceleration can be obtained by differentiating with respect to time:
$$v(t) = \frac{dx}{dt} = -A\omega\sin(\omega t)$$
$$a(t) = \frac{dv}{dt} = -A\omega^2\cos(\omega t)$$

The total energy of the system is given by:
$$E_{total} = E_{kinetic} + E_{potential} = \frac{1}{2}mv^2 + \frac{1}{2}kx^2$$

The amplitude of the harmonic oscillator can be obtained by conservation of energy:
$$\frac{1}{2}(m_1+m_2)v_f^2 = \frac{1}{2}kA^2$$

Therefore:
$$A = \sqrt{\frac{(m_1+m_2)v_f^2}{k}}$$

## Period and Frequency

The period and frequency of the oscillator can be obtained as:

Period:
$$T = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac{m_1+m_2}{k}}$$

Frequency:
$$f = \frac{1}{T} = \frac{\omega}{2\pi} = \frac{1}{2\pi}\sqrt{\frac{k}{m_1+m_2}}$$


# System Parameters (json_data/collision_in_mass_spring.json)

The simulation uses the following default parameters:
- Projectile mass: $m_1 = 2.0$ kg
- Block mass: $m_2 = 1.0$ kg  
- Initial projectile velocity: $v_1 = 10.0$ m/s
- Initial block velocity: $v_2 = 0.0$ m/s
- Spring constant: $k = 50.0$ N/m
- Number of cycles: 5
- Samples per cycle: 20

## Key Results

From these parameters, the system calculates:
- Final velocity after collision: $v_f = 6.67$ m/s
- Total mass: $m_{total} = 3.0$ kg
- Angular frequency: $\omega = 4.08$ rad/s
- Period: $T = 1.54$ s
- Frequency: $f = 0.65$ Hz
- Amplitude: $A = 1.63$ m

# Manual Calculations

The theoretical calculations can be found in the math & calculations folder.