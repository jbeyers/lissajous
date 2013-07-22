// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
 
Servo servox;  // create servo object to control a servo 
Servo servoy; // a maximum of eight servo objects can be created 
 
double pos = 0;    // variable to store the servo position 
float spd = 0.005;
float facter = 1.0;
float starter = 0;
int adjx = 90;
int adjy = 90;
float decay = 60000;
 
void setup() 
{ 
  servox.attach(9);  // attaches the servo on pin 9 to the servo object 
  servoy.attach(10);  // attaches the servo on pin 10 to the servo object 
  pinMode(2, INPUT_PULLUP);
  randomSeed(analogRead(0));
} 
 
 
void loop() 
{ 
  while (digitalRead(2) != 0)
  {
    delay(10);
    facter = random(2001, 2021)/1000.0;
    starter = random(3141)/1000.0;
  }
  for(pos = 0; pos < decay*0.9; pos += 1) 
  {  
    adjx = int(90 + int(70 * (1 - pos/decay) * sin(pos * spd)));
    adjy = int(90 + int(70 * (1 - pos/decay) * sin(starter + (pos * spd * facter))));
    servox.write(adjx);
    servoy.write(adjy);
    delay(1);                       // waits 15ms for the servo to reach the position 
  } 
  servox.write(90);
  servoy.write(90);
}

