// This is based on Sweep
// by BARRAGAN <http://barraganstudio.com> 


#include <Servo.h> 

// Create the servo objects
Servo servox;
Servo servoy;

double pos = 0; // Position incrementer
float spd = 0.005; // This value seems to work for reasonable speed.
float facter; // Ratio between servox and servoy periods.
float starter; // Starting position offset between the servos.
//float facter2 = 1.0; // Ratio between servox and servoy periods.
//float starter2 = 0; // Starting position offset between the servos.
int adjx = 90; // Position of servox
int adjy = 90; // Position of servoy
float decay = 60000; // Gives the amount of steps to run on. Higher gives a slower decay.
float scale; // Scaling the image to maximum size. Gets adjusted after first run.
float circle_size;
float circle_speed;
float circle_start;
float min_x;
float min_y;
bool first_loop;

void setup() { 
  servox.attach(6);  // attaches the servo on pin 9 to the servo object
  servoy.attach(7);  // attaches the servo on pin 10 to the servo object
  pinMode(3, INPUT_PULLUP); // Starting button input
  Serial.begin(9600);
} 

void loop() { 
  // Wait for a button press.
  while (digitalRead(3) != 0) {
    if (Serial.available() > 0 ) {
      facter = Serial.parseFloat();
      starter = Serial.parseFloat();
      //circle_size = Serial.parseFloat();
      //circle_speed = Serial.parseFloat();
      //circle_start = Serial.parseFloat();
      //min_x = Serial.parseFloat();
      //min_y = Serial.parseFloat();
      //scale = Serial.parseFloat();
    }
  }

  // Main loop, to 90% decay in amplitude of the movements.
  first_loop = true;
  decay = 60000;
  //facter = 2.015;
  //starter = 1.57;
  circle_size = 0.5;
  circle_speed = 0.0;
  circle_start = 1.57;
  min_x = 52.5;
  min_y = 35.35;
  scale = 2.0151;

  for(pos = int(decay*0.1); pos < decay; pos += 1)
  {  
    // Adjx just gives me a nice sine wave
    adjx = 90 - (int)min_x + int(70 * scale * (pos/decay * sin(pos * spd) + circle_size * (pos/decay) * sin(circle_start + (pos * spd * circle_speed))));

    // Also a sinewave, with offsets and different period.
    adjy = 90 - (int)min_y + int(70 * scale * (pos/decay * sin(starter + pos * spd * facter) + circle_size * (pos/decay) * cos(circle_start + (pos * spd * circle_speed))));

    servox.write(adjx);
    servoy.write(adjy);

    // This gives us time to drop the pen
    if (first_loop) {
      first_loop = false;
    }

    delay(1); // Just for consistent speed.
  } 
}
