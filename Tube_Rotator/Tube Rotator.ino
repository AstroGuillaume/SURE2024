#include <AccelStepper.h>

// Define stepper motor connections and motor interface type
#define dirPin 2
#define stepPin 3
#define motorInterfaceType 1

// Create a new instance of the AccelStepper class
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

// Variable to control speed
float speed = 80.0; // Speed in steps per second

void setup() {
  // Set the maximum speed
  stepper.setMaxSpeed(1000); // Set a high max speed to avoid limiting the actual speed
  stepper.setSpeed(speed); // Set the initial speed
}

void loop() {
  // Run the stepper motor at constant speed
  stepper.runSpeed();
}
