/*
 * This program turns both motors at varying speeds
*/

int leftMotor1 = 1;    // Left Motor
int leftMotor2 = 12;
int leftMotorPWM = 11;

int rightMotor1 = 4;    // Right Motor
int rightMotor2 = 5;
int rightMotorPWM = 10;

// initial directions
int m1_on = true;
int m2_on = true;


void setup() {

  // Specify pin modes
  pinMode(leftMotor1, HIGH);
  pinMode(leftMotor2, HIGH);
  pinMode(rightMotor1, HIGH);
  pinMode(rightMotor2, HIGH);
  
  // Set motor 1 direction
  digitalWrite(leftMotor1, m1_on);
  digitalWrite(leftMotor2, LOW);

  // Set motor 2 direction
  digitalWrite(rightMotor1, m2_on);
  digitalWrite(rightMotor2, LOW); 

  // Set speeds
  analogWrite(leftMotorPWM, 75);
  analogWrite(rightMotorPWM, 75);
}

int counter = 0;
void loop() {
  if (counter > 200)
  {
    switchOnOff();
    counter = 0;
  }

  counter += 1;
  delay(10);
}

void switchOnOff()
{
  // toggle on / off
  m1_on = !m1_on;
  m2_on = !m2_on;
  
  // Set motor 1 
  digitalWrite(leftMotor1, m1_on);

  // Set motor 2
  digitalWrite(rightMotor1, m2_on);
}
