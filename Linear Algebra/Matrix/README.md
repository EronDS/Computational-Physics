# Matrix Transformations & Determinants

> **Definition** (Determinant): The determinant of a square matrix $(n \times n)$ $A$ is:

$$\det(A) = \sum_{\sigma \in S_n}\text{sgn}(\sigma)A_{1\sigma(1)} A_{2\sigma(2)} \cdots A_{n\sigma(n)}$$

$$= \epsilon_{j_1, j_2,\ldots,j_n} A_{j_1}^1 A_{j_2}^2 \cdots A_{j_n}^n$$

## 2×2 Case

For a $2 \times 2$ matrix $A$:

$$ A = \begin{pmatrix}
A_{11}  &  A_{12} \\
A_{21} & A_{22}
\end{pmatrix}
$$

$$\det(A) = \sum_{\sigma \in S_2} \text{sgn}(\sigma) A_{1\sigma(1)}A_{2\sigma(2)}$$

Since there are only 2 possible permutations in $S_2$:
- $\sigma: 1\rightarrow1,  2\rightarrow2$ (identity, $\text{sgn}(\sigma) = +1$)
- $\tau: 1\rightarrow 2, 2\rightarrow 1$ (single transposition, $\text{sgn}(\tau) = -1$)

Therefore:

$$\det(A) = \text{sgn}(\sigma)A_{1\sigma(1)}A_{2\sigma(2)} + \text{sgn}(\tau) A_{1\tau(1)}A_{2\tau(2)}$$

$$= 1 \cdot A_{11}A_{22} + (-1) \cdot A_{12}A_{21}$$

$$\boxed{\det(A) = A_{11}A_{22} - A_{12}A_{21}}$$

---

**Note**: $\det(A) \in \mathbb{R}$ or $\det(A) \in \mathbb{C}$ depending on the matrix entries.

> [!tip]
> Determinants are used to calculate the **cross product** in $\mathbb{R}^3$.

## Geometric Interpretation

The determinant $\det(A)$ represents the **scaling factor** of the linear transformation.

> [!abstract] Determinant as Dilatation Factor  
> The determinant of a linear transformation \( A \) describes how it scales or distorts space.

| Condition                       | Geometric Effect             | Interpretation                                                                                                         |
| :------------------------------ | :--------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| $\lvert \det(A) \rvert > 1$     | 🟢 **Expansion**             | The transformation **stretches** space (volume increases).                                                            |
| $\lvert \det(A) \rvert < 1$     | 🔵 **Contraction**           | The transformation **compresses** space (volume decreases).                                                           |
| $\det(A) < 0$                   | 🟣 **Orientation Reversal**  | Like a **mirror reflection** — orientation is flipped. The magnitude shows the **stretch/compression** factor.       |
| $\det(A) = 0$                   | 🔴 **Collapse / Degenerate** | The transformation **flattens** space (not invertible). Results in lower-dimensional output.                         |

> 💡 **Summary:**  
> - $\det(A)$ measures **volume scaling** in $\mathbb{R}^n$.  
