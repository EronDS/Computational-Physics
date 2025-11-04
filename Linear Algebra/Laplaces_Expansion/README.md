# Laplace's Expansion
Laplace's Expansion offers a computational way for computing higher dimension determinants through recursion.

> [!NOTE]
> **Theorem (Laplace's Expansion Formula)**: Given an $n \times n$ matrix A,
> $$\det(A) = \sum_{j=1}^n A_{ij}\Delta_{ij} = \sum_{j=1}^n (-1)^{i+j}A_{ij}M_{ij}$$
> 
> For an $n \times n$ matrix $A$, define $A^{ij}$ to be the $(n-1) \times (n-1)$ matrix having the $i$-th row and $j$-th column of $A$ removed.
> 
> **Minor**: $M_{ij} = \det(A^{ij})$  
> **Cofactor**: $\Delta_{ij} = (-1)^{i+j}\det(A^{ij}) = (-1)^{i+j}M_{ij}$

## Implementation

```cpp
float determinant_of_matrix(const vector<vector<float>>& matrix) {
        // determinant for sub-matrix 2x2 main diagonal method
        if (matrix.size() == 3 && matrix[0].size() == 3){
            float det = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
                      - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
                      + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);
            return det;
        }
        else if(matrix.size() == 2 && matrix[0].size() == 2) {
            float det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
            return det;
        }
        else if(matrix.size() == 1 && matrix[0].size() == 1) {
            return matrix[0][0];
        }
        else{LaplacesExpansion le(matrix);
            //return le.sum_expansion();
            return le.getDeterminant(); // Recursive calculation for each matrix until reaching 3/2/1 dimensions
        }
    }
```

The recursive implementation handles matrices of any size by:
1. **Base cases**: Direct formulas for 1×1, 2×2, and 3×3 matrices
2. **Recursive case**: For larger matrices, creates minors and recursively computes their determinants
## Big O Analysis

### Time Complexity

The Laplace expansion has a **factorial time complexity**: **O(n!)**

**Detailed Analysis:**

For an n×n matrix using Laplace expansion along the first row:
- We compute n cofactors
- Each cofactor requires computing the determinant of an (n-1)×(n-1) matrix
- This creates a recursive tree structure

**Recurrence Relation:**
```
T(n) = n × T(n-1) + O(n²)
```
Where:
- `n × T(n-1)`: Computing n minors of size (n-1)×(n-1)
- `O(n²)`: Time to create each minor matrix (removing row/column)

**Solution:**
```
T(n) = n × (n-1) × (n-2) × ... × T(base_case)
T(n) = O(n!)
```

**Base Cases:**
- 1×1 matrix: O(1)
- 2×2 matrix: O(1)
- 3×3 matrix: O(1) (direct formula)

**Growth Analysis:**
| Matrix Size | Operations Required | Approximate Count |
|-------------|-------------------|-------------------|
| 3×3         | Direct formula    | ~10 operations    |
| 4×4         | 4 × 3×3          | ~40 operations    |
| 5×5         | 5 × 4×4          | ~200 operations   |
| 6×6         | 6 × 5×5          | ~1,200 operations |
| 7×7         | 7 × 6×6          | ~8,400 operations |
| 8×8         | 8 × 7×7          | ~67,200 operations|
| n×n         | n!               | n! operations     |

### Space Complexity

**O(n³)** due to:
- **Recursion depth**: O(n) - maximum recursion depth is n
- **Minor storage**: O(n²) - each recursive call stores minors in map
- **Matrix copies**: O(n²) - creating minor matrices


### Optimization Opportunities

1. **Memoization**: Store computed determinants to avoid recalculation
2. **Row/Column Selection**: Choose row/column with most zeros
3. **Alternative Algorithms**: 
   - LU Decomposition: O(n³)
   - Gaussian Elimination: O(n³)
4. **Numerical Stability**: Use double precision for larger matrices

### Practical Limitations

- **n ≤ 8**: Manageable computation time
- **n = 10**: ~3.6 million operations (slow but feasible)
- **n ≥ 12**: Impractical for real-time computation

> [!NOTE] 
> LU decomposition & Gaussian Elimination (to be implemented) will be used for larger matrices due to their superior O(n³) complexity.
