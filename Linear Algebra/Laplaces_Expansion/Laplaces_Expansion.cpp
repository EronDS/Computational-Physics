#include <vector>
#include <map>
#include <cmath>

using namespace std;

class LaplacesExpansion {
    public:
    vector<vector<float>> A;
    map<pair<int, int>, vector<vector<float>>> M;
    int I, J;

    LaplacesExpansion(const vector<vector<float>>& matrix){
        A = matrix;
        // Initialize M (Minors submatrices) based on the size of A
        I = A.size();
        J = A[0].size();

        this->computeExpansion();
    }
    
    void computeExpansion() {
        for(int i = 0; i < I; i++) {
            for(int j = 0; j < J; j++) {
                M[{i, j}] = get_minor(i, j);                
            }
        }

        float determinant = this->sum_expansion();
    }

    private:

    vector<vector<float>> get_minor(int row, int col) {
        vector<vector<float>> m = A;
        m.erase(m.begin() + row);
        for (int i = 0; i < m.size(); i++) {
            m[i].erase(m[i].begin() + col);
        }
        return m;
    }

    float determinant_of_matrix(const vector<vector<float>>& matrix) {
        // determinant for sub-matrix 2x2 main diagonal method
        if(matrix.size() == 2 && matrix[0].size() == 2) {
            float det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
            return det;
        }
        return 0.0; // Para casos não esperados
    }

    float sum_expansion() {
        float determinant = 0.0;
        for(int j = 0; j < J; j++) {
            float sign = pow(-1, 0 + j); // (-1)^(i+j) para i=0
            float minor_det = determinant_of_matrix(this->M[{0, j}]); // Usar o minor, não o cofactor
            determinant += this->A[0][j] * sign * minor_det;
        }
        return determinant;
    }
    
    public:
    float getDeterminant() {
        return sum_expansion();
    }
};

#include <iostream>

int main() {
    // Test matrix:
    // [2 4 2]
    // [3 2 1]
    // [2 0 1]
    vector<vector<float>> testMatrix = {
        {2, 4, 2},
        {3, 2, 1},
        {2, 0, 1}
    };
    
    LaplacesExpansion laplace(testMatrix);
    float determinant = laplace.getDeterminant();
    
    cout << "Matrix:" << endl;
    for(int i = 0; i < testMatrix.size(); i++) {
        cout << "[";
        for(int j = 0; j < testMatrix[i].size(); j++) {
            cout << testMatrix[i][j];
            if(j < testMatrix[i].size() - 1) cout << " ";
        }
        cout << "]" << endl;
    }
    
    cout << "\nDeterminant using Laplace's Expansion: " << determinant << endl;
    
    return 0;
}