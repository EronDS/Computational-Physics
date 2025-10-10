
#define _USE_MATH_DEFINES
#include <vector>
#include <string>
#include <map>
#include <cmath>
#include <fstream>
#include <iostream>
#include <iomanip>
using namespace std;

class ProjectileMotion{
    public:
    map<string, vector<float>> position;
    map<string, vector<float>> velocity;
    map<string, vector<float>> acceleration;
    vector<float> time;

    float t;
    float delta_t;

    float apogee_time;

    float h_max;

    float mass;

    float energy_initial;
    float energy_final;
    float angle_of_collapse;

    ProjectileMotion(float s_ox, float s_oy, float v, 
        float v_angle, float a_ox = 0, float a_oy = -9.81,
        float mass = 1.0, int data_points_per_sec = 100){


        float v_ox = v*cos(v_angle);
        float v_oy = v*sin(v_angle);

        position["x"] = vector<float>();
        position["y"] = vector<float>();
        
        velocity["x"] = vector<float>();
        velocity["y"] = vector<float>();
        
        acceleration["x"] = vector<float>();
        acceleration["y"] = vector<float>();
        
        position["x"].push_back(s_ox);
        position["y"].push_back(s_oy);
        
        velocity["x"].push_back(v_ox);
        velocity["y"].push_back(v_oy);
        
        acceleration["x"].push_back(a_ox);
        acceleration["y"].push_back(a_oy);
        
        time.push_back(0.0);
        
        this->mass = mass;

        this->t = find_t();
        this->delta_t = this->t / data_points_per_sec;
        this->sample();

        this->energy_initial = this->get_energy_at_beggining();
        this->energy_final = this->get_energy_at_collapse();
        this->angle_of_collapse = this->get_angle_of_collapse();
        this->h_max = this->calc_h_max();
    }

    void save_to_json(const string& filename) {
        ofstream file(filename);
        if (!file.is_open()) {
            cerr << "Error: Could not open file " << filename << endl;
            return;
        }

        file << fixed << setprecision(6);
        file << "{\n";
        file << "  \"metadata\": {\n";
        file << "    \"total_time\": " << t << ",\n";
        file << "    \"delta_t\": " << delta_t << ",\n";
        file << "    \"apogee_time\": " << apogee_time << ",\n";
        file << "    \"h_max\": " << h_max << ",\n";
        file << "    \"mass\": " << mass << ",\n";
        file << "    \"energy_initial\": " << energy_initial << ",\n";
        file << "    \"energy_final\": " << energy_final << ",\n";
        file << "    \"angle_of_collapse\": " << angle_of_collapse << "\n";
        file << "  },\n";
        
        file << "  \"time_series\": {\n";
        file << "    \"time\": [";
        for (size_t i = 0; i < time.size(); ++i) {
            file << time[i];
            if (i < time.size() - 1) file << ", ";
        }
        file << "],\n";
        
        file << "    \"position_x\": [";
        for (size_t i = 0; i < position["x"].size(); ++i) {
            file << position["x"][i];
            if (i < position["x"].size() - 1) file << ", ";
        }
        file << "],\n";
        
        file << "    \"position_y\": [";
        for (size_t i = 0; i < position["y"].size(); ++i) {
            file << position["y"][i];
            if (i < position["y"].size() - 1) file << ", ";
        }
        file << "],\n";
        
        file << "    \"velocity_x\": [";
        for (size_t i = 0; i < velocity["x"].size(); ++i) {
            file << velocity["x"][i];
            if (i < velocity["x"].size() - 1) file << ", ";
        }
        file << "],\n";
        
        file << "    \"velocity_y\": [";
        for (size_t i = 0; i < velocity["y"].size(); ++i) {
            file << velocity["y"][i];
            if (i < velocity["y"].size() - 1) file << ", ";
        }
        file << "]\n";
        
        file << "  }\n";
        file << "}\n";
        
        file.close();
        cout << "Data saved to " << filename << endl;
    }

    private:
    float find_t(){
        // apogee time = d/dt[sy] = 0; (Maxima);
        // apogee time = -Voy / ay 
        float apogee_time = -this->velocity["y"][0] / acceleration["y"][0];
        this->apogee_time = apogee_time;
        return (2 * apogee_time);
    }

    float calc_h_max(){
        // h_max = Sy(apogee_time);

        return(position["y"][0] + velocity["y"][0] * \
            this->apogee_time + ((acceleration["y"][0] * pow(this->apogee_time, 2))/2));
    }

    float get_energy_at_beggining(){
        // Total kinetic energy = (1/2) * m * (vx^2 + vy^2)
        float v_squared = pow(this->velocity["x"][0], 2) + pow(this->velocity["y"][0], 2);
        return (this->mass * v_squared) / 2;
    }

    float get_energy_at_collapse(){
        // Total energy at collapse = Kinetic Energy + Potential Energy
        // KE = (1/2) * m * (vx^2 + vy^2), PE = m * g * h
        float vx_final = this->velocity["x"].back();
        float vy_final = this->velocity["y"].back();
        float kinetic_energy = (this->mass * (pow(vx_final, 2) + pow(vy_final, 2))) / 2;
        float potential_energy = this->mass * (-acceleration["y"][0]) * position["y"].back();
        return kinetic_energy + potential_energy;
    }

    float get_angle_of_collapse() {
        float vx = velocity["x"].back();
        float vy = velocity["y"].back();
        
        // Angle of collapse (in relation with Horizontal angle);

        float angle_radians = atan2(vy, vx);
        float angle_degrees = angle_radians * 180.0 / M_PI;
        
        return angle_degrees;
    }

    float get_velocity(float t, string axis){
        // v = v_o + at
        return(this->velocity[axis][0] + this->acceleration[axis].back() * t);
    }

    float get_position(float t, string axis){
        // s = s_o + v_o t + at^2/
        return(this->position[axis][0] + velocity[axis][0]*t \
            + (this->acceleration[axis].back() * pow(t, 2))/2);
    }

    void sample(){
        // Sample positions and velocities over time
        for(float current_time = this->delta_t; current_time <= this->t; current_time += this->delta_t){
            time.push_back(current_time);
            position["x"].push_back(get_position(current_time, "x"));
            position["y"].push_back(get_position(current_time, "y"));
            velocity["x"].push_back(get_velocity(current_time, "x"));
            velocity["y"].push_back(get_velocity(current_time, "y"));
        }
    }

};

int main() {
    // Example usage: Create a projectile motion simulation
    // Parameters: initial_x, initial_y, velocity, angle (in radians), accel_x, accel_y, mass, data_points_per_sec
    
    float initial_x = 0.0;      // Starting x position (m)
    float initial_y = 0.0;      // Starting y position (m)
    float velocity = 50.0;      // Initial velocity magnitude (m/s)
    float angle = M_PI / 4;     // Launch angle in radians (45 degrees)
    float accel_x = 0.0;        // Horizontal acceleration (m/s²)
    float accel_y = -9.81;      // Vertical acceleration - gravity (m/s²)
    float mass = 1.0;           // Mass of projectile (kg)
    int data_points = 100;      // Data points per second
    
    // Create projectile motion object
    ProjectileMotion projectile(initial_x, initial_y, velocity, angle, 
                              accel_x, accel_y, mass, data_points);
    
    // Save data to JSON file
    projectile.save_to_json("projectile_motion_data.json");
    
    // Print some key results
    cout << "\n=== Projectile Motion Results ===" << endl;
    cout << "Total flight time: " << projectile.t << " seconds" << endl;
    cout << "Maximum height: " << projectile.h_max << " meters" << endl;
    cout << "Apogee time: " << projectile.apogee_time << " seconds" << endl;
    cout << "Initial energy: " << projectile.energy_initial << " J" << endl;
    cout << "Final energy: " << projectile.energy_final << " J" << endl;
    cout << "Angle of collapse: " << projectile.angle_of_collapse << " degrees" << endl;
    
    return 0;
}
