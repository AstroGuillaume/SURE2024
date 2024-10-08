This chamber controls the temperature and humidity for our droplet analysis

In order to use the chamber, first make sure to plug in the following items:
  1) Power Supply, turn it ON, and set it to 11.95V
  2) Plug for the fans
  3) Power supply for the coolant fan

The arduino code should already be uploaded on the temperature & humidity controlled chamber, but if there is any problem, the code can be found in the ChamberControl folder (chamber_operation_arduino.ino).

When utilizing the chamber, connect the USB cable to your computer and run the python file included in this folder. The following should be done in order:

  1) Changer the values of the curr_dir and folder_name variables to locations that match where you would like the temperature and humidity data to be stored on your computer. For example, on my computer, I set it to the following:

  curr_dir = "C:\\Users\\guill\\OneDrive\\Documents\\02-TRAVAIL\\03 - EMPLOIS\\SURE 2024\\chamber_operation_arduino"           folder_name = "\\TestData"  # sub-folder to store temp + graphs
  
  2) The program will ask you whether you would like the temperature to be turned ON or OFF. Enter either ON or OFF using your keyboard. If OFF is chosen, the temperature will be disregarded. If not, it will prompt you to enter the temperature using the keyboard. Press the return key when you are done.
  3) The program will then ask you whether you would like the humidity to be turned ON or OFF. Enter either ON or OFF using your keyboard. If OFF is chosen, the humidity will be disregarded. If not, it will prompt you to enter the humidity using the keyboard. Press the return key when you are done.
  4) Then, the available serial ports will be listed, and the one with the arduino connected to it will be indicated. Enter the number of the port you would like to use with the keyboard and press the return key.
  5) The initial configurations of the box will be done (it should take about 30 seconds to execute, be patient). Once this is done, the command line will indicate "next...". At this stage, you will have the option to enter multiple commands, choose the one that you would like to execute and press the return key on the keyboard:

      1. "T" : Returns the current temperature in the chamber
      2. "H" : Returns the current humidity in the chamber
      3. "C" : Collects the temperature and/or humidity for the desired amount of seconds. Once you press this command, you                 will be prompted to enter the collection time (in seconds), press the return key once you are done.

The program will save the curves of the temperature and/or humidity on your computer at the folder destination that you entered in step 1. The curves are taken from the moment you set the temperature and humidity variables to 20 seconds after the desired humidity and/or temperature have been reached. The curves will be saved along with a text file containing the exact values used in the graph. These information will be saved in a sub-folder with the current date and time.

A control loop ensures that when the temperature or humidity values are reached, the chamber keeps those values constant.
