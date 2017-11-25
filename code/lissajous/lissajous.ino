// This is based on Sweep
// by BARRAGAN <http://barraganstudio.com> 


#include <Servo.h> 

// Create the servo objects
Servo servox;
Servo servoy;

double pos = 0; // Position incrementer
float spd = 0.005; // This value seems to work for reasonable speed.
float facter = 1.0; // Ratio between servox and servoy periods.
float starter = 0; // Starting position offset between the servos.
//float facter2 = 1.0; // Ratio between servox and servoy periods.
//float starter2 = 0; // Starting position offset between the servos.
int adjx = 90; // Position of servox
int adjy = 90; // Position of servoy
float decay = 60000; // Gives the amount of steps to run on. Higher gives a slower decay.
int scale = 70; // Scaling the image to maximum size. Gets adjusted after first run.
int counter = 0; // How many times through the main loop.

void setup() 
{ 
  servox.attach(6);  // attaches the servo on pin 9 to the servo object
  servoy.attach(7);  // attaches the servo on pin 10 to the servo object
  pinMode(3, INPUT_PULLUP); // Starting button input
  randomSeed(analogRead(0)); // Just seed with a random value
  Serial.begin(9600);
} 

void loop() 
{ 
    // Wait for a button press.
    while (digitalRead(3) != 0)
    {
        // Keep generating random values. Only on button press do we lock in the values.
        // The random seed is not random enough, so this provides a more random result.
        //facter = 1.015; // Increase the second number for variation.
        //starter = 3.141; // offset the starting point by 0-3.141 radians
        if (Serial.available() > 0 ) {
          facter = Serial.parseFloat();
          starter = Serial.parseFloat();
        };
    }
    // Main loop, to 90% decay in amplitude of the movements.
    decay = 60000;
    
    counter = 0;
    scale = 70;
    for(pos = int(decay*0.1); pos < decay; pos += 1)
    {  
        // Adjx just gives me a nice sine wave
        adjx = int(90 + int(scale * pos/decay * sin(pos * spd)));

        // Also a sinewave, with offsets and different period.
        adjy = int(90 + int(scale * (pos/decay) * sin(starter + (pos * spd * facter))));

        servox.write(adjx);
        servoy.write(adjy);
        delay(1); // Just for consistent speed.
    } 

    // Return to center after drawing.
    delay(5000);
    servox.write(90);
    servoy.write(90);
}

