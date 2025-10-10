#!/usr/bin/env python3
"""
Simple demonstration of the animated projectile motion
"""

from plots import ProjectileMotionVisualizer

def main():
    # Create the visualizer
    print("Creating ProjectileMotionVisualizer...")
    viz = ProjectileMotionVisualizer()
    
    print("Starting animation...")
    print("The animation will show:")
    print("- Red circle: the projectile")
    print("- Blue trail: path taken by the projectile")
    print("- Green arrow: velocity vector")
    print("- Info boxes: real-time data")
    print("\nClose the plot window to continue...")
    
    # Create the animation with customizable parameters
    anim = viz.animate_projectile(
        interval=50,        # 50ms between frames (20 FPS)
        trail_length=15,    # Show last 15 positions in trail
        save_gif=False      # Set to True if you want to save as GIF
    )
    
    print("Animation complete!")

if __name__ == "__main__":
    main()