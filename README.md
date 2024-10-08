# SURE2024
Research on airborne viruses
![Chamber_picture1](https://github.com/user-attachments/assets/ce65262c-8383-4f49-92de-6ef3cce8cb1e)

#1. Setting the controlled temperature & humidity chamber:

The first step when using the controlled chamber is to plug the following elements:
  - Cooling unit
  - fans
  - DC power supply (controlling the heat pads and one solenoid valve)
  - 10,000 Lux lamp
  - power supply for the ultrasound particl atomizer

The usb cable must then be plugged into your computer. The Arduino script should have already been uploaded to the device, but in case anything happens, a copy can be found in the ChamberControl folder. 

Open the chamber_operation_arduino python script and ensure all dependencies are met (the script itself installs some of them, but some might have been missed). Then make sure you specify where you want the temperature and humidity data to be stored on your computer by modifying the curr_dir variable.

Launch the program. The program will ask wheter the temperature should be turned on or off. If the temperature is turned on, it will ask for the desired value to be set. The same process will be done for the humidity. The program will then list all the utilized serial ports and ask which one you would like to use. Usually, only one arduino device is plugged to the computer, so just enter the only serial port listed. The chamber will run the initial configurations and will then start to control the temperature and humidity.

You will then be able to specify three commands:
1) "C": This collect data. If you choose this command, the temperature and humidity data, along with a graph, will be stored in the specified folder variable. It includes the data from the moment the command was entered to 20 seconds after both variables have been set.
2) "T": This outputs the current temperature in the chamber. It is the average value given by the four different sensors.
3) "H"" This outputs the humidity in the chamber. It is the average value given by the four different sensors.

#2. Turning on the high speed camera:

The photron SA5 high speed camera should be connected to the electrical outlet with a cable that has an hirose connector. If the camera is plugged properly, the green light will light on. The other connection to be made is the ethernet cable, which should be plugged into the computer that will perform the analysis. 

Turn on the computer and enter into the PFV4 software. When the camera is properly connected to the computer, you can select it in the software under direct -> camera control. Click on "Record".

#3. Ejecting the droplet with the compressed air system:

The 5/16" clear tube should be plugged into the laboratory hose with a worm drive clamp. This clamp is very important in the setup as it avoids the ejection of the tubing from the laboratory hose. Adjust the pressure regulator for the air ejection system, and adjust the pressure regulator for the pipette pushing piston. You can adjust the desired pressure using a screwdriver.

Turn on the ON/OFF toggle switch on top of the small circuit enclosure box. Then press on the push button switch. This will open the two solenoid valves and allow a constant flow rate to be acheived at the air ejection needle. Open the laboratory air supply. You will be able to adjust the air flow to the desired flow rate by looking at the value indicated by the rotameter. Ensure to not go above the maximum flow rate indicated on the rotameter, this could damage the instrument. Turn the ON/OFF metal toggle switch to "OFF" and then turn it "ON" again, this closes the valves and repowers ON the arduino inside the box. This will allow a sufficient pressure to be built in the compressed air line, allowing the piston and air ejection system to be ready for activation.

Pipette your solution using either the 10uL or 100uL dedicated pipette and place it in the pipette support. Lower the pipette down using the hex key, to a level where it is close to the air ejection needle. You can also adjust the height of the piston by using the hex key. The piston should directly touch the top of the pipette.

When ready to proceed to the droplet ejection, click on the recording button on the computer and quickly press on the push button switch. The droplet will be ejected as soon as the push button switch is pressed, and 10ms later, the compressed air system will be turned ON, fragmenting the droplet into multiple other smaller droplets.

You can select the relevant frames within the whole recording by adjusting the start and end cursors on PFV4.


**Tube Rotator**

This Falcon tube rotator was made to mix polymer solutions for long durations while ensuring that sedimentation does not happen. It must be plugged to a 120V AC outlet and just needs to be turned to ON. The speed can be controlled by opening the box, plugging the arduino board to the computer, adjusting the speed variable in the arduino script under TubeRotator -> tube_rotator.ino to the desired value. Since the board is not a true arduino board, the CH340 driver should be installed on your computer to be able to see the board in the arduino app. The driver can be downloaded from: https://www.elegoo.com/blogs/arduino-projects/elegoo-arduino-nano-board-ch340-usb-driver?srsltid=AfmBOooNBPDVZOu_l9fAv63BIZNMFUos_b01z_TnlKjmj5HMD87adBCv

https://github.com/user-attachments/assets/549b61cc-e7b3-4ce6-a9e2-92ba2238ea65

![8d2e3f3b-d74f-4acc-a942-e9fa067e933f](https://github.com/user-attachments/assets/460a19ba-cfa0-4b6d-93e1-4eaf823a2721)


![6c8852f8-8e95-4737-a1b6-ba9b650f0fd5](https://github.com/user-attachments/assets/36552de2-1775-4620-96f1-ec595d040fdc)


**Safety**

when using the spray setup, it is mandatory to wear PPE equipment. Safety goggles should be worn at all times as there are compressed air hazards. If using nanoparticles within the controlled chamber, everything must be done under the fume hood. The spray setup was designed to fit exactly there. Before each experiment, the water for the humidifier must be changed and put in the bin below:

![ca5ba0b2-c194-481d-a081-c201a6464cab](https://github.com/user-attachments/assets/090c7b6d-8bfe-4415-a3c9-2a9cff071bcb)

The cardboard containers for the silica beads should be changed when cleaning the chamber. The silica beads are normally blue, but change color once they absorb humidity (red). If the beads have become red, they must be placed in the oven to remove the humidity. The chamber must be considered as contaminated from the moment that nanoparticles have been sprayed in it.
