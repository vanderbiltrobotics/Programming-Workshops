/*
 * This program turns both motors at varying speeds
*/

int leftMotor1 = 1;    // Left Motor
int leftMotor2 = 12;
int leftMotorPWM = 11;

int rightMotor1 = 4;    // Right Motor
int rightMotor2 = 5;
int rightMotorPWM = 10;


void setup() {

  // Specify pin modes
  pinMode(leftMotor1, HIGH);
  pinMode(leftMotor2, HIGH);
  pinMode(rightMotor1, HIGH);
  pinMode(rightMotor2, HIGH);
  
  // Set motor 1 direction
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);

  // Set motor 2 direction
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH); 
}

void loop() {

  // Slow speed
  analogWrite(leftMotorPWM, 50);
  analogWrite(rightMotorPWM, 50);
  delay(2000);

  // Medium speed
  analogWrite(leftMotorPWM, 125);
  analogWrite(rightMotorPWM, 125);
  delay(2000);

  // Fast speed
  analogWrite(leftMotorPWM, 200);
  analogWrite(rightMotorPWM, 200);
  delay(2000);
}
