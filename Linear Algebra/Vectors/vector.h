#ifndef VECTOR_H
#define VECTOR_H

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
    
    Vector(list<float> lst);
    float length();
    list<float> getUnitVector();
};

// Function declarations
pair<float,float> DotProduct(Vector * a, Vector * b);
Vector CrossProduct(Vector * a, Vector * b);
void WriteToJsonVector(map<string, list<float>> vec_data, string filename, bool print_json = true);

#endif