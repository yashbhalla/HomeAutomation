#include <iostream>
#include <string>
#include <algorithm>

float temp_val, right_val, humidity_val, light_start, temp_start, humidifier_start, current_api_flow, thresh_temp, thresh_light, thresh_humidifier;

float read_temp();
bool read_light();
float read_humidity();

void operate_light(bool state);
void operate_fan(bool state);
void operate_humidifier(bool state);

void set_temp_thresh(float value);
void set_light_thresh(bool state);
void set_humidifier_thresh(float value);
//void set_api_flow();

float read_temp()
{
    //temp_val = ;
    return temp_val;
}

bool read_light()
{
    // light_start = ;
    return light_start > thresh_light;
}

float read_humidity()
{
    // humidity_val = ;
    return humidity_val;
}

void operate_light(bool state)
{
    if (state)
        std::cout << "Light turned ON" << std::endl;
    else
        std::cout << "Light turned OFF" << std::endl;
}

void operate_fan(bool state)
{
    if (state)
        std::cout << "Fan turned ON" << std::endl;
    else
        std::cout << "Fan turned OFF" << std::endl;
}

void operate_humidifier(bool state)
{
    if (state)
        std::cout << "Humidifier turned ON" << std::endl;
    else
        std::cout << "Humidifier turned OFF" << std::endl;
}

void set_temp_thresh(float value)
{
    if (value >= -10 && value <= 120)
    {
        thresh_temp = value;
        std::cout << "Temperature threshold set to: " << thresh_temp << std::endl;
    }
    else {
        std::cout << "Invalid temperature value. Please enter a value between -10 and 120 Celsius." << std::endl;
    }
}

void set_light_thresh(bool state)
{
    thresh_light = state ? 1 : 0;
    std::cout << "Light threshold set to: " << (state ? "ON" : "OFF") << std::endl;
}

void set_humidifier_thresh(float value)
{
    if (value >= 0 && value <= 100)
    {
        thresh_humidifier = value;
        std::cout << "Humidifier threshold set to: " << thresh_humidifier << "%" << std::endl;
    }
    else {
        std::cout << "Invalid humidifier value. Please enter a value between 0 and 100." << std::endl;
    }
}

int main()
{
    std::string userInput;
    while (true)
    {
        std::cout << "Enter a command: ";
        std::getline(std::cin, userInput);

        std::transform(userInput.begin(), userInput.end(), userInput.begin(), ::tolower);

        if (userInput == "read temp")
        {
            float temp = read_temp();
            std::cout << "Current Temperature: " << temp << "°C" << std::endl;
        }
        else if (userInput == "read light")
        {
            bool light = read_light();
            std::cout << "Light is " << (light ? "ON" : "OFF") << std::endl;
        }
        else if (userInput == "read humidifier")
        {
            float humidity = read_humidity();
            std::cout << "Current Humidity: " << humidity << "%" << std::endl;
        }
        else if (userInput.find("set temp to ") != std::string::npos)
        {
            float value = std::stof(userInput.substr(11));
            set_temp_thresh(value);
        }
        else if (userInput.find("set light to ") != std::string::npos)
        {
            std::string stateStr = userInput.substr(13);
            bool state = (stateStr == "on");
            set_light_thresh(state);
        }
        else if (userInput.find("set humidifier to ") != std::string::npos)
        {
            float value = std::stof(userInput.substr(18));
            set_humidifier_thresh(value);
        }
        else if (userInput == "quit")
        {
            break;
        }
        else
        {
            std::cout << "Invalid command. Please try again." << std::endl;
        }
    }

    return 0;
}
