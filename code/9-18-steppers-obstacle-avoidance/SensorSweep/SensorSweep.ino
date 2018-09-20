
/**
 * This program shows how to sweep the stepepr motor across a region while
 * taking sensor readings along the way
 */

// Include stepper library
#include <Stepper.h>

// defines
#define STEPS 200

// Sensor pin
int sensorPin = A0;

// Stepper motor pin assignments
int INA2 = 7;
int INA1 = 8;
int INB1 = 9;
int INB2 = 6;

// define our stepper motor object
Stepper stepper(STEPS, 7, 8, 9, 6);

void setup() {
  stepper.setSpeed(10);
}

int sensorValue;
int currentSteps = 0;
int stepsPerLoop = 1;

void loop() {
  
  if ((currentSteps >= 25) || (currentSteps <= -25)){
    delay(500);
    stepsPerLoop *= -1;
  }

  stepper.step(stepsPerLoop);
  currentSteps += stepsPerLoop;
  sensorValue = analogRead(sensorPin);
}
