
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import os


class ProjectileMotionVisualizer:
    def __init__(self, json_file="projectile_motion_data.json", output_folder="plot_and_visualizers"):
        with open(json_file, 'r') as f:
            self.json_data = json.load(f)
        
        # Extract data for convenience
        self.time = np.array(self.json_data["time_series"]["time"])
        self.x_pos = np.array(self.json_data["time_series"]["position_x"])
        self.y_pos = np.array(self.json_data["time_series"]["position_y"])
        self.x_vel = np.array(self.json_data["time_series"]["velocity_x"])
        self.y_vel = np.array(self.json_data["time_series"]["velocity_y"])
        
        # Extract acceleration data if available
        if "acceleration_x" in self.json_data["time_series"]:
            self.x_accel = np.array(self.json_data["time_series"]["acceleration_x"])
            self.y_accel = np.array(self.json_data["time_series"]["acceleration_y"])
        else:
            # Calculate accelerations from velocity if not available
            self.x_accel = np.gradient(self.x_vel, self.time)
            self.y_accel = np.gradient(self.y_vel, self.time)
        
        # Metadata
        self.metadata = self.json_data["metadata"]
        
        # Create output directory
        self.output_dir = f"./{output_folder}"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def plot_trajectory(self, save_image=True):
        """Plot the complete trajectory"""
        plt.figure(figsize=(12, 8))
        plt.plot(self.x_pos, self.y_pos, 'b-', linewidth=2, label='Trajectory')
        plt.plot(self.x_pos[0], self.y_pos[0], 'go', markersize=8, label='Start')
        plt.plot(self.x_pos[-1], self.y_pos[-1], 'ro', markersize=8, label='End')
        
        # Mark the apogee
        apogee_idx = np.argmax(self.y_pos)
        plt.plot(self.x_pos[apogee_idx], self.y_pos[apogee_idx], 'o', 
                color='orange', markersize=10, label='Apogee')
        
        plt.xlabel('Horizontal Position (m)')
        plt.ylabel('Vertical Position (m)')
        plt.title('Projectile Motion Trajectory')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.axis('equal')
        
        # Add metadata text with all new information
        info_text = f"Max Height: {self.metadata['h_max']:.2f} m\n"
        info_text += f"Total Time: {self.metadata['total_time']:.2f} s\n"
        info_text += f"Apogee Time: {self.metadata['apogee_time']:.2f} s\n"
        
        # Add initial acceleration info if available
        if 'initial_acceleration_x' in self.metadata:
            info_text += f"Initial Accel X: {self.metadata['initial_acceleration_x']:.2f} m/s²\n"
            info_text += f"Initial Accel Y: {self.metadata['initial_acceleration_y']:.2f} m/s²\n"
        else:
            info_text += f"Initial Accel X: {self.x_accel[0]:.2f} m/s²\n"
            info_text += f"Initial Accel Y: {self.y_accel[0]:.2f} m/s²\n"
        
        # Add energy information if available
        if 'energy_loss' in self.metadata:
            energy_loss_percent = self.metadata['energy_loss'] * 100
            info_text += f"Energy Loss: {energy_loss_percent:.2f}%"
        
        plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        # Save image
        if save_image:
            filename = os.path.join(self.output_dir, "trajectory_plot.png")
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Trajectory plot saved as: {filename}")
        
        plt.show()
    
    def animate_projectile(self, interval=50, trail_length=20, save_gif=True, save_mp4=True, filename_base="projectile_motion"):
        """
        Animate the projectile motion
        
        Parameters:
        interval: Animation interval in milliseconds
        trail_length: Number of points to show in the trail
        save_gif: Whether to save animation as GIF
        filename: Name of the GIF file if saving
        """
        fig, ax = plt.subplots(figsize=(15, 10))
        
        # Set up the plot with margins for text
        ax.set_xlim(-max(self.x_pos) * 0.05, max(self.x_pos) * 1.1)
        ax.set_ylim(-max(self.y_pos) * 0.05, max(self.y_pos) * 1.15)
        ax.set_xlabel('Horizontal Position (m)', fontsize=12)
        ax.set_ylabel('Vertical Position (m)', fontsize=12)
        ax.set_title('Animated Projectile Motion', fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        # Initialize plot elements
        projectile = Circle((0, 0), radius=max(self.x_pos)*0.005, 
                           color='red', zorder=5)
        ax.add_patch(projectile)
        
        trail_line, = ax.plot([], [], 'b-', alpha=0.7, linewidth=2, label='Trail')
        velocity_arrow = ax.annotate('', xy=(0, 0), xytext=(0, 0),
                                   arrowprops=dict(arrowstyle='->', color='green', lw=2),
                                   zorder=4)
        
        # Text display - all in one box
        info_text = ax.text(0.02, 0.90, '', transform=ax.transAxes, fontsize=11,
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.9),
                           verticalalignment='top')
        
        # Metadata in a separate corner - including all new information
        metadata_info = f"Max Height: {self.metadata['h_max']:.2f} m\n"
        metadata_info += f"Total Time: {self.metadata['total_time']:.2f} s\n"
        metadata_info += f"Range: {self.x_pos[-1]:.2f} m\n"
        
        # Add initial acceleration info
        if 'initial_acceleration_x' in self.metadata:
            metadata_info += f"Initial Accel X: {self.metadata['initial_acceleration_x']:.2f} m/s²\n"
            metadata_info += f"Initial Accel Y: {self.metadata['initial_acceleration_y']:.2f} m/s²\n"
        else:
            metadata_info += f"Initial Accel X: {self.x_accel[0]:.2f} m/s²\n"
            metadata_info += f"Initial Accel Y: {self.y_accel[0]:.2f} m/s²\n"
        
        metadata_info += f"Initial Energy: {self.metadata['energy_initial']:.2f} J\n"
        metadata_info += f"Final Energy: {self.metadata['energy_final']:.2f} J\n"
        
        # Add energy loss if available
        if 'energy_loss' in self.metadata:
            energy_loss_percent = self.metadata['energy_loss'] * 100
            metadata_info += f"Energy Loss: {energy_loss_percent:.2f}%\n"
        
        metadata_info += f"Angle of Collapse: {self.metadata['angle_of_collapse']:.2f}°"
        
        metadata_text = ax.text(0.98, 0.97, metadata_info,
                               transform=ax.transAxes, fontsize=9,
                               verticalalignment='top', horizontalalignment='right',
                               bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.9))
        
        
        def animate(frame):
            if frame >= len(self.time):
                return projectile, trail_line, velocity_arrow, info_text
            
            # Current position and velocity
            x, y = self.x_pos[frame], self.y_pos[frame]
            vx, vy = self.x_vel[frame], self.y_vel[frame]
            
            # Update projectile position
            projectile.center = (x, y)
            
            # Update trail
            start_idx = max(0, frame - trail_length)
            trail_x = self.x_pos[start_idx:frame+1]
            trail_y = self.y_pos[start_idx:frame+1]
            trail_line.set_data(trail_x, trail_y)
            
            # Update velocity arrow (scaled for visibility)
            scale = max(self.x_pos) * 0.001
            velocity_arrow.set_position((x, y))
            velocity_arrow.xy = (x + vx * scale, y + vy * scale)
            
            # Update text information in single box
            speed = np.sqrt(vx**2 + vy**2)
            info_text.set_text(f'Time: {self.time[frame]:.2f} s\n'
                              f'Position: ({x:.1f}, {y:.1f}) m\n'
                              f'Velocity: ({vx:.1f}, {vy:.1f}) m/s\n'
                              f'Speed: {speed:.1f} m/s')
            
            return projectile, trail_line, velocity_arrow, info_text
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=len(self.time),
                                     interval=interval, blit=True, repeat=True)
        
        plt.tight_layout()
        
        # Save animation files
        if save_gif:
            gif_filename = os.path.join(self.output_dir, f"{filename_base}.gif")
            print(f"Saving animation as GIF: {gif_filename}...")
            anim.save(gif_filename, writer='pillow', fps=1000//interval)
            print("GIF saved!")
        
        if save_mp4:
            mp4_filename = os.path.join(self.output_dir, f"{filename_base}.mp4")
            print(f"Saving animation as MP4: {mp4_filename}...")
            try:
                anim.save(mp4_filename, writer='ffmpeg', fps=1000//interval, bitrate=1800)
                print("MP4 saved!")
            except Exception as e:
                print(f"Could not save MP4 (ffmpeg may not be installed): {e}")
                print("Trying alternative writer...")
                try:
                    anim.save(mp4_filename, writer='html', fps=1000//interval)
                    print("HTML animation saved instead!")
                except Exception as e2:
                    print(f"Could not save video file: {e2}")
        
        plt.show()
        return anim
    
    def plot_velocity_components(self, save_image=True):
        """Plot velocity components over time"""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # X velocity
        ax1.plot(self.time, self.x_vel, 'b-', linewidth=2, label='Vx')
        ax1.set_ylabel('X Velocity (m/s)')
        ax1.set_title('Velocity Components vs Time')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Y velocity
        ax2.plot(self.time, self.y_vel, 'r-', linewidth=2, label='Vy')
        ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax2.set_ylabel('Y Velocity (m/s)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Speed (magnitude)
        speed = np.sqrt(self.x_vel**2 + self.y_vel**2)
        ax3.plot(self.time, speed, 'g-', linewidth=2, label='Speed')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Speed (m/s)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        plt.tight_layout()
        
        # Save image
        if save_image:
            filename = os.path.join(self.output_dir, "velocity_components.png")
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Velocity components plot saved as: {filename}")
        
        plt.show()


# Example usage
if __name__ == "__main__":
    # Create visualizer with custom output folder
    symmetric_json = "projectile_motion_data_symmetric.json"
    non_symmetric_json = "projectile_motion_data_non_symmetric.json"

    output_folder_name_symmetric = "plot_and_visualizers_symmetric"
    output_folder_name_non_symmeitrc = "plot_and_visualizers_non_symmetric"
    viz = ProjectileMotionVisualizer(json_file= non_symmetric_json,output_folder=output_folder_name_non_symmeitrc)
    
    print(f"Output directory: {viz.output_dir}")
    # Show different visualizations and save them
    print("\n1. Plotting complete trajectory...")
    viz.plot_trajectory(save_image=True)
    
    print("2. Creating animated visualization...")
    anim = viz.animate_projectile(interval=50, trail_length=15, save_gif=True, save_mp4=True)
    
    print("3. Plotting velocity components...")
    viz.plot_velocity_components(save_image=True)
    
    print("\nAll visualizations have been saved to the plot_and_visualizers directory!")
    


