
# Arduino Basics  (9.8.18)

### About the Arduino

Rather than re-writing an inferior version here, I highly reccomend reading [this excellent SparkFun article](https://learn.sparkfun.com/tutorials/what-is-an-arduino) if you aren't familiar with Arduino. It gives a great explanation of what the Arduino is, why they're so popular, and all the information you need about the hardware it includes to get started using one. Additionally, it has links to other articles covering the basics of electricity, circuits, digital logic, etc. which may be helpful for a lot of you. 

#### What is it good at?

Arduinos are super convenient for interfacing with sensors and motors. Because they have lots of general purpose input-output digital pins, as well as analog input pins, you can collect lots of sensor data, control motors, and communicate with other devices easily. Arduino also has a good IDE and a programming language based off of C which make it simple to do each of those things with only a few lines of code. It's also helpful that they have good documentation and a very large user base, so pretty much any simple problem you could encounter will have a solution online somewhere. 

#### What is it not good at?

Arduino specs:
- Memory:          32,000 bytes   (32 kb)
- RAM:             2,000 bytes    (2  kb)
- Processor speed: 16,000,000 Hz  (16 MHz)

Average PC specs:
- Memory:          256,000,000,000 bytes (256 GB)
- RAM   :            8,000,000,000 bytes (8   GB)
- Processor speed:   3,000,000,000 Hz    (3  GHz)

When it comes to actual computing power, the Arduino simply does not compare to any modern computer. Even the 5$ Raspberry Pi Zero has 512 MB of RAM and runs at 1 GHz (it uses an SD card for memory so size will vary, but will always be multiple GB). What this means is that when we want to do any kind of real processing, we'll need to use something better suited for that such as an RPi, a laptop, or some other computing device. 

A commonly used setup for robotics applications is to connect an Arduino (or similar microcontroller) to another computer. The Arduino, which is excellent for I/O handles the reading of sensors and the control of actuators. It collects sensor information and sends a condensed version of it (e.g "Obstacle 50 cm ahead") to the other computer  which uses that information to decide what to do next. That computer sends commands back to the Arduino (e.g. "Turn 90 Degrees clockwise @ 20 RPM") which actually turns on the motors in the appropriate manner to carry out the task.

Note that there are some microcontrollers which combine these two roles. For instance the BeagleBone Black has processing power similar to a Raspberry Pi but has much better assortment of GPIO pins (65 in the BeagleBone Black vs. 8 in the RPi). So in a sense, it combines some of the best features of the RPi and Arduino in one unit. There are pros and cons to each approach and what setup you choose to use really comes down to what you're most comfortable with and what seems like the best approach for your application. And while Arduino, RPi, and BeagleBone are some of the most commonly used microcontroller / microprocessors, thousands of variations on these are available, each with different advantages and drawbacks.

---

For a lot of these lessons, we'll be writing programs intended to run on this little robot that I built a few years ago (which still needs a name so if you've got any ideas, let me know!)

[ADD PICTURE HERE]

I think this will be a good platform for us to experiment with and learn all about programming for robotics without needing the mining robot up and running and without risking damaging anything important for the competition. 

Here's a list of the components on the robot:
- Adafruit Metro Mini
- Raspberry Pi Zero
- 12V LiPo Battery
- 5V voltage regulator
- 2x geared DC motor (with encoders)
- 3 axis accelerometer (not actually useable right now since I ran out of ports on the Metro)
- Dual MC33926 Motor Driver
- Sharp GP2Y0A60SZLF Analog Distance Sensor (10-150cm)
- NEMA 17 Stepper Motor, 200 steps per revolution
- Adafruit TB6612 1.2A DC/Stepper Motor Driver Breakout Board

I'll explain each of these in more detail before we use them so don't worry if you're unfamiliar with any or all


#### The Adafruit Metro Mini

This robot uses an Adafruit Metro Mini to read its sensors and control its motors. The Metro is bascially just an Arduino Uno packed on to a smaller board. It has all the same I/O pins, the same memory and clock speed (in fact it uses the exact same processor chip), and can be programmed via the Arduino IDE as though it were an Uno. 

The Uno is nice in that it has female connectors on every pin and it's nice and big and easier to see what's going on. When you're prototyping a project, this is great because it's easy to use jumper wires to test out different circuits and debug your program. When you know how you want everything wired and you're ready to put your project into an actual robot, it can sometimes be nice to have a smaller board such as the Metro mini. This board is smaller and cheaper (15$ vs. 35$ for the Uno) but you have to solder all your connections so it's not ideal for quickly testing different circuit designs.

Note that I'll probalby refer to the Metro mini as 'the Arduino' - they are functionally the same for our purposes.

[IMAGES OF ARDUINO UNO AND METRO MINI]

#### Basic Arduino code

Download the Arduino IDE from [here](https://www.arduino.cc/en/Main/Software) and follow the steps [here](https://learn.adafruit.com/add-boards-arduino-v164/setup) to add the drivers for the Metro Mini. You may be able to upload code without these but you're less likely to run into issues if you do so I would advise it.

When you open the Arduino IDE, you'll see the following program

``` 
void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
```

As the comments indicate, the `setup()` function will run once at the beginning of the program. This is where you'll specify whether pins are being used as inputs / outputs, establish serial connection, and set the initial state of the program. Filling out this function is usually pretty straightforward. 

The `loop()` function runs once `setup()` has completed and repeats indefinitely until the Arduino loses power or is reset. Thus, when you write a program for Arduino you have to organize your code in such a way that it works properly with this endless looping. This can be tricky to get used to - programs you'd have written for school would almost never work like this. But once you get used to it, the loop turns out to be super useful for robotics applications.

### Controlling a motor

The most basic thing we need to do is spin motors that are connected to the robot's wheels. These are 12V DC motors - the specs can be found [here](https://www.pololu.com/product/3239). DC motors are the simplest type of motor we'll work with. They have two leads, a + lead and a - lead. If a voltage is applied accross those leads, the motor will spin. If a higher voltage is applied, the motor will spin faster. If we switch the direction the voltage is applied, the motor will spin the opposite direction. Simple enough.

We'll soon encounter a few problems though:
1. The Arduino's digital pins only output 5V when set to high. Our motors are rated for 12V and while they'll still spin if we apply slighly less voltage, 5V won't be nearly enough to spin them
2. Motor's can draw a lot of current. These motors have a stall current of 2.1A - this means that if we hold the shaft of the motor and stop it from spinning, the motor will be drawing 2.1A of current. Now this stall current is @ 12V but if we apply 5V, the stall current will still be about 1A. This is too much for the Arduino. The total current across all the digital pins shouldn't exceed 200mA or we risk frying the board.
3. Digital pins only have two possible values, 0V or 5V. But we want to be able to set the motor to a wide range of speeds, not just off and full speed. 


#### Pulse Width Modulation (PWM)

PWM allows us to simulate an analog output using a digital pin. It works by rapidly turning the digital pin on and off and varying the amount of time spent on versus the time spent off. If the pin is at 5V for 50% of the time and at 0V for 50% of the time, it's as though were setting the pin voltage to 2.5V. If the voltage applied to our motors is high only 10% of the time, the motors will spin at 10% of full speed. If we toggled the value slowly, say once every second, we'd be able see or hear the output changing from low to high. By toggling it very rapidly, the switching becomes unnoticeable. Think of fluorescent ceiling lights. They are actually turning on and off at the frequency of their AC power supply but because the switching happens so fast, you don't notice it.

[PWM IMAGE HERE]


#### Motor Drivers

Motor drivers address problems 1 and 2 from above. A motor driver takes a separate power supply, 12V in our case, which it applies to the motor. It also recieves a few 5V inputs from the Arduino which determine the way that the higher voltage is applied to the motor. The motor driver in our little robot expects three inputs for each motor. Two of the inputs determine the direction and the other uses PWM to set the speed.

|DIR PIN 1| DIR PIN 2| Behavior |
|:-------:|:--------:|:--------:|
| 0V | 0V | Off (coast) |
| 0V | 5V | Forward |
| 5V | 0V | Reverse |
| 5V | 5V | Off (break) |

We apply a PWM signal the the PWM pin on the motor driver to vary the speed of the motor. We use the 5V pins on the Arduino to tell the motor driver which direction and how fast to turn the motor (this draws very little current), and the motor driver uses the higher voltage input to actually drive the motor.

[MOTOR DRIVER IMAGE HERE]


#### Arduino code

[This code](https://github.com/vanderbiltrobotics/Programming-Workshops/tree/master/code/9-8-motors-range-sensors/ControlMotors), when uploaded to the robot, will cause the motors to switch between low, medium, and high speed, remaining at each speed for 2 seconds.

```
int leftMotor1 = 1;    // Left Motor
int leftMotor2 = 12;
int leftMotorPWM = 11;

int rightMotor1 = 4;    // Right Motor
int rightMotor2 = 5;
int rightMotorPWM = 10;
```
These lines aren't strictly necessary but they make it easier to refer to the correct pins later. For example, pin 4 on the Arduino is connected to the first direction control input on the motor driver. Now, rather than typing '4' when we want to refer to this pin, we can type 'rightMotor1' instead. We don't have to remember the numbers. 

```
  // Specify pin modes
  pinMode(leftMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);
  pinMode(rightMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
```
Because the Arduino's digital pins can be used as either inputs or outputs, we need to specify how were using each pin before we use them. The `pinMode(x, dir)` function sets pin x's direction to 'dir'. We only do this once so it goes in `setup()`

```
  // Set motor 1 direction
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);

  // Set motor 2 direction
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH); 
```
These lines set the directions of both motors. `digitalWrite(x, val)` sets pin x's value to 'val'. HIGH means 5V while LOW means 0V. From the table above, we see that this sets the direction of both motors to forward.

One quick note  - LOW, HIGH, and OUTPUT are all macros defined in the Arduino language. The following can be used interchangeably:

LOW == 0 == false == INPUT
HIGH == 1 == true == OUTPUT

```
  analogWrite(leftMotorPWM, 50);
  analogWrite(rightMotorPWM, 50);
  delay(2000);
```
`analogWrite(x, val)` sets pin x's value to 'val' where val is an integer in the range 0 to 255. 0 = off, 255 = full speed, 50 = ((50 / 255) * 100)% speed. `delay(2000)` just causes the program to do nothing for 2000 milliseconds, allowing us to see the effects of our speed changes. 


### Reading a sensor

#### IR range sensor

The robot has an infrared range sensor which uses pulses of light to determine the distance to objects in front of it. Range information is super useful for a mobile robot, allowing it to detect obstacles and navigate. The specs for the sensor on our robot can be found [here](https://www.pololu.com/product/2474). 

Reading from this sensor is very simple. It has 3 connections, 5V and Gnd, which power the sensor, and one signal line which sends an analog signal which corresponds to the current range reading. We connect this line to one of the analog input pins on the Arduino.

#### Analog to Digital Conversion

There is one complication we have to overcome with this sensor, but luckily, the Arduino handles it for us. The sensor encodes the range value by adjusting the voltage on the signal line. The following graph is the mapping provided in the datasheet:


The problem is that the Arduino's processor is a digital device and thus can only work in discrete values which can be represented by binary digits. The sensor is returning a continuous voltage which could take on any of the infinte values between 0 and 5V. To convert the analog values from the sensor to digital values that the processor can work with, a bit of circuitry called an analog to digital converter (ADC) is used. The ADC ['quantizes'] the continuous values into the range 0 to 1023. 0V would be quantized to 0, 5V to 1023, and an intermediate value such as 2.2V would be quantized to (2.2 / 5.0) * 1023 = 450. We do lose some accuracy as the infinite values between 0 and 5 are being mapped to only 1024 different value. However, this is still more than enough accuracy for our needs.

#### Arduino code

[Here](https://github.com/vanderbiltrobotics/Programming-Workshops/tree/master/code/9-8-motors-range-sensors/ReadRangeSensor) is code that reads values from the sensor

```
// sensor
int sensorPin = A0;

// Other vars
int sensorValue;
float voltage;
```
Here we're just giving A0 (analog input pin 0) the name 'sensorPin so it's easier to refer to. We also create a variable to store the value in once we read it and a variable to store the voltage in after we convert the quantized value to an actual voltage.

```
  sensorValue = analogRead(sensorPin);
  voltage = map(sensorValue, 0, 1023, 0, 500); 
  voltage = voltage / 100.0;
```
analogRead(x) returns the current value at analog pin A0. This  will be a value in the range 0 to 1023 so we use the `map()` function to map the value stored in `sensorValue` from the range 0-1023 to the range 0-500. 0-500 is used because map only uses integer ranges so if we want better precision, we need to first map to 0-500 and then divide by 100 to get a value in the range 0 to 5. 

##### Serial communication

That's really all there is to it.However, when we're reading from a sensor, it's helpful to be able to see the values being read by the Arduino so we can make sure everything is working right. 

If we keep the Arduino connected to a computer with a USB cable, we can use the [***serial monitor***](https://www.arduino.cc/reference/en/language/functions/communication/serial/) to send messages between the computer and the Arduino. To use the serial monitor, we add the line `Serial.begin(9600)`. 9600 is the *baud rate* and specifies the rate that bytes will be sent between the two devices. We can then use the commands `Serial.print("message")` and `Serial.println("message")` to send messages from the Arduino to the computer. If we wanted, we could write a separate program to run on the computer and send messages back from the computer to the Arduino. Starting the serial monitor in `setup()` and add the following lines in the loop,
```
  Serial.print("Quantized value:\t");
  Serial.print(sensorValue);
  Serial.print("\tVoltage:\t");
  Serial.println(voltage);
```
we can now open the serial monitor in the Arduino IDE (magnifying glass icon in the top right) and see the sensor values printed on the screen. 


### Bringing it all together

The goal for today is to write a program that makes the robot drive forward until it detects an object in front of it. When an object is detected, the robot should stop moving. If there is no longer an object detected, the robot should resume driving. All the information needed to get this program working should be available on this page. 

[A working arduino script is available here](https://github.com/vanderbiltrobotics/Programming-Workshops/tree/master/code/9-8-motors-range-sensors/ApproachWall) - try to get it working on your own before you look at this

### Helpful resources

- [Arduino programming language documentation](https://www.arduino.cc/reference/en/)





*If you have questions, comments, or concerns, message me on Slack or email jacob.gloudemans@vanderbilt.edu*