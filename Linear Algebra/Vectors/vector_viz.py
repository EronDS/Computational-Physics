import matplotlib.pyplot as plt
import numpy as np
import os 

class VectorVisualizer:
    def __init__(self, json_path:str|os.PathLike):
        import json
        with open(json_path, 'r') as f:
            self.data = json.load(f)
        
    def plot_vectors(self):
        vec_a = np.array(self.data["Vector A"])
        vec_b = np.array(self.data["Vector B"])
        
        # Extract metadata
        length_a = self.data["Vector A Length"][0]
        length_b = self.data["Vector B Length"][0]
        dot_product = self.data["Dot Product"][0]
        angle_rad = self.data["Angle (radians)"][0]
        angle_deg = np.degrees(angle_rad)
        
        origin = np.array([0, 0, 0])
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot vector A
        ax.quiver(*origin, vec_a[0], vec_a[1], vec_a[2], 
                 color='blue', label=f'Vector A: ({vec_a[0]}, {vec_a[1]}, {vec_a[2]})', 
                 arrow_length_ratio=0.1, linewidth=3)
        
        # Plot vector B
        ax.quiver(*origin, vec_b[0], vec_b[1], vec_b[2], 
                 color='green', label=f'Vector B: ({vec_b[0]}, {vec_b[1]}, {vec_b[2]})', 
                 arrow_length_ratio=0.1, linewidth=3)
        
        # Create angle arc/shading
        # Normalize vectors for angle calculation
        vec_a_norm = vec_a / np.linalg.norm(vec_a)
        vec_b_norm = vec_b / np.linalg.norm(vec_b)
        
        # Create points for the angle arc
        n_points = 20
        t = np.linspace(0, 1, n_points)
        
        # Create arc points using spherical linear interpolation (slerp)
        arc_points = []
        for ti in t:
            # Simple linear interpolation between normalized vectors
            interp_vec = (1-ti) * vec_a_norm + ti * vec_b_norm
            interp_vec = interp_vec / np.linalg.norm(interp_vec)  # Re-normalize
            arc_points.append(interp_vec * min(length_a, length_b) * 0.6)  # Scale based on smaller vector, more visible
        
        arc_points = np.array(arc_points)
        
        # Plot the angle arc
        ax.plot(arc_points[:, 0], arc_points[:, 1], arc_points[:, 2], 
               color='red', linewidth=4, alpha=0.9, label=f'Angle: {angle_deg:.1f}°')
        
        # Create angle shading (triangle fan from origin) - make it more substantial
        for i in range(len(arc_points)-1):
            # Create triangle vertices: origin, arc_point[i], arc_point[i+1]
            triangle = np.array([origin, arc_points[i], arc_points[i+1]])
            ax.plot_trisurf(triangle[:, 0], triangle[:, 1], triangle[:, 2], 
                           color='red', alpha=0.4)
        
        # Set axis limits based on vector magnitudes
        max_range = max(length_a, length_b) * 1.2
        ax.set_xlim([-max_range/2, max_range])
        ax.set_ylim([-max_range/2, max_range])
        ax.set_zlim([-max_range/2, max_range])
        
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Create comprehensive title and metadata text
        title = '3D Vector Analysis and Visualization'
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add metadata text box
        metadata_text = (
            f'Vector A: ({vec_a[0]:.3f}, {vec_a[1]:.3f}, {vec_a[2]:.3f})\n'
            f'Vector B: ({vec_b[0]:.3f}, {vec_b[1]:.3f}, {vec_b[2]:.3f})\n'
            f'|A| = {length_a:.3f}\n'
            f'|B| = {length_b:.3f}\n'
            f'A · B = {dot_product:.3f}\n'
            f'Angle = {angle_deg:.1f}° ({angle_rad:.3f} rad)\n'
            f'cos(θ) = {np.cos(angle_rad):.3f}'
        )
        
        # Position text box
        ax.text2D(0.02, 0.98, metadata_text, transform=ax.transAxes, 
                 fontsize=10, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                 family='monospace')
        
        # Legend
        ax.legend(loc='upper right', bbox_to_anchor=(1.0, 0.85))
        
        plt.tight_layout()
        plt.savefig("images/vector_visualization.png", dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    # Example usage
    viz = VectorVisualizer("vector_data.json")
    os.makedirs("images", exist_ok=True)
    viz.plot_vectors()
