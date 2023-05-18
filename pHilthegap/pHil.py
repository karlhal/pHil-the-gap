'''
@file demo_PH_read.py
Modified version of the original demo_PH_read.py from DFRobot
@author Karl Hallström (karlhal@chalmers.se)
@version  Your Version
@date  Your Date
@copyright Copyright (c) 2023 pHil The Gap - Chalmers tekniska högskola (philthegap2023.com)
@license Creative Commons Attribution 4.0 International (CC BY 4.0)
This software is released under the Creative Commons Attribution 4.0 International license. 
You are free to copy, redistribute and adapt the material for any purpose, even commercially, under the following terms:
Attribution — You must give appropriate credit to the original author (DFRobot), provide a link to the license, 
and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests 
the licensor endorses you or your use. For more details visit:
https://creativecommons.org/licenses/by/4.0/

The original code from which this code is derived is under The MIT License (MIT) 
@author [Jiawei Zhang](jiawei.zhang@dfrobot.com)
@copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
'''



import sys
import time
from datetime import datetime

ADS1115_REG_CONFIG_PGA_6_144V = 0x00  # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V = 0x02  # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V = 0x04  # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V = 0x06  # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V = 0x08  # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V = 0x0A  # 0.256V range = Gain 16

from pHil_ADS1115 import ADS1115
from pHil_PH import pHil_PH

ads1115 = ADS1115()
ph = pHil_PH()

ph.begin()

# Read your temperature sensor to execute temperature compensation

calibration_data = {}
import json

def calibration():
    calibration_data = {}
    for pH in [7, 4]:
        input(f"Please put the pH sensor into the {pH} pH buffer solution and keep it there for one minute, then type 'yes': ")
        print("Measuring...")
        readings = []
        for _ in range(10):
            ads1115.setAddr_ADS1115(0x48)
            ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
            adc0 = ads1115.readVoltage(0)
            PH = ph.read_PH(adc0['r'], buffer_temperature)
            readings.append(PH)
            time.sleep(1)
        average_PH = sum(readings) / len(readings)
        calibration_data[pH] = average_PH
    with open('calibration_data.json', 'w') as file:
        json.dump(calibration_data, file)
    print("Calibration is now done! Type 'yes' to start a measurement or 'stop' to end the program.")
    response = input().lower()
    if response == 'yes':
        measurement()
    elif response == 'stop':
        print("Program ended.")
    else:
        print("Invalid input. Program ended.")

def measurement():
    with open('calibration_data.json', 'r') as file:
        calibration_data = json.load(file)

    def linear_func(x):
        x1, y1 = 7, calibration_data[str(7)]
        x2, y2 = 4, calibration_data[str(4)]
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        return m * x + b

    while True:
        ads1115.setAddr_ADS1115(0x48)
        ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
        adc0 = ads1115.readVoltage(0)
        PH = ph.read_PH(adc0['r'], ocean_temperature)
        PH = linear_func(PH)
        print("PH:%.2f Time:%s" % (PH, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        with open("data_log.txt", "a") as file:
            file.write(f"PH:%.2f Coordinates: {dive_coordinates} Time:%s\n" % (PH, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        time.sleep(1.0)

def main():
    global dive_coordinates  # Declare it as global here before you assign any value to it.
    print("Hi, welcome to pHil the gap sensor instrument!")
    dive_coordinates = input("Before starting, please enter the coordinates of the dive: ")

    temp_buffer = input("We will need the temperature of the buffer solutions (in C) (or q to quit the program): ")
    if temp_buffer.lower() == 'q':
        print("Program ended.")
        return
    else:
        try:
            temp_buffer = float(temp_buffer)  # Convert the input to a float
        except ValueError:
            print("Invalid temperature entered. Please enter a numeric value.")
            return

    temp_ocean = input("Now type the temperature of the ocean (in C): ")
    try:
        temp_ocean = float(temp_ocean)  # Convert the input to a float
    except ValueError:
        print("Invalid temperature entered. Please enter a numeric value.")
        return

    # Assign temperatures globally
    global buffer_temperature
    global ocean_temperature
    buffer_temperature = temp_buffer
    ocean_temperature = temp_ocean

    while True:  # Keep asking for user input until a valid input is given
        user_input = input("Great! Enter 'c' for calibration, 'm' for measurement, or 'q' to quit: ")
        if user_input.lower() == 'c':
            calibration()
        elif user_input.lower() == 'm':
            measurement()
        elif user_input.lower() == 'q':
            print("Program ended.")
            break  # Exit the loop, effectively ending the program
        else:
            print("Invalid input, please enter either 'c' or 'm'.")

# Make sure to call the main function when the script is run directly
if __name__ == "__main__":
    main()

