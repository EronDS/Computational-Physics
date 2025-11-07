#include <vector>
#include <iostream>
#include <map>
#include <cmath>
#include <iomanip>
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


class InverseMatrix {
    public:
    vector<vector<float>> A;
    float A_determinant;
    InverseMatrix(const vector<vector<float>>& matrix){
        A = matrix;
        LaplacesExpansion le(A);
        A_determinant = le.getDeterminant();
        if(A_determinant == 0) {
            throw invalid_argument("Matrix cannot inverted. Det(A)");
        }
    }

    vector<vector<float>> getInverseMatrix(){
        vector<vector<float>> inverse(A.size(), vector<float>(A[0].size(), 0.0f));
        
        // Calculate cofactor matrix
        vector<vector<float>> cofactor(A.size(), vector<float>(A[0].size(), 0.0f));
        for(int i = 0; i < A.size(); i++){
            for(int j = 0; j < A[0].size(); j++){
                float sign = pow(-1, i + j);
                float minor_det = LaplacesExpansion(get_minor(i, j)).getDeterminant();
                cofactor[i][j] = sign * minor_det;
            }
        }
        
        // Transpose the cofactor matrix to get adjugate matrix
        // Then divide by determinant to get inverse: A^(-1) = adj(A) / det(A)
        for(int i = 0; i < A.size(); i++){
            for(int j = 0; j < A[0].size(); j++){
                inverse[i][j] = cofactor[j][i] / A_determinant; // Note: j,i for transpose
            }
        }
        
        return inverse;
    }

    vector<vector<float>> multiply(const vector<vector<float>>& B){
        if(A[0].size() != B.size()){
            throw invalid_argument("Incompatible matrix sizes for multiplication.");
        }
        vector<vector<float>> result(A.size(), vector<float>(B[0].size(), 0.0f));
        for(int i = 0; i < A.size(); i++){
            for(int j = 0; j < B[0].size(); j++){
                for(int k = 0; k < A[0].size(); k++){
                    result[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        cout << "Result of multiplication:" << endl;
        for (const auto& row : result) {
            for (float val : row) {
                cout << fixed << setprecision(2) << val << " ";
            }
            cout << endl;
        }
        return result;
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
};



int main(){
    vector<vector<float>> matrix5x5_nonzero_det = {
    {1.0f, 0.0f, 0.0f, 0.0f, 0.0f},
    {0.0f, 1.0f, 0.0f, 0.0f, 0.0f},
    {0.0f, 0.0f, 1.0f, 0.0f, 0.0f},
    {0.0f, 0.0f, 0.0f, 1.0f, 0.0f},
    {0.0f, 0.0f, 0.0f, 0.0f, 1.0f}
};

    InverseMatrix im(matrix5x5_nonzero_det);

    cout << "Original Matrix A:" << endl;
    for (const auto& row : im.A) {
        for (float val : row) {
            cout << fixed << setprecision(2) << val << " ";
        }
        cout << endl;
    }
    cout << endl;

    vector<vector<float>> inverse = im.getInverseMatrix();
    cout << "Inverse Matrix A^(-1):" << endl;
    for (const auto& row : inverse) {
        for (float val : row) {
            cout << fixed << setprecision(2) << val << " ";
        }
        cout << endl;
    }
    cout << endl;

    cout << "Verification: A * A^(-1) should equal Identity Matrix I:" << endl;
    im.multiply(inverse);

    return 0;

}


