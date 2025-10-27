import numpy as np  
from matplotlib import pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")


class Matrix:
    def __init__(self, type:str, vector_space_type:str, n:int = 100,save_path:str = "./Matrix/figures/default.png", **matrix_kwargs) -> None:
        """
        Initializes the Matrix class with a given 2D numpy array.

        Parameters:
        type (str): The type of matrix transformation ('rotation', 'scaling', 'shearing', 'reflection', 'collapse').
        vector_space_type (str): The type of vector space ('rectangular', 'circular').
        n (int): Number of elements in the vector space (sampling points). Default is 100.
        matrix_kwargs: Additional keyword arguments for matrix creation.
        Example:
        {"rotation": ["angle"],
        "scaling": ["scale_x", "scale_y"],
        "shearing": ["shear_x", "shear_y"],
        "reflection": [],
        "collapse": []}
        Returns:
        self.Matrix: An instance of the Matrix (np.ndarray) used for transformations.
        self.n (int): Number of elements in the vector space.
        self.vector_space_elements (np.ndarray): The created vector space.


        Raises:
        ValueError: If the provided type is not supported.

        """

        self.matrix_kwargs = matrix_kwargs
        self.save_path = save_path
        self.available_matrix_kwargs = {"rotation": ["angle"],
                                        "scaling": ["scale_x", "scale_y"],
                                        "shearing": ["shear_x", "shear_y"],
                                        "reflection": []}
        
        # Validate matrix kwargs if provided
        if matrix_kwargs:
            for key in matrix_kwargs.keys():
                if key not in self.available_matrix_kwargs:
                    raise ValueError(f"Matrix type '{key}' not supported. Available types are: {list(self.available_matrix_kwargs.keys())}")
                # Check if the provided kwargs match the expected ones for this type
                expected_kwargs = self.available_matrix_kwargs[key]
                if expected_kwargs:  # Only check if there are expected kwargs
                    provided_kwargs = list(matrix_kwargs[key].keys()) if isinstance(matrix_kwargs[key], dict) else []
                    for expected_kwarg in expected_kwargs:
                        if expected_kwarg not in provided_kwargs:
                            print(f"Warning: Expected kwarg '{expected_kwarg}' not provided for type '{key}'. Using default value.")

        self.available_types:list[str] = ['rotation','scaling','shearing','reflection', 'collapse']
        self.available_vector_spaces:list[str] = ["rectangular", "circular"]

        if type not in self.available_types:
            raise ValueError(f"Type '{type}' is not supported. Available types are: {self.available_types}")
        
        self.type:str = type
        self.vector_space_type:str = vector_space_type

        self.vector_space_elements:np.ndarray = self._create_vector_space(vector_space_type, n)
        self.n:int = n
        self.Matrix:np.ndarray = self._create_transformation_matrix()


        self.determinant:float = np.linalg.det(self.Matrix)

        self.vector_space_elements_prime:np.ndarray = self.applyTransform(self.vector_space_elements)

        self.visualize()


    def applyTransform(self,vector_space_elements:np.ndarray) -> np.ndarray:
        """
        Applies the matrix transformation to the given vector space.

        $A\vec{v} = \vec{v'}$

        Parameters:
        vector_space (np.ndarray): The vector space to transform.

        Returns:
        np.ndarray: The transformed vector space.
        """
        self.vector_space_elements = vector_space_elements
        self.vector_space_elements_prime =  np.dot(self.Matrix, vector_space_elements)
        return self.vector_space_elements_prime

    def _create_transformation_matrix(self) -> np.ndarray:
        """
        Creates a transformation matrix based on the specified type.

        Returns:
        np.ndarray: The created transformation matrix.
        """

        if self.type == "rotation":
            # Use provided angle or default to 45 degrees
            angle = self.matrix_kwargs.get(self.type, {}).get("angle", np.pi / 4)
            matrix = np.array([[np.cos(angle), -np.sin(angle)],
                               [np.sin(angle), np.cos(angle)]])
        elif self.type == "collapse":
            # Collapse transformation matrix
            matrix = np.array([[1, 1],
                               [2, 2]])
            
        elif self.type == "scaling":
            # Use provided scaling factors or defaults
            scale_x = self.matrix_kwargs.get(self.type, {}).get("scale_x", 2)
            scale_y = self.matrix_kwargs.get(self.type, {}).get("scale_y", 3)
            matrix = np.array([[scale_x, 0],
                               [0, scale_y]])

        elif self.type == "shearing":
            # Use provided shearing factors or defaults
            shear_x = self.matrix_kwargs.get(self.type, {}).get("shear_x", 1)
            shear_y = self.matrix_kwargs.get(self.type, {}).get("shear_y", 0)
            matrix = np.array([[1, shear_x],
                               [shear_y, 1]])

        elif self.type == "reflection":
            # Reflection over x-axis (no parameters needed)
            matrix = np.array([[1, 0],
                               [0, -1]])

        else:
            raise ValueError(f"Matrix type '{self.type}' is not supported.")

        return matrix
    def _create_vector_space(self, vector_space_type:str, n:int) -> np.ndarray:
        """
        Creates a vector space based on the specified type.

        Parameters:
        vector_space_type (str): The type of vector space to create.
        n (int): Number of elements in the vector space.

        Returns:
        np.ndarray: The created vector space.
        """

        if vector_space_type == "rectangular":
            # Create a dense grid that has at least n points to sample from
            grid_density = max(20, int(np.sqrt(n * 2)))  # Ensure we have enough points
            x = np.linspace(-1, 1, grid_density)
            y = np.linspace(-1, 1, grid_density)
            X, Y = np.meshgrid(x, y)
            all_vectors = np.vstack([X.ravel(), Y.ravel()])
            
            # Randomly sample exactly n points from the grid
            total_points = all_vectors.shape[1]
            if n > total_points:
                # If n is larger than available points, use all points
                vectors = all_vectors
                print(f"Requested {n} points but only {total_points} available. Using all {total_points} points from {grid_density}x{grid_density} grid")
            else:
                # Sample exactly n points
                sample_indices = np.random.choice(total_points, size=n, replace=False)
                vectors = all_vectors[:, sample_indices]
                print(f"Sampled {n} points from {grid_density}x{grid_density} rectangular grid ({total_points} total points available)")

        elif vector_space_type == "circular":
            theta = np.linspace(0, 2 * np.pi, n)
            r = 1
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            vectors = np.vstack([x, y])
            print(f"Created circular space: {n} points")

        else:
            raise ValueError(f"Vector space type '{vector_space_type}' is not supported.")

        return vectors
    def visualize(self) -> None:
        """
        Visualizes the matrix transformation.
        with seaborn and matplotlib.
        Returns:
        None

        """
        import os

        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        if self.vector_space_type == "rectangular":
            ax1.scatter(self.vector_space_elements[0, :], 
                       self.vector_space_elements[1, :], 
                       c='blue', s=50, alpha=0.8, label='Original Vectors', edgecolors='navy', linewidth=0.5)
        else:  # circular
            # For circular, show as a line
            ax1.plot(self.vector_space_elements[0, :], 
                    self.vector_space_elements[1, :], 
                    'b-', linewidth=2, label='Original Circle')
            ax1.scatter(self.vector_space_elements[0, :], 
                       self.vector_space_elements[1, :], 
                       c='blue', s=30, alpha=0.8, edgecolors='navy', linewidth=0.5)
        
        # Add basis vectors to original space
        # Standard basis vectors: e1 = [1,0], e2 = [0,1]
        ax1.arrow(0, 0, 1, 0, head_width=0.05, head_length=0.08, fc='green', ec='green', linewidth=3, label='$\hat{i}$')
        ax1.arrow(0, 0, 0, 1, head_width=0.05, head_length=0.08, fc='orange', ec='orange', linewidth=3, label='$\hat{j}$')

        ax1.set_title('Original Vector Space', fontsize=14, fontweight='bold')
        ax1.set_xlabel('x', fontsize=12)
        ax1.set_ylabel('y', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        ax1.legend()
        
        # Transformed vector space (right plot)
        if self.vector_space_type == "rectangular":
            ax2.scatter(self.vector_space_elements_prime[0, :], 
                       self.vector_space_elements_prime[1, :], 
                       c='red', s=50, alpha=0.8, label='Transformed Vectors', edgecolors='darkred', linewidth=0.5)
        else:  # circular
            ax2.plot(self.vector_space_elements_prime[0, :], 
                    self.vector_space_elements_prime[1, :], 
                    'r-', linewidth=2, label='Transformed Circle')
            ax2.scatter(self.vector_space_elements_prime[0, :], 
                       self.vector_space_elements_prime[1, :], 
                       c='red', s=30, alpha=0.8, edgecolors='darkred', linewidth=0.5)
        
        # Add transformed basis vectors
        # Transform the basis vectors: A*e1 and A*e2
        transformed_e1 = self.Matrix @ np.array([1, 0])  # First column of matrix
        transformed_e2 = self.Matrix @ np.array([0, 1])  # Second column of matrix
        
        ax2.arrow(0, 0, transformed_e1[0], transformed_e1[1], 
                 head_width=0.05, head_length=0.08, fc='green', ec='green', linewidth=3, label="$A·\hat{i}$")
        ax2.arrow(0, 0, transformed_e2[0], transformed_e2[1], 
                 head_width=0.05, head_length=0.08, fc='orange', ec='orange', linewidth=3, label="$A·\hat{j}$")

        ax2.set_title('Transformed Vector Space', fontsize=14, fontweight='bold')
        ax2.set_xlabel('x', fontsize=12)
        ax2.set_ylabel('y', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        ax2.legend()
        
        # Create main title with matrix information
        matrix_str = f"⎡{self.Matrix[0,0]:8.3f}  {self.Matrix[0,1]:8.3f}⎤\n⎣{self.Matrix[1,0]:8.3f}  {self.Matrix[1,1]:8.3f}⎦"
        
        fig.suptitle(f"{self.type.capitalize()} Transformation\n" +
                    f"Transformation Matrix A:\n" +
                    matrix_str + f"\ndet(A) = {self.determinant:.3f}", 
                    fontsize=16, fontweight='bold', fontfamily='monospace')
        
        # Adjust layout to prevent overlap
        plt.tight_layout()
        plt.subplots_adjust(top=0.75)
        
        # Save as PNG image
        plt.savefig(self.save_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print(f"Matrix transformation visualization created!")
        print(f"Type: {self.type.capitalize()} transformation")
        print(f"Vector space: {self.vector_space_type}")
        print(f"Matrix:")
        print(f"⎡{self.Matrix[0,0]:8.3f}  {self.Matrix[0,1]:8.3f}⎤")
        print(f"⎣{self.Matrix[1,0]:8.3f}  {self.Matrix[1,1]:8.3f}⎦")
        print(f"Determinant: {self.determinant:.3f}")
        print(f"PNG image saved as: {self.save_path}")
        
        return 
    

if __name__ == "__main__":
    import os 
    os.makedirs("./Matrix/figures", exist_ok=True)

    matrix_operation_types:list[str] = ['rotation','scaling','shearing','reflection', 'collapse']

    for matrix_type in matrix_operation_types:
        matrix = Matrix(type=matrix_type, vector_space_type="rectangular", n=1800,
                        save_path = f"./Matrix/figures/{matrix_type}.png")
        print(f"{matrix_type.capitalize()} Transformation:")
        print(matrix.vector_space_elements.shape)
        print(matrix.vector_space_elements_prime.shape)