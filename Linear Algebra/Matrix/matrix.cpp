#include "../Vectors/vector.h"
#include <vector>
#include <iostream>

using namespace std;

class Matrix{
    public:
    int n_rows, n_cols;
    vector<vector<float>> mat;

    Matrix(const vector<vector<float>>& matrix){
        mat = matrix;
        n_rows = mat.size();
        n_cols = (n_rows > 0) ? mat[0].size() : 1;
    }

    vector<float> applyTransform(const vector<float>& vec) const {
        if(vec.size() != n_cols){
            throw invalid_argument("Vector size (num_row) must match number of matrix columns.");
        }
        vector<float> result(n_rows, 0.0f);

        for(int j = 0; j < n_cols; j++){
            for(int i = 0; i < n_rows; i++){
                vector<float> matrix_vector = {mat[i][j], vec[j]};
                result[i] += matrix_vector[0] * matrix_vector[1];
            }
        }
        return result;
    }
};

int main(){
    vector<vector<float>> matrix = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    Matrix mat(matrix);
    vector<float> vec = {1, 0, 1};
    vector<float> transformed_vec = mat.applyTransform(vec);
    cout << "Transformed Vector: ";
    for(float val : transformed_vec){
        cout << val << " ";
    }
    cout << endl;

    // For dot product: we need a 1x3 matrix (row vector) multiplied by 3x1 vector (column)
    // This gives us: [1, 2, 3] * [4; 5; 6] = 1*4 + 2*5 + 3*6 = 32
    vector<vector<float>> vec_a_row = {{1, 2, 3}};  // 1x3 matrix (row vector)
    vector<float> vec_b = {4, 5, 6};                // 3x1 vector (column vector)

    Matrix vec_a_matrix(vec_a_row);
    vector<float> dot_product_result = vec_a_matrix.applyTransform(vec_b);

    cout << "Dot Product Result: ";
    for(float val : dot_product_result){
        cout << val << " ";
    }
    cout << endl;

    return 0;

}