#include <vector>
#include <map>
#include <cmath>
#include <stdexcept>

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

        if(I != J) {
            throw invalid_argument("Matrix must be square.");
        }

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
            return le.getDeterminant();
        }
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
    
    // Higher dimension test (8x8 matrix)
    vector<vector<float>> matrix8x8= {
        {1, 2, 3, 4, 5, 6, 7, 8},
        {9, 10, 11, 12, 13, 14, 15, 16},
        {17, 18, 19, 20, 21, 22, 23, 24},
        {25, 26, 27, 28, 29, 30, 31, 32},
        {33, 34, 35, 36, 37, 38, 39, 40},
        {41, 42, 43, 44, 45, 46, 47, 48},
        {49, 50, 51, 52, 53, 54, 55, 56},
        {57, 58, 59, 60, 61, 62, 63, 64}
    };
    cout << "\nMatrix 8x8:" << endl;
    for(int i = 0; i < matrix8x8.size(); i++) {
        cout << "[";
        for(int j = 0; j < matrix8x8[i].size(); j++) {
            cout << matrix8x8[i][j];
            if(j < matrix8x8[i].size() - 1) cout << " ";
        }
        cout << "]" << endl;
    }

    LaplacesExpansion laplace_1(matrix8x8);
    float determinant_1 =  laplace_1.getDeterminant();

    cout << "\nDeterminant using Laplace's Expansion (8x8 matrix): " << determinant_1 << endl;


    vector<vector<float>> matrix5x5_nonzero = {
    {1.0f, 0.0f, 0.0f, 0.0f, 0.0f},
    {0.0f, 1.0f, 0.0f, 0.0f, 0.0f},
    {0.0f, 0.0f, 1.0f, 0.0f, 0.0f},
    {0.0f, 0.0f, 0.0f, 1.0f, 0.0f},
    {0.0f, 0.0f, 0.0f, 0.0f, 1.0f}
};
    LaplacesExpansion laplace_2(matrix5x5_nonzero);
    float determinant_2 =  laplace_2.getDeterminant();

    cout << "\nMatrix 5x5 Determinant (Identity Matrix):" << endl;
    for(int i = 0; i < matrix5x5_nonzero.size(); i++) {
        cout << "[";
        for(int j = 0; j < matrix5x5_nonzero[i].size(); j++) {
            cout << matrix5x5_nonzero[i][j];
            if(j < matrix5x5_nonzero[i].size() - 1) cout << " ";
        }
        cout << "]" << endl;
    }


    cout << "\nDeterminant using Laplace's Expansion (5x5 matrix): " << determinant_2 << endl;


    vector<vector<float>> matrix5x5_negative = {
    {-1.0f, 0.0f, 0.0f, 0.0f, 0.0f},
    {0.0f, -1.0f, 0.0f, 0.0f, 0.0f},
    {0.0f, 0.0f, -1.0f, 0.0f, 0.0f},
    {0.0f, 0.0f, 0.0f, -1.0f, 0.0f},
    {0.0f, 0.0f, 0.0f, 0.0f, -1.0f}
};
    LaplacesExpansion laplace_3(matrix5x5_negative);
    float determinant_3 =  laplace_3.getDeterminant();
    for(int i = 0; i < matrix5x5_negative.size(); i++) {
        cout << "[";
        for(int j = 0; j < matrix5x5_negative[i].size(); j++) {
            cout << matrix5x5_negative[i][j];
            if(j < matrix5x5_negative[i].size() - 1) cout << " ";
        }
        cout << "]" << endl;
    }
    cout << "\nDeterminant using Laplace's Expansion (5x5 Reflection Matrix): " << determinant_3 << endl;
    return 0;
}