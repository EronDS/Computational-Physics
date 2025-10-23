#include <vector>
#include <list>
#include <iostream>
#include <cmath>
#include <utility>
#include <iomanip>
#include <map>
#include <fstream>
#include <string>

using namespace std;


class Vector{
    public:
    vector<float> vec;
    list<float> unit_vector;
    int size;
    Vector(list<float> lst){
        vec = vector<float>(lst.begin(), lst.end());
        size = vec.size();
    }

    float length(){
        float sum = 0;
        for(int num : vec){
            sum += pow(num, 2);
        }
        return sqrt(sum);
    }

    list<float> getUnitVector(){
        float len = length();
        list<float> unit_vec;
        for(float component : vec){
            unit_vec.push_back(component / len);
        }
        return unit_vec;
    }
    
};


pair<float,float> DotProduct(Vector *  a, Vector *  b){
    if(a->size != b->size){
        throw invalid_argument("Vectors must be of the same length");
    }
    float dot_product = 0; 

    for(int i =0; i < a->size; i++){
        dot_product += a->vec[i] * b->vec[i];
    }

    float theta;

    // |a|*|b|*cos(theta) = a.b
    theta = acos(dot_product / (a->length() * b->length()));

    return make_pair(dot_product, theta);
}

Vector CrossProduct(Vector * a, Vector * b){
    if(a->size != 3 || b->size != 3) {
        throw invalid_argument("Cross product only defined for 3D vectors");
    }
    
    // Using Levi-Civita symbol εijk
    // Cross product: c_i = ε_ijk * a_j * b_k

    vector<float> result_vec(3);
    
    // Levi-Civita tensor components (only non-zero elements)
    // ε₁₂₃ = ε₂₃₁ = ε₃₁₂ = +1
    // ε₁₃₂ = ε₂₁₃ = ε₃₂₁ = -1
    
    // c₁ = ε₁₂₃ * a₂ * b₃ + ε₁₃₂ * a₃ * b₂ = a₂b₃ - a₃b₂
    result_vec[0] = a->vec[1] * b->vec[2] - a->vec[2] * b->vec[1];
    
    // c₂ = ε₂₃₁ * a₃ * b₁ + ε₂₁₃ * a₁ * b₃ = a₃b₁ - a₁b₃
    result_vec[1] = a->vec[2] * b->vec[0] - a->vec[0] * b->vec[2];
    
    // c₃ = ε₃₁₂ * a₁ * b₂ + ε₃₂₁ * a₂ * b₁ = a₁b₂ - a₂b₁
    result_vec[2] = a->vec[0] * b->vec[1] - a->vec[1] * b->vec[0];

    list<float> result_list(result_vec.begin(), result_vec.end());
    
    return Vector(result_list);
}


void WriteToJsonVector(map<string, list<float>> vec_data, string filename, bool print_json = true){
    ofstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return;
    }
    
    string json_content = "{\n";

    bool first = true;
    for (const auto& pair : vec_data) {
        if (!first) {
            json_content += ",\n";
        }
        first = false;
        
        json_content += "  \"" + pair.first + "\": [";
        
        bool first_element = true;
        for (const auto& value : pair.second) {
            if (!first_element) {
                json_content += ", ";
            }
            first_element = false;
            
            // Format the number properly
            ostringstream oss;
            oss << fixed << setprecision(6) << value;
            json_content += oss.str();
        }
        
        json_content += "]";
    }
    
    json_content += "\n}\n";
    
    // Write to file
    file << json_content;
    file.close();
    
    cout << "Vector data written to " << filename << endl;
    
    // Print JSON if requested
    if (print_json) {
        cout << "\nGenerated JSON:\n" << json_content << endl;
    }
}


int main() {
    list<float> lst = {1, 2, 3,};
    list<float> lst2 = {5, 4, 3,};


    Vector a(lst);
    Vector b(lst2);

    cout << "Length of vector a: " << a.length() << endl;
    cout << "Length of vector b: " << b.length() << endl;


    pair<float, float> result = DotProduct(&a, &b);
    cout << "Dot product: " << result.first << ", Angle (radians): " << result.second << endl;

    // Cross product calculation
    Vector cross_result = CrossProduct(&a, &b);
    cout << "Cross product: (" << cross_result.vec[0] << ", " << cross_result.vec[1] << ", " << cross_result.vec[2] << ")" << endl;
    cout << "Cross product magnitude: " << cross_result.length() << endl;

    map<string, list<float>> vec_data;
    vec_data["Vector A"] = lst;
    vec_data["Vector B"] = lst2;
    vec_data["Vector A Length"] = list<float>{a.length()};
    vec_data["Vector B Length"] = list<float>{b.length()};
    vec_data["Dot Product"] = list<float>{result.first};
    vec_data["Angle (radians)"] = list<float>{result.second};
    vec_data["Vector A Unit"] = a.getUnitVector();
    vec_data["Vector B Unit"] = b.getUnitVector();
    vec_data["Cross Product"] = list<float>(cross_result.vec.begin(), cross_result.vec.end());
    vec_data["Cross Product Magnitude"] = list<float>{cross_result.length()};
    vec_data["Cross Product Unit"] = cross_result.getUnitVector();

    WriteToJsonVector(vec_data, "vector_data.json");

    return 0;
}  