
# IMPORTS
import subprocess
import sys
import matplotlib.pyplot as plt
import keyboard
from datetime import datetime
import time
import re
import importlib
import os
import queue
import numpy as np


# GLOBAL VARIABLEs
curr_dir = "C:\\Users\\guill\\OneDrive\\Documents\\02-TRAVAIL\\03 - EMPLOIS\\SURE 2024\\chamber_operation_arduino"  # folder to store data
folder_name = "\\TestData"  # sub-folder to store temp + graphs

temperature_data = []   # array to plot temperature
humidity_data = []
time_data_temp = []
time_data_humi = []
recording_ON = False
continue_setup = False
go_setup = True
finished_reading = False
time_to_add = True
var = ""
duration_to_add = 20
init_time = 0
first_var_set = False # to ensure both humidity and temperature have been set

temperature_ON = input("temperature --> ON OR OFF\n")
if (temperature_ON == "ON"):
    desired_temperature = input("Enter the desired Temperature (degrees celcius) using the keyboard: ")
humidity_ON = input("humidity --> ON OR OFF\n")
if (humidity_ON == "ON"):
    desired_humidity = input("Enter the desired relative Humidity (%) using the keyboard: ")


# PROGRAM START 
# (queue for inter-thread communication)
plot_queue = queue.Queue()
serial_data = []

# Get current date and time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# make directory to store data
dir = os.path.join(curr_dir+folder_name+"\\"+current_time)

# make a subdirectory with the time 
os.makedirs(dir)
print("directory with current time created...")

# ensure packages are installed on the computer
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def try_import(package, import_name):
    try:
        importlib.import_module(import_name)
    except ImportError:
        try:
            install_package(package)
        except:
            print(f"Install the {package} package using the CLI. It failed to install here.")

try_import('serial.tools.list_ports', 'serial')
import serial.tools.list_ports
try_import('keyboard', 'keyboard')
import keyboard
try_import('pandas', 'pandas')
import pandas
try_import('openpyxl', 'openpyxl') 
import openpyxl

# gives all the communication ports on the computer
ports = serial.tools.list_ports.comports()

# tells our program we are using serial communication
ser = serial.Serial()
portsList = []

# prints all ports on the computer
for port in ports:
    portsList.append(str(port))
    print(str(port))

com = input("Select Com Port for Arduino #: ")

# check ports are indeed ports
for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print("using port: ",use)

# setup serial communication
ser.baudrate = 9600
ser.port = use
ser.timeout = 5

try:
    ser.open()
    print("Serial port opened successfully.")
    print("Please wait for the device to be initialized...")
except Exception as e:
    print(f"Failed to open serial port: {e}")
    exit()

# Callback function to handle key press events
def on_key_event(event):
    global init_time
    if event.event_type == keyboard.KEY_DOWN:

        # keyboard data
        data = input("")

        # data collection
        if data == "C":
            init_time = time.time()
            global recording_ON
            recording_ON = True
            collect_data()
            plot_data()

        # encode keyboard data
        if data:
            ser.write(data.encode('utf-8'))

# Register the callback function for key press events
keyboard.on_press(on_key_event)

# Function to collect data for a specified duration
def collect_data():

    global next_data                     # what data will be fetched next?
    global finished_reading
    global time_to_add              # time to add after desired temp or humi has been reached
    start_time = 1000000000000      # arbitrary very long time to ensure the condition doesn't initially evaluate to True
    var_counts = [0,0]              # counts the number of temperature and humidity data points

    if (temperature_ON == "ON" and humidity_ON == "ON"):
        next_data= "temp"
        same = var_counts[0] == var_counts[1]

    if (temperature_ON == "ON" and humidity_ON == "OFF"):
        next_data= "temp"
        same = True

    if (temperature_ON == "OFF" and humidity_ON == "ON"):
        next_data= "humi"
        same = True

    while ((not finished_reading) or (time.time() - start_time < duration_to_add) or (not same)):

        if finished_reading and time_to_add:
            start_time = time.time()
            time_to_add = False
        
        if finished_reading:
            print("current time: ", time.time())
            print("time elapsed: ", time.time()-start_time)
            print("duration to add: ", duration_to_add)

        if (temperature_ON == "ON" and humidity_ON == "OFF"):
            ser.write(b"T\n")  # Request temperature from Arduino
            time.sleep(0.1)
            time.sleep(1)  # Request data every second
        
        elif (temperature_ON == "OFF" and humidity_ON == "ON"):
            ser.write(b"H\n")
            time.sleep(0.1)
            time.sleep(1)  # Request data every second

        elif (temperature_ON == "ON" and humidity_ON == "ON"):
            if next_data== "humi":

                # ask for humidity
                ser.write(b"H\n")
                time.sleep(0.1)
                time.sleep(1)  
                var_counts[0] += 1
                next_data = "temp"
            
            elif next_data == "temp":

                # ask for temperature
                ser.write(b"T\n")
                time.sleep(0.1)
                time.sleep(1)  
                var_counts[1] += 1
                next_data= "humi"
            same = var_counts[0] == var_counts[1]

    if temperature_ON == "ON":
        print(temperature_data)
    if humidity_ON == "ON":
        print(humidity_data)


# Function to plot data
def plot_data():

    global temperature_data
    global humidity_data

    if temperature_ON == "ON" and humidity_ON == "OFF":

        if temperature_data:

            temperature_data = [float(temp) for temp in temperature_data]
        
            # Assuming each data point is recorded at regular intervals
            # time_axis = range(len(temperature_data))  # Create time axis
            time_axis = time_data_temp
            
            # Set the maximum number of y-axis ticks
            plt.ylim(min(temperature_data), max(temperature_data))

            # Calculate the step size based on the range of your data and the number of bins
            step = (max(temperature_data) - min(temperature_data)) / 15

            # Generate the y-ticks
            y_ticks = np.arange(min(temperature_data), max(temperature_data), step)

            # Set the y-ticks
            plt.yticks(y_ticks)

            plt.autoscale(tight=True)

            # Plot temperature data against time
            plt.plot(time_axis, temperature_data)
            plt.xlabel('Time (s)')
            plt.ylabel('Temperature (degrees)')
            plt.title('Temperature plot')

            # Set y-axis limits to ensure highest temperature is on top
            plt.autoscale(tight=True)
            plt.savefig(curr_dir+"\\"+folder_name+"\\"+current_time+"\\figure_"+current_time)
            plt.show()

        else:
            print("Temperature data is empty.")

    elif temperature_ON == "OFF" and humidity_ON == "ON":

        if humidity_data:

            humidity_data = [float(humi) for humi in humidity_data]
        
            # Assuming each data point is recorded at regular intervals
            # time_axis = range(len(humidity_data))  # Create time axis
            time_axis = time_data_humi
            
            # Set the maximum number of y-axis ticks
            plt.ylim(min(humidity_data), max(humidity_data))

            # Calculate the step size based on the range of your data and the number of bins
            step = (max(humidity_data) - min(humidity_data)) / 15

            # Generate the y-ticks
            y_ticks = np.arange(min(humidity_data), max(humidity_data), step)

            # Set the y-ticks
            plt.yticks(y_ticks)

            plt.autoscale(tight=True)

            # Plot temperature data against time
            plt.plot(time_axis, humidity_data)
            plt.xlabel('Time (s)')
            plt.ylabel('Relative humidity (%)')
            plt.title('Humiditiy Plot')

            # Set y-axis limits to ensure highest temperature is on top
            plt.autoscale(tight=True)
            plt.savefig(curr_dir+"\\"+folder_name+"\\"+current_time+"\\figure_"+current_time)
            plt.show()

        else:
            print("Humidity data is empty.")

    elif temperature_ON == "ON" and humidity_ON == "ON":

        if humidity_data and temperature_data:

            temperature_data = [float(temp) for temp in temperature_data]
            humidity_data = [float(humi) for humi in humidity_data]
        
            # Assuming each data point is recorded at regular intervals
            # time_axis = range(len(humidity_data))  # Create time axis
            
            fig, axs = plt.subplots(2)

            # Define a function to set y-axis limits, ticks and autoscale
            def set_yaxis(ax, data, num_ticks=15):
                ax.set_ylim(min(data), max(data))
                step = (max(data) - min(data)) / num_ticks
                y_ticks = np.arange(min(data), max(data), step)
                ax.set_yticks(y_ticks)
                ax.autoscale(tight=True)

            # Plot humidity data against time and set y-axis
            axs[0].plot(time_data_humi, humidity_data)
            axs[0].set(ylabel='Relative humidity (%)', title='Humidity Plot')
            set_yaxis(axs[0], humidity_data)

            # Plot temperature data against time and set y-axis
            axs[1].plot(time_data_temp, temperature_data)
            axs[1].set(xlabel='Time (s)', ylabel='Temperature (°C)', title='Temperature Plot')
            set_yaxis(axs[1], temperature_data)

            plt.tight_layout()
            plt.savefig(curr_dir+"\\"+folder_name+"\\"+current_time+"\\figure_"+current_time)
            plt.show()

        else:
            print("Humidity and temperatrue data are empty.")

def check_pattern(text):
    pattern = r"(?<!=)\d{2}\.\d{2}"   # Matches two digits, followed by a dot, followed by two digits
    if re.search(pattern, text):
        return True
    else:
        return False
    

# set desired humidity and temperature
setup = "0"
isInitialData = True


# In your main loop
while (True):

    # read serial data
    serial_data = ser.readline().decode('utf-8').strip()

    # print what is written over the serial line
    if serial_data:
        print(serial_data)

    if recording_ON:
        # check if it correspond to a humidity or temperature
        if check_pattern(serial_data):

            if (isInitialData):
                initialData = float(serial_data)
                isInitialData = False

            if (humidity_ON == "ON" and next_data == "humi"):

                if (float(desired_humidity)<float(initialData) and float(serial_data)<=float(desired_humidity)):
                    if temperature_ON == "ON":
                        first_var_set = True
                    else:
                        finished_reading = True

                if (float(desired_humidity)>float(initialData) and float(serial_data)>=float(desired_humidity)):
                    if temperature_ON == "ON":
                        first_var_set = True
                    else:
                        finished_reading = True

                humidity_data.append(serial_data)
                time_data_humi.append(time.time()-init_time)
                
                # Construct file path
                print("saving at -->",dir+f"\\humidity_data_{current_time}.txt")
                file_path = os.path.join(dir+f"\\humidity_data_{current_time}.txt")

                # Write data to file
                with open(file_path, "a") as file:
                    file.write(serial_data + " --> " + str(time.time()-init_time) + "\n")

                    
            if (temperature_ON == "ON" and next_data == "temp"):

                if (float(desired_temperature)<float(initialData) and float(serial_data)<=float(desired_temperature)):
                    if humidity_ON == "ON":
                        if first_var_set:
                            finished_reading = True
                    else:
                        finished_reading = True

                if (float(desired_temperature)>float(initialData) and float(serial_data)>=float(desired_temperature)):
                    if humidity_ON == "ON":
                        if first_var_set:
                            finished_reading = True
                    else:
                        finished_reading = True

                temperature_data.append(serial_data)
                time_data_temp.append(time.time() - init_time)
                
                # Construct file path
                print("saving at -->",dir+f"\\temperature_data_{current_time}.txt")
                file_path = os.path.join(dir+f"\\temperature_data_{current_time}.txt")
                                
                # Write data to file
                with open(file_path, "a") as file:
                    file.write(serial_data + " --> " + str(time.time()-init_time) + "\n")

    if serial_data == "Finished the initial configurations":
        continue_setup = True
    
    if (serial_data == "next..." and setup == "4"):
        print("Please enter the next command...\n")
    
    elif serial_data == "next...":
        go_setup = True


    # initial configuration
    if (continue_setup == True):
        
        # set temperature to be ON or OFF
        # print("setup",setup)
        if (setup == "0" and go_setup==True):
            setup = "1"
            go_setup = False
            print("setting temperature on or off...\n")
            ser.write("TO{0}\n".format(temperature_ON).encode('utf-8'))
            continue
        
        # set humidity to be ON or OFF
        if (setup == "1" and go_setup==True):
            setup = "2"
            go_setup = False
            print("setting humidity on or off...\n")
            ser.write("HO{0}\n".format(humidity_ON).encode('utf-8'))
            continue
        
        # set desired temperature
        if (temperature_ON == "ON" and go_setup==True and setup == "2"):
                go_setup = False
                print("setting desired temperature")
                ser.write("ST{0}\n".format(desired_temperature).encode('utf-8'))
                setup = "3"
                continue
        
        if (humidity_ON == "ON" and go_setup==True and setup == "3"):
                setup = "4"
                go_setup = False
                print("setting desired humidity")
                ser.write("SH{0}\n".format(desired_humidity).encode('utf-8'))
                go_setup = False
                continue_setup = False
                continue



