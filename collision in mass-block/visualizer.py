import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D
import os

# Load the JSON data
def load_data():
    with open('json_data/collision_in_mass_spring.json', 'r') as f:
        data = json.load(f)
    return data

def create_oscillation_animation():
    # Load data
    data = load_data()
    system_info = data['system_info']
    osc_info = data['oscillation_info']
    
    # Extract parameters
    mass = system_info['mass']
    k = system_info['k']
    amplitude = system_info['Amplitude']
    
    # Extract time series data (time is already in seconds)
    time = np.array(osc_info['time'])
    position = np.array(osc_info['position'])
    velocity = np.array(osc_info['velocity'])
    acceleration = np.array(osc_info['acceleration'])
    kinetic_energy = np.array(osc_info['kinetic_energy'])
    potential_energy = np.array(osc_info['potential_energy'])
    total_energy = np.array(osc_info['total_energy'])
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # Layout: 2 rows, 3 columns
    # Top row: Animation and Energy plot
    # Bottom row: Position, Velocity, Acceleration plots
    
    # Animation subplot (top left, larger)
    ax_anim = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=1)
    
    # Energy plot (top right)
    ax_energy = plt.subplot2grid((3, 3), (0, 2), rowspan=1)
    
    # Bottom row plots
    ax_pos = plt.subplot2grid((3, 3), (1, 0), rowspan=1)
    ax_vel = plt.subplot2grid((3, 3), (1, 1), rowspan=1)
    ax_acc = plt.subplot2grid((3, 3), (1, 2), rowspan=1)
    
    # Additional plot for total energy verification
    ax_total = plt.subplot2grid((3, 3), (2, 0), colspan=3, rowspan=1)
    
    # Set up animation subplot
    ax_anim.set_xlim(-0.5, 3.5)
    ax_anim.set_ylim(-0.5, 1.5)
    ax_anim.set_aspect('equal')
    ax_anim.set_title('Block-Spring Oscillation Animation', fontsize=14, fontweight='bold')
    ax_anim.grid(True, alpha=0.3)
    
    # Spring visualization parameters
    equilibrium_pos = 1.5  # Position where spring is at natural length
    spring_coils = 8
    block_size = 0.2
    
    # Create spring coordinates (zigzag pattern)
    def create_spring_coords(x_block):
        # Spring extends from wall (x=0) to block
        spring_x = np.linspace(0.05, x_block - block_size/2, spring_coils * 4)
        spring_y = np.zeros_like(spring_x)
        
        # Create zigzag pattern
        for i in range(1, len(spring_x) - 1):
            if i % 4 == 1:
                spring_y[i] = 0.1
            elif i % 4 == 3:
                spring_y[i] = -0.1
        
        return spring_x, spring_y + 0.5
    
    # Initialize animation elements
    wall = Rectangle((-0.1, 0.3), 0.1, 0.4, facecolor='gray', edgecolor='black')
    ax_anim.add_patch(wall)
    
    block = Rectangle((0, 0.4), block_size, block_size, facecolor='red', edgecolor='black')
    ax_anim.add_patch(block)
    
    spring_line, = ax_anim.plot([], [], 'b-', linewidth=2, label='Spring')
    
    # Add equilibrium line
    ax_anim.axvline(x=equilibrium_pos, color='green', linestyle='--', alpha=0.5, label='Equilibrium')
    
    # Info text
    info_text = ax_anim.text(0.02, 0.98, '', transform=ax_anim.transAxes, 
                            verticalalignment='top', fontsize=10,
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax_anim.legend(loc='upper right')
    
    # Set up energy plot
    ax_energy.set_title('Energy vs Time', fontweight='bold')
    ax_energy.set_xlabel('Time (s)')
    ax_energy.set_ylabel('Energy (J)')
    ax_energy.grid(True, alpha=0.3)
    
    ke_line, = ax_energy.plot([], [], 'r-', linewidth=2, label='Kinetic Energy')
    pe_line, = ax_energy.plot([], [], 'b-', linewidth=2, label='Potential Energy')
    te_line, = ax_energy.plot([], [], 'g-', linewidth=2, label='Total Energy')
    energy_point, = ax_energy.plot([], [], 'ko', markersize=8)
    
    ax_energy.legend()
    ax_energy.set_xlim(0, max(time))
    ax_energy.set_ylim(0, max(total_energy) * 1.1)
    
    # Set up position plot
    ax_pos.set_title('Position vs Time', fontweight='bold')
    ax_pos.set_xlabel('Time (s)')
    ax_pos.set_ylabel('Position (m)')
    ax_pos.grid(True, alpha=0.3)
    pos_line, = ax_pos.plot([], [], 'b-', linewidth=2)
    pos_point, = ax_pos.plot([], [], 'ro', markersize=8)
    ax_pos.set_xlim(0, max(time))
    ax_pos.set_ylim(min(position) * 1.1, max(position) * 1.1)
    
    # Set up velocity plot
    ax_vel.set_title('Velocity vs Time', fontweight='bold')
    ax_vel.set_xlabel('Time (s)')
    ax_vel.set_ylabel('Velocity (m/s)')
    ax_vel.grid(True, alpha=0.3)
    vel_line, = ax_vel.plot([], [], 'r-', linewidth=2)
    vel_point, = ax_vel.plot([], [], 'ro', markersize=8)
    ax_vel.set_xlim(0, max(time))
    ax_vel.set_ylim(min(velocity) * 1.1, max(velocity) * 1.1)
    
    # Set up acceleration plot
    ax_acc.set_title('Acceleration vs Time', fontweight='bold')
    ax_acc.set_xlabel('Time (s)')
    ax_acc.set_ylabel('Acceleration (m/s²)')
    ax_acc.grid(True, alpha=0.3)
    acc_line, = ax_acc.plot([], [], 'g-', linewidth=2)
    acc_point, = ax_acc.plot([], [], 'ro', markersize=8)
    ax_acc.set_xlim(0, max(time))
    ax_acc.set_ylim(min(acceleration) * 1.1, max(acceleration) * 1.1)
    
    # Set up total energy verification plot
    ax_total.set_title('Energy Conservation Verification', fontweight='bold')
    ax_total.set_xlabel('Time (s)')
    ax_total.set_ylabel('Energy (J)')
    ax_total.grid(True, alpha=0.3)
    ax_total.plot(time, kinetic_energy, 'r-', linewidth=2, label='Kinetic Energy', alpha=0.7)
    ax_total.plot(time, potential_energy, 'b-', linewidth=2, label='Potential Energy', alpha=0.7)
    ax_total.plot(time, total_energy, 'g-', linewidth=2, label='Total Energy', alpha=0.7)
    total_point, = ax_total.plot([], [], 'ko', markersize=8)
    ax_total.legend()
    ax_total.set_xlim(0, max(time))
    ax_total.set_ylim(0, max(total_energy) * 1.1)
    
    # Animation function
    def animate(frame):
        # Current data point
        current_time = time[frame]
        current_pos = position[frame]
        current_vel = velocity[frame]
        current_acc = acceleration[frame]
        current_ke = kinetic_energy[frame]
        current_pe = potential_energy[frame]
        current_te = total_energy[frame]
        
        # Update block position (oscillates around equilibrium position)
        block_x = equilibrium_pos + current_pos
        block.set_x(block_x - block_size/2)
        
        # Update spring
        spring_x, spring_y = create_spring_coords(block_x)
        spring_line.set_data(spring_x, spring_y)
        
        # Update info text
        info_text.set_text(f'Time: {current_time:.3f} s\n'
                          f'Position: {current_pos:.3f} m\n'
                          f'Velocity: {current_vel:.3f} m/s\n'
                          f'Acceleration: {current_acc:.3f} m/s²\n'
                          f'KE: {current_ke:.3f} J\n'
                          f'PE: {current_pe:.3f} J\n'
                          f'Total E: {current_te:.3f} J')
        
        # Update energy plots
        ke_line.set_data(time[:frame+1], kinetic_energy[:frame+1])
        pe_line.set_data(time[:frame+1], potential_energy[:frame+1])
        te_line.set_data(time[:frame+1], total_energy[:frame+1])
        energy_point.set_data([current_time], [current_te])
        
        # Update position plot
        pos_line.set_data(time[:frame+1], position[:frame+1])
        pos_point.set_data([current_time], [current_pos])
        
        # Update velocity plot
        vel_line.set_data(time[:frame+1], velocity[:frame+1])
        vel_point.set_data([current_time], [current_vel])
        
        # Update acceleration plot
        acc_line.set_data(time[:frame+1], acceleration[:frame+1])
        acc_point.set_data([current_time], [current_acc])
        
        # Update total energy verification point
        total_point.set_data([current_time], [current_te])
        
        return (block, spring_line, info_text, ke_line, pe_line, te_line, energy_point,
                pos_line, pos_point, vel_line, vel_point, acc_line, acc_point, total_point)
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=len(time), 
                                 interval=200, blit=False, repeat=True)
    
    plt.tight_layout()
    
    # Save as GIF
    print("Saving animation as GIF...")
    anim.save('block_spring_oscillation.gif', writer='pillow', fps=5, dpi=100)
    
    # Save as MP4 (requires ffmpeg)
    try:
        print("Saving animation as MP4...")
        anim.save('block_spring_oscillation.mp4', writer='ffmpeg', fps=5, dpi=100)
        print("MP4 saved successfully!")
    except Exception as e:
        print(f"Could not save MP4: {e}")
        print("Make sure ffmpeg is installed for MP4 export")
    
    print("GIF saved successfully!")
    
    # Show the animation
    plt.show()
    
    return anim

if __name__ == "__main__":
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Creating block-spring oscillation animation...")
    print("System parameters from JSON:")
    
    data = load_data()
    system_info = data['system_info']
    
    print(f"Mass: {system_info['mass']:.3f} kg")
    print(f"Spring constant: {system_info['k']:.3f} N/m")
    print(f"Amplitude: {system_info['Amplitude']:.3f} m")
    print(f"Angular frequency: {system_info['w']:.3f} rad/s")
    print(f"Frequency: {system_info['frequency']:.3f} Hz")
    print(f"Period: {system_info['period']:.3f} s")
    print(f"Initial kinetic energy: {system_info['kinectic_energy']:.3f} J")
    print(f"System velocity at collision: {system_info['system_velocity_at_collision']:.3f} m/s")
    print(f"Total simulation time: {system_info['total_time']:.3f} s")
    print()
    
    anim = create_oscillation_animation()
