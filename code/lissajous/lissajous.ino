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

// Known good combos of params: These will generate nice-looking lissajous figures.
//p
    "multiplier":random.randint(1, 3),
    "offset":random.uniform(0.0, 0.03),
    "starter":random.uniform(0.0, 3.142),
    "circle_size":random.uniform(0.0, 1.0),
    "circle_speed":random.uniform(0.0, 3.0),
    "circle_offset":random.uniform(-0.05, 0.05),
    "circle_start":random.uniform(0.0, 3.142),
int known_good_params[][] ={
  {}
};

void setup() { 
  servox.attach(6);  // attaches the servo on pin 9 to the servo object
  servoy.attach(7);  // attaches the servo on pin 10 to the servo object
  pinMode(3, INPUT_PULLUP); // Starting button input
//  Serial.begin(9600);
  randomSeed(analogRead(0));
  servox.write(90);
  servoy.write(90);
} 

void loop() { 
  // Wait for a button press.
  while (digitalRead(3) != 0) {
//    if (Serial.available() > 0 ) {
//      facter = Serial.parseFloat();
//      starter = Serial.parseFloat();
//      circle_size = Serial.parseFloat();
//      circle_speed = Serial.parseFloat();
//      circle_start = Serial.parseFloat();
//      min_x = Serial.parseFloat();
//      min_y = Serial.parseFloat();
//      scale = Serial.parseFloat();
//      Serial.print(facter);
//      Serial.println();

    facter = random(3)/1.0 + 1.0 + random(301)/10000.0;
    starter = random(315)/100.0;
    circle_size = random(20, 100)/100.0;
    circle_speed = random(4)/1.0 - 0.05 + random(101)/1000.0;
    circle_start = random(315)/100.0;
    min_x = 0.0;
    min_y = 0.0;
    scale = 1.5;
  }
  servox.write(90);
  servoy.write(90);
  delay(5000);
  // Main loop, to 90% decay in amplitude of the movements.
  decay = 60000.0;

  for(pos = int(decay*0.1); pos < decay; pos += 1)
  {  
    // Adjx just gives me a nice sine wave
    adjx = 90 - (int)min_x + int(35 * scale * (pos/decay * sin(pos * spd) + circle_size * (pos/decay) * sin(circle_start + (pos * spd * circle_speed))));

    // Also a sinewave, with offsets and different period.
    adjy = 90 - (int)min_y + int(35 * scale * (pos/decay * sin(starter + pos * spd * facter) + circle_size * (pos/decay) * cos(circle_start + (pos * spd * circle_speed))));

    servox.write(adjx);
    servoy.write(adjy);

    delay(1); // Just for consistent speed.
  } 
}
