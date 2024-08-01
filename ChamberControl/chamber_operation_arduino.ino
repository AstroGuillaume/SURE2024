
// LIBRARIES
#include <Wire.h> // allows communication to I2C devices
#include <SparkFun_Qwiic_Relay.h>
// #include <Adafruit_Sensor.h>
#include <Adafruit_Si7021.h>

// function prototypes
void clearSerialMonitor();
void print_desiredValues();
int  getValue();
void tcaselect(uint8_t i);
void read_tempAndHumidity();
float readHumidity();
float readTemperature();
void talk_with_python();

// Qwicc relay setup
#define RELAY_ADDR 0x18 
Qwiic_Relay relay(RELAY_ADDR); 

// Cooling chamber relay setup
int relay_cold = 2;

// temperature sensor setup 
Adafruit_Si7021 sensor = Adafruit_Si7021();

// recall: float is a data type that holds up to 7 digits (unlike const int, these can be changed)
float RH1 = 0.0; // intialization of 'Read Humidity value
float T1 = 0.0; // initliazation of 'Temperature' value
float RH2 = 0.0; 
float T2 = 0.0;
float RH3 = 0.0;
float T3 = 0.0;
float RH4 = 0.0;
float T4 = 0.0;
float chamberHum = 0.0;
float chamberTemp = 0.0;

// multiplexer setup
#define TCAADDR 0x70

// multiplexer id setup 
// recall: const int is a data type that can store decimals, octals and hexadecimal bases. It is assigned only when declared and cannot be changed afterwards. 
const int TRH1 = 0; // corresponding ID #0 on multiplexer
const int TRH2 = 1; // corresponding ID #1 on multiplexer
const int TRH3 = 2; // corresponding ID #3 on multiplexer
const int TRH4 = 3; // corresponding ID #4 on multiplexer
// const int RELAY_Hum = 4; // relay for humidifier
const int pin_hum = 56;
const int RELAY_Heat = 5; //relay for heating

int getValue(){
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n'); // Read input until newline character
    int desiredValue = inputString.toInt(); // Convert input string to an integer
    return desiredValue;
  }
}

String getString(){
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n'); // Read input until newline character
    return inputString;
  }
}

// Declare the global variables
float desiredHum;
float desiredTemp;  

float temperature;
float humidity;
String msg;

String humidity_ON;
String temperature_ON;

void setup() {

  // begin serial transmission
  Wire.begin(); 
  Serial.begin(9600);
  while (!Serial); delay(2000); // errorproofing: 2 second wait time for serial monitor to be opened
  sensor.begin();
  relay.begin();

  // clear the serial monitor
  clearSerialMonitor();

  Serial.println("Just started the initial configurations. Please wait... \n");
  delay(1000);
  
  // set the relay for the cooling chamber
  pinMode(relay_cold, OUTPUT);
  pinMode(pin_hum, OUTPUT);
  digitalWrite(relay_cold, LOW);
  digitalWrite(pin_hum, LOW);

  // INITIALIZE MUX - 8 available ports in total 
  for (uint8_t t=0; t<8; t++) {
    tcaselect(t); // tcaseselect is used to specify which multiplexer port you want to access
    Serial.print("TCA Port #"); Serial.println(t);
    for (uint8_t addr = 0; addr<=127; addr++) {
      if (addr == TCAADDR) continue; // continue allows you to skip forward in the loop

      Wire.beginTransmission(addr);
      if (!Wire.endTransmission()) {
        Serial.print("Found I2C 0x");  Serial.println(addr,HEX);
      }
    }
  }
  Serial.println("\ndone");

  // TEMPERATURE AND RELATIVE HUMIDITY 
  read_tempAndHumidity();

  relay.turnAllRelaysOff();
  Serial.println("Finished the initial configurations\n");
}



void loop()
{ 
  read_tempAndHumidity();
  talk_with_python();

  if (humidity_ON == "ON")
  { 
    // CONDITIONAL TO TURN ON HUMIDITY RELAY
    read_tempAndHumidity();
    talk_with_python();
    // Serial.println(chamberHum);
    // Serial.println(desiredHum);
    if(chamberHum < desiredHum)
    {
      bool increaseHum = true; 

      // tcaselect(RELAY_Hum); // this is in MUX port 4
      // relay.turnRelayOn();
      digitalWrite(pin_hum, HIGH);


      while(increaseHum == true)
      {
        read_tempAndHumidity();
        talk_with_python();

        if(chamberHum >= desiredHum)
        {
          increaseHum = false;
        }
      }
      // tcaselect(RELAY_Hum);
      // relay.turnRelayOff();
    }
    else if(chamberHum >= desiredHum)
    {
      // tcaselect(RELAY_Hum);
      // relay.turnRelayOff();
      digitalWrite(pin_hum, LOW);
      read_tempAndHumidity();
      talk_with_python();
    }
  }
    
  if (temperature_ON == "ON")
  {
    // CONDITIONAL TO TURN ON HEAT RELAY
    if(chamberTemp < desiredTemp)
    {
      digitalWrite(relay_cold, LOW);
      bool increaseTemp = true; 

      tcaselect(RELAY_Heat); // this is in MUX port 5
      relay.turnRelayOn();
      
      while(increaseTemp == true)
      {
          read_tempAndHumidity();
          talk_with_python();

          if(chamberTemp >= desiredTemp)
          {
            increaseTemp = false;
          }
      }
      tcaselect(RELAY_Heat);
      relay.turnRelayOff();
    }
    else if(chamberTemp >= desiredTemp)
    {
      tcaselect(RELAY_Heat);
      relay.turnRelayOff();
      digitalWrite(relay_cold, HIGH);
      read_tempAndHumidity();
      talk_with_python();
    }
  }
    
  }







// ** FUNCTION DEFINITIONS BELOW **

void clearSerialMonitor()
{
  for (int i = 0; i < 50; i++)
  {
    Serial.println(); // Print empty lines
  }
}

void tcaselect(uint8_t i) { // uint8 means unsigned int of 8 bytes 
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

void print_desiredValues()
{
  
  Serial.print("Desired Humidity: ");
  Serial.println(desiredHum);
  Serial.print(" %");
  Serial.print("Desired Temperature: ");
  Serial.println(desiredTemp);
  Serial.print(" degrees celcius");
  Serial.println();

}


void read_tempAndHumidity()
{
  tcaselect(TRH1);
  T1 = sensor.readTemperature();
  RH1 = sensor.readHumidity();
  tcaselect(TRH2);
  T2 = sensor.readTemperature();
  RH2 = sensor.readHumidity();
  tcaselect(TRH3);
  T3 = sensor.readTemperature();
  RH3 = sensor.readHumidity();
  tcaselect(TRH4);
  T4 = sensor.readTemperature();
  RH4 = sensor.readHumidity();

  chamberHum = (RH1+RH2+RH3+RH4)/4;
  chamberTemp = (T1+T2+T3+T4)/4;
}

float readHumidity(){
    // get the sensor to read the temp and humidity again during each while loop iteration
  tcaselect(TRH1);
  RH1 = sensor.readHumidity();
  tcaselect(TRH2);
  RH2 = sensor.readHumidity();
  tcaselect(TRH3);
  RH3 = sensor.readHumidity();
  tcaselect(TRH4);
  RH4 = sensor.readHumidity();

  return (RH1+RH2+RH3+RH4)/4;
}

float readTemperature(){
  // get the sensor to read the temp and humidity again during each while loop iteration
  tcaselect(TRH1);
  T1 = sensor.readTemperature();
  tcaselect(TRH2);
  T2 = sensor.readTemperature();
  tcaselect(TRH3);
  T3 = sensor.readTemperature();
  tcaselect(TRH4);
  T4 = sensor.readTemperature();
  return (T1+T2+T3+T4)/4; // updated temp
}

void talk_with_python()
{
  // Check if there's at least one byte available on the serial buffer
  if (Serial.available() > 0) 
  {
    // Read the command string until a newline character is encountered
    String command = Serial.readStringUntil('\n');
    Serial.println("command received: \n");
    Serial.println(command);
  
    // Compare the received command with "TEMP" and "HUMI"
    if (command == "T") 
    { 
      float temp = readTemperature();
      Serial.println(temp);
    }
    else if (command == "H")
    { 
      float humi = readHumidity();
      Serial.println(humi);
    }

    else if (command.startsWith("ST"))
    {
      desiredTemp = command.substring(2).toFloat();
      Serial.println("entered temp: ");
      Serial.println(desiredTemp);
      Serial.println("temperature command received and processed\n");
      Serial.println("next...");
    }

    else if (command.startsWith("SH"))
    {
      desiredHum = command.substring(2).toFloat();
      Serial.println("humidity command received and processed\n");
      Serial.println("next...");
    }

    else if (command.startsWith("TO"))
    {
      if (command.endsWith("ON"))
      {
        temperature_ON = "ON";
        Serial.println("Temperature was set ON");
        Serial.println("next...");
      }
      else if (command.endsWith("OFF"))
      {
        temperature_ON = "OFF";
        Serial.println("Temperature was set OFF");
        Serial.println("next...");
      }
    }
    else if (command.startsWith("HO"))
    {
      if (command.endsWith("ON"))
      {
        humidity_ON = "ON";
        Serial.println("Humidity was set to ON");
        Serial.println("next...");
      }
      else if (command.endsWith("OFF"))
      {
        humidity_ON = "OFF";
        Serial.println("Humidity was set to OFF");
        Serial.println("next...");
      }
    }
  }
}