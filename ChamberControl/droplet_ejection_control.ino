// Set GPIO pins
const int relay_piston = 3;
const int relay_compressor = 5; 
int push_button = 4;

int lastButtonState = HIGH;   // the previous reading from the input pin
int buttonState = HIGH;       // the current stable reading from the input pin
int num_iter = 1;

// Debounce parameters
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

void setup() {
  
  // Set Pin Modes
  pinMode(relay_piston, OUTPUT);
  pinMode(relay_compressor, OUTPUT);
  pinMode(push_button, INPUT_PULLUP);

  digitalWrite(relay_piston, LOW);
  digitalWrite(relay_compressor, LOW);  

  Serial.begin(9600);

}

void loop() {

  int reading = digitalRead(push_button); // Read the state of the button

  // Check if the button state has changed
  if (reading != lastButtonState) {
    // Reset the debouncing timer
    lastDebounceTime = millis();
  }

  // Check if the stable state has been reached
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // If the button state has changed
    if (reading != buttonState) {
      buttonState = reading;

      // Only take action if the new button state is LOW
      if (buttonState == LOW) {
        Serial.println("Button is pressed");

          // set initial pin states
        if (num_iter == 1)
        {
          digitalWrite(relay_piston, HIGH);
          delay(50);
          digitalWrite(relay_compressor, HIGH);
          Serial.println("num_iter");
          Serial.print(num_iter);
          num_iter += 1;
        }
        // else if (num_iter == 2)
        // {
        //   digitalWrite(relay_piston, HIGH);
        //   Serial.println("num_iter");
        //   Serial.print(num_iter);
        //   num_iter += 1;
        // }
        else if (num_iter == 2)
        {
          digitalWrite(relay_piston, LOW);
          digitalWrite(relay_compressor, LOW);
          Serial.println("num_iter");
          Serial.print(num_iter);
          num_iter = 1;
        }
      }
    }
  }

  // Save the reading for the next loop iteration
  lastButtonState = reading;

  delay(10); // Short delay to make the loop more stable
}
