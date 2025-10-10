#!/usr/bin/env python3
"""
Enhanced ProjectileMotionVisualizer Demo
Shows all new features including initial accelerations and energy loss
"""

from plots import ProjectileMotionVisualizer

def main():
    print("=== Enhanced Projectile Motion Visualization Demo ===")
    print()
    
    # Create visualizer with custom folder name
    custom_folder = "enhanced_physics_plots"
    
    print(f"Creating visualizer with output folder: '{custom_folder}'")
    viz = ProjectileMotionVisualizer(output_folder=custom_folder)
    
    print(f"✓ Output directory created: {viz.output_dir}")
    print()
    
    # Display what new information is available
    print("📊 New Information Available:")
    if 'initial_acceleration_x' in viz.metadata:
        print(f"   • Initial X Acceleration: {viz.metadata['initial_acceleration_x']:.2f} m/s²")
        print(f"   • Initial Y Acceleration: {viz.metadata['initial_acceleration_y']:.2f} m/s²")
    else:
        print(f"   • Initial X Acceleration: {viz.x_accel[0]:.2f} m/s² (calculated)")
        print(f"   • Initial Y Acceleration: {viz.y_accel[0]:.2f} m/s² (calculated)")
    
    if 'energy_loss' in viz.metadata:
        energy_loss_percent = viz.metadata['energy_loss'] * 100
        print(f"   • Energy Loss: {energy_loss_percent:.3f}%")
    
    print(f"   • Initial Energy: {viz.metadata['energy_initial']:.2f} J")
    print(f"   • Final Energy: {viz.metadata['energy_final']:.2f} J")
    print()
    
    # Generate visualizations
    print("🎬 Generating Enhanced Visualizations...")
    print("   1. Static trajectory plot with all metadata...")
    viz.plot_trajectory(save_image=True)
    
    print("   2. Animated projectile motion...")
    anim = viz.animate_projectile(
        interval=60,           # Slightly slower for better viewing
        trail_length=20,       # Longer trail
        save_gif=True,
        save_mp4=True,
        filename_base="enhanced_projectile_motion"
    )
    
    print("   3. Velocity components analysis...")
    viz.plot_velocity_components(save_image=True)
    
    print("   4. Acceleration components analysis...")
    viz.plot_acceleration_components(save_image=True)
    
    print(f"\n✅ All visualizations saved to: {viz.output_dir}")
    print("\nFiles generated:")
    print("   • trajectory_plot.png")
    print("   • enhanced_projectile_motion.gif")
    print("   • enhanced_projectile_motion.mp4 (if ffmpeg available)")
    print("   • velocity_components.png")
    print("   • acceleration_components.png")

if __name__ == "__main__":
    main()