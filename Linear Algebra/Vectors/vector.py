import numpy as np
import math
from numba import jit, jitclass
from numba.types import int32, float32

# Usando Numba para compilação JIT (Just-In-Time)
# Isso compila automaticamente para código nativo na primeira execução

spec = [
    ('vec', int32[:]),
    ('size', int32)
]

@jitclass(spec)
class Vector:
    def __init__(self, vec_array):
        self.vec = vec_array
        self.size = len(vec_array)
    
    def length(self):
        sum_sq = 0.0
        for i in range(self.size):
            sum_sq += self.vec[i] ** 2
        return math.sqrt(sum_sq)

@jit(nopython=True)
def dot_product_fast(a, b):
    """Versão ultra-rápida compilada para código nativo"""
    if len(a) != len(b):
        raise ValueError("Vectors must be of the same length")
    
    dot_prod = 0.0
    for i in range(len(a)):
        dot_prod += a[i] * b[i]
    
    # Calcular comprimentos
    len_a = math.sqrt(sum(a[i]**2 for i in range(len(a))))
    len_b = math.sqrt(sum(b[i]**2 for i in range(len(b))))
    
    theta = math.acos(dot_prod / (len_a * len_b))
    
    return dot_prod, theta

# Versão simples usando NumPy (também muito rápida)
def dot_product_numpy(a, b):
    """Versão usando NumPy - simples e rápida"""
    a = np.array(a)
    b = np.array(b)
    
    dot_prod = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    theta = np.arccos(dot_prod / (norm_a * norm_b))
    
    return dot_prod, theta

# Exemplo de uso
if __name__ == "__main__":
    # Dados de teste
    vec1 = np.array([1, 2, 3], dtype=np.int32)
    vec2 = np.array([5, 4, 3], dtype=np.int32)
    
    print("=== Usando NumPy (mais fácil) ===")
    dot_np, angle_np = dot_product_numpy(vec1, vec2)
    print(f"Dot product: {dot_np}, Angle: {angle_np}")
    
    print("\n=== Usando Numba (compilação JIT) ===")
    dot_nb, angle_nb = dot_product_fast(vec1, vec2)
    print(f"Dot product: {dot_nb}, Angle: {angle_nb}")
    
    print("\n=== Usando classe Vector com Numba ===")
    v1 = Vector(vec1)
    v2 = Vector(vec2)
    print(f"Length v1: {v1.length()}")
    print(f"Length v2: {v2.length()}")
    
    # Benchmark simples
    import time
    
    # Dados maiores para testar performance
    big_vec1 = np.random.randint(1, 10, 10000, dtype=np.int32)
    big_vec2 = np.random.randint(1, 10, 10000, dtype=np.int32)
    
    # NumPy
    start = time.time()
    for _ in range(1000):
        dot_product_numpy(big_vec1, big_vec2)
    numpy_time = time.time() - start
    
    # Numba (primeira chamada compila)
    dot_product_fast(big_vec1, big_vec2)  # Compilação
    start = time.time()
    for _ in range(1000):
        dot_product_fast(big_vec1, big_vec2)
    numba_time = time.time() - start
    
    print(f"\n=== Benchmark (1000 iterações) ===")
    print(f"NumPy time: {numpy_time:.4f}s")
    print(f"Numba time: {numba_time:.4f}s")
    print(f"Speedup: {numpy_time/numba_time:.2f}x")