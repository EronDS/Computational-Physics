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

float CrossProduct(Vector * a, Vector * b){

}


void WriteToJsonVector(map<string, list<float>> vec_data, string filename){
    ofstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return;
    }
    
    file << "{\n";
    
    bool first = true;
    for (const auto& pair : vec_data) {
        if (!first) {
            file << ",\n";
        }
        first = false;
        
        file << "  \"" << pair.first << "\": [";
        
        bool first_element = true;
        for (const auto& value : pair.second) {
            if (!first_element) {
                file << ", ";
            }
            first_element = false;
            file << fixed << setprecision(6) << value;
        }
        
        file << "]";
    }
    
    file << "\n}\n";
    file.close();
    
    cout << "Vector data written to " << filename << endl;
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


    map<string, list<float>> vec_data;
    vec_data["Vector A"] = lst;
    vec_data["Vector B"] = lst2;
    vec_data["Vector A Length"] = list<float>{a.length()};
    vec_data["Vector B Length"] = list<float>{b.length()};
    vec_data["Dot Product"] = list<float>{result.first};
    vec_data["Angle (radians)"] = list<float>{result.second};

    WriteToJsonVector(vec_data, "vector_data.json");

    return 0;
}  