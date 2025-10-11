#include <cmath>
#include <vector>
#include <map>
#include <string>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <filesystem>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

using namespace std;


class ProjectileSpringBlock{
    public:
    float m1, v1, m2, v2, k;

    map<string, float>system_info;

    int num_cycles, samples_per_cycle;
    float delta_t;

    map<string, vector<float>> oscilation_info;

    ProjectileSpringBlock(float m1, float v1,
        float m2, float v2,
        float k, int num_cycles, int samples_per_cycle){

        // body 1 parameters
        this->m1 = m1;
        this->v1 = v1;
        // body 2 parameters (block-spring system)
        this->m2 = m2;
        this->v2 = v2;
        this->k = k;

        // calcuating collision system info;

        this->Collision();
        
        // harmonic oscillator (post collision) info;
        
        this->num_cycles = num_cycles;
        this->samples_per_cycle = samples_per_cycle;
        
        // Calculate period and time step
        float period = 2.0 * M_PI / system_info["w"];  // T = 2π/ω
        float frequency = 1.0 / period;  // f = 1/T
        
        // Store period and frequency in system_info
        system_info["period"] = period;
        system_info["frequency"] = frequency;
        
        this->delta_t = period / (float)samples_per_cycle;

        this->Oscillate();


    }

    
    void saveJson(string path = "./json_data/collision_in_mass_spring.json"){
        // Create directory if it doesn't exist
        filesystem::path filePath(path);
        filesystem::create_directories(filePath.parent_path());
        
        ofstream jsonFile(path);
        
        if (!jsonFile.is_open()) {
            cout << "Error: Could not open file " << path << " for writing." << endl;
            return;
        }

        jsonFile << fixed << setprecision(6);
        jsonFile << "{\n";
        
        // Save system_info
        jsonFile << "  \"system_info\": {\n";
        bool first = true;
        for (const auto& pair : system_info) {
            if (!first) jsonFile << ",\n";
            jsonFile << "    \"" << pair.first << "\": " << pair.second;
            first = false;
        }
        jsonFile << "\n  },\n";
        
        // Save oscillation_info (time series data)
        jsonFile << "  \"oscillation_info\": {\n";
        first = true;
        for (const auto& pair : oscilation_info) {
            if (!first) jsonFile << ",\n";
            jsonFile << "    \"" << pair.first << "\": [";
            
            // Write array values
            for (size_t i = 0; i < pair.second.size(); i++) {
                if (i > 0) jsonFile << ", ";
                jsonFile << pair.second[i];
            }
            jsonFile << "]";
            first = false;
        }
        jsonFile << "\n  }\n";
        
        jsonFile << "}\n";
        jsonFile.close();
        
        cout << "Data saved to " << path << endl;
    }

    private:
    
    void Collision(){
        // vf = \frac{m1v1 + m2v2}{m1+m2}
        // E_k = \frac{(m1+m2)vf^2}{2}
        // A = \sqrt{2E_k/k}

        float velocity_block_projectile_at_collision = (m1*v1 + m2*v2) / (m1+m2);
        float kinectic_energy = ((m1+m2) * pow(velocity_block_projectile_at_collision,2)) / 2;
        float amplitude = sqrt(2*kinectic_energy/k);
        float w = sqrt(k/(m1+m2));

        system_info["system_velocity_at_collision"] = velocity_block_projectile_at_collision;
        system_info["kinectic_energy"] = kinectic_energy;
        system_info["Amplitude"] = amplitude;
        system_info["w"] = w;
        system_info["mass"] = (m1+m2);
        system_info["k"] = k;
        return;
    }

    void Oscillate(){

        // x = Acos(wt);
        // v = d/dt[x] = -wAsin(wt);
        // a = d/dt[v] = -w^2Acos(wt);

        // Initialize vectors in oscillation_info map
        oscilation_info["time"] = vector<float>();
        oscilation_info["position"] = vector<float>();
        oscilation_info["velocity"] = vector<float>();
        oscilation_info["acceleration"] = vector<float>();
        oscilation_info["kinetic_energy"] = vector<float>();
        oscilation_info["potential_energy"] = vector<float>();
        oscilation_info["total_energy"] = vector<float>();

        float current_time = 0.0;
        int total_samples = this->num_cycles * this->samples_per_cycle;
        
        // Calculate total simulation time for the specified number of cycles
        float total_time = this->num_cycles * system_info["period"];

        for(int sample = 0; sample < total_samples; sample++){

            float x = system_info["Amplitude"] * cos(system_info["w"] * current_time);
            float v = -system_info["w"] * system_info["Amplitude"] * sin(system_info["w"] * current_time);
            float a = -pow(system_info["w"], 2) * system_info["Amplitude"] * cos(system_info["w"] * current_time);

            float kinetic_energy = (system_info["mass"] * pow(v, 2)) / 2;
            float potential_energy = (system_info["k"] * pow(x, 2)) / 2;
            float total_energy = kinetic_energy + potential_energy;

            // Store data in oscillation_info map
            oscilation_info["time"].push_back(current_time);
            oscilation_info["position"].push_back(x);
            oscilation_info["velocity"].push_back(v);
            oscilation_info["acceleration"].push_back(a);
            oscilation_info["kinetic_energy"].push_back(kinetic_energy);
            oscilation_info["potential_energy"].push_back(potential_energy);
            oscilation_info["total_energy"].push_back(total_energy);

            current_time += this->delta_t;
        }
        
        // Store total time in system_info for reference
        system_info["total_time"] = total_time;
    }
};

// Test function to verify the implementation
int main() {
    // Test parameters
    float m1 = 2.0;  // mass of projectile (kg)
    float v1 = 10.0; // initial velocity of projectile (m/s)
    float m2 = 1.0;  // mass of block (kg)
    float v2 = 0.0;  // initial velocity of block (m/s)
    float k = 50.0;  // spring constant (N/m)
    int num_cycles = 5;        // number of complete oscillation cycles
    int samples_per_cycle = 20; // samples per complete cycle

    ProjectileSpringBlock system(m1, v1, m2, v2, k, num_cycles, samples_per_cycle);
    
    cout << "System Information:" << endl;
    cout << "Collision velocity: " << system.system_info["system_velocity_at_collision"] << " m/s" << endl;
    cout << "Amplitude: " << system.system_info["Amplitude"] << " m" << endl;
    cout << "Angular frequency: " << system.system_info["w"] << " rad/s" << endl;
    cout << "Frequency: " << system.system_info["frequency"] << " Hz" << endl;
    cout << "Period: " << system.system_info["period"] << " s" << endl;
    cout << "Total mass: " << system.system_info["mass"] << " kg" << endl;
    cout << "Number of cycles: " << num_cycles << endl;
    cout << "Samples per cycle: " << samples_per_cycle << endl;
    cout << "Total simulation time: " << system.system_info["total_time"] << " s" << endl;
    
    cout << "\nOscillation data points collected: " << system.oscilation_info["time"].size() << endl;
    
    // Display first few data points
    cout << "\nFirst 10 data points:" << endl;
    cout << "Time\tPosition\tVelocity\tAcceleration\tKE\tPE\tTotal Energy" << endl;
    for(int i = 0; i < min(10, (int)system.oscilation_info["time"].size()); i++) {
        cout << system.oscilation_info["time"][i] << "\t" 
             << system.oscilation_info["position"][i] << "\t"
             << system.oscilation_info["velocity"][i] << "\t"
             << system.oscilation_info["acceleration"][i] << "\t"
             << system.oscilation_info["kinetic_energy"][i] << "\t"
             << system.oscilation_info["potential_energy"][i] << "\t"
             << system.oscilation_info["total_energy"][i] << endl;
    }
    
    // Save data to JSON file
    system.saveJson();
    
    return 0;
}