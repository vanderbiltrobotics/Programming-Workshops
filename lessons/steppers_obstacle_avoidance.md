# Stepper Motors and Basic Obstacle Avoidance (9.18.18)

### Types of Motors


#### DC Motors

DC motors are powered by two wires, power and ground. When a voltage is applied across their leads, they rotate continuously. Direction is determined by the polarity of the voltage across the leads while speed is determined by the magnitude of the voltage. Often, PWM is used to mimic voltages between fully off and fully on by rapidly pulsing the power on and off with varying duty cycles. If any of this is unfamiliar, it was explained in the previous lesson so check that out. [This video](https://www.youtube.com/watch?v=GQLED3gmONg) also gives an awesome explanation with visuals.

#### Servo Motors

Servo motors combine a dc motor with a set of gears, a control circuit, and a potentiometer. Rather than spinning continuously, a servo has a specific range of motion, generally around 180 degrees. The motor takes 3 inputs, power, ground, and a PWM signal. In servo motors, the PWM signal doesn't control the speed of rotation but rather the angle of the motor shaft. Servos don't rotate continuously, they stay fixed at the angle indicated by the PWM signal. This makes them useful for a different set of applications. For instance, in a robotic arm, you want to be able to set the angle of each joint. You want the motors to move to the correct angles, then stay there until you tell them otherwise. This would be a good place for a servo motor. Our robot doesn't have any servos on it but if you're interested in how to control them with Arduino, the documentation is [here](https://www.arduino.cc/en/reference/servo). And here is [a more in-depth video](https://www.youtube.com/watch?v=J8atdmEqZsc). 

#### Stepper Motors

Stepper motors are so-named because they rotate in discrete steps. There are different configurations for stepper motors, generally requiring 4, 6, or 8 wires as inputs. Pairs of two wires each control a different set of windings which when energized in a certain way cause the motor to take one step. By continuously alternating which coils are energized, you can cause the motor to step quickly. Each step moves the motor a very precise amount, allowing for precise position control. If a stepper motor has 200 steps per revolution (1.8 deg / step), we can turn the shaft exactly 180 degrees by taking 100 steps. Unlike servos, stepper motors have no limits on how far they can turn in either direction. Stepper motors are often used in 3D printers, CNC machines, and optical disk drives, places where precise position control is required over many revolutions of the motor. Adafruit has [a good overview of stepper motors here](https://learn.adafruit.com/all-about-stepper-motors/what-is-a-stepper-motor)

### Controlling a stepper motor

In our robot, the IR range sensor is mounted on a NEMA 17 stepper motor. This motor has 200 steps / revolution so 1.8 degrees per step. The Arduino controls the stepper using [an Adafruit tb6612 stepper motor driver](https://learn.adafruit.com/adafruit-tb6612-h-bridge-dc-stepper-motor-driver-breakout/overview). Like with the driver for the dc motor, we connect the higher voltage (12v) power supply to the 'vMotor' pins on this board. The steppers are powered with the high voltage while the Arduino communicates with the board using lower voltage. The driver has 2 pins for each coil in the stepper motor (MOTORA, MOTORB) - this is where we connect the wires coming from the motor. In addition to 5V and Gnd, 4 more inputs are required to control the driver: AIN1, AIN2, BIN1, and BIN2. These each connect to a digital I/O pin on the Arduino. For more on what this driver does and how it works, check out the page linked above.

#### Arduino code

Stepping the motor repeatedly requires rapidly switching which coils are energized. It would be tricky to code this behavior ourselves, but luckliy [Arduino provides a library](https://www.arduino.cc/en/Reference/Stepper) which makes it easy to control this kind of stepper. [This code](https://github.com/vanderbiltrobotics/Programming-Workshops/tree/master/code/9-18-steppers-obstacle-avoidance/BasicStepperMotorControl) uses that library to rotate the stepper back and forth, 180 degrees at a time.

`#include <Stepper.h>` gives us access to the stepper library. `Stepper stepper(STEPS, INA2, INA1, INB1, INB2);` is where we create our Stepper object which will allow us to easily control the motor. We input the steps per revolution for the motor as well as the four pins that are connected to the motor's driver. `stepper.setSpeed(20)` sets the RPM the motor will turn at once we start stepping.

```
stepper.step(STEPS / 2);
delay(500);
stepper.step(-STEPS / 2);
delay(500);
```
This is where we do the actual stepping. The `step(n)` method will step the motor exactly n times. Passing a negative number reverses the direction of the steps. Note that the delays aren't necessary.


#### Zeroing the stepper motor

Stepper motors are useful because they let us control the position of the motor shaft very precisely. For our application, we want to know the direction that the IR range sensor is pointing relative to the robot. However, with a stepper motor, we don't know the absolute position of the shaft, we only know how many steps we've taken in either direction since the program started (assuming that we've kept track of this). For that information to be useful, we need to know how the motor was oriented when the program started running. In an application where high precision is important, this is usually solved by adding a limit switch. When the program starts, the stepper will turn in one direction until a switch is pressed. Because the location of the switch is fixed, the exact position of the stepper motor is then known. We don't have a limit switch on the robot unfortunately. One way to adress this issue is to manually point the sensor in a known direction before starting the robot. Your code should then assume that this starting location is where the motor is when the code starts. It's not ideal but it's the best we can do for now. 

### Today's task - avoiding obstacles

The final goal for today is to write a program that causes the robot to drive around the room avoiding obstacles. There are different ways to accomplish this, some of which will make use of the stepper motor and some of which may not. The important thing is that the robot doesn't hit any obastacles as it drives around (including things that may be harder to avoid such as like chair legs). 

Here are some things that may be helpful for completing this task

#### Taking a sweep of sensor readings

An important thing to realize is that the range sensor covers a pretty small angle. If the sensor is pointing straight ahead, it won't necessarily detect a narrow object that's slightly to the side, even if the robot could run into that object. For this reason, it may be useful to scan across the region in front of the robot by rotating the sensor back and forth. [Here is code that will do that.]() Notice that unlike the first stepper example, we take small steps here. If we do `stepper.step(100)`, the code will not advance until all 100 steps have finished. That means there's no chance for us to take sensor readings in between. There's also a variable, `currentSteps` which keeps track of how many steps we've taken relative to the start position. Any time that we take more steps, currentSteps should be updated. Now, if we detect an obstacle in a sensor reading, we know the exact direction to the obstacle - it's just `currentSteps` converted to an angle. 


#### Responding to the obstacle (helper functions)

It's useful to be able to momentarily pause the loop, do some other task, then resume the loop once the task is finished. You can use a helper function for this. Define a function outside the loop, at the bottom of the page. If you then call this function from within the loop, you'll jump to that function, execute it, and return to the loop. [This example]() shows how you can do that to periodically switch the direction of a motor.

#### Turning

We didn't really cover turning in the previous lesson so I'll go over it briefly here. For this type of vehicle, where each wheel has its own motor (contrast this to a car), we turn the robot by driving the motors at different speeds. If both motors are moving the same direction, one slightly slower than the other, the robot will turn along a wide arc. If one motor is much slower than the other, the arc will have a much smaller radius. If one wheel is completely stationary, the other wheel will circle around the stationary wheel with the stationary wheel at the center of the arc. Finally, if the motors are spinning in opposite directions at the same speed, the robot will rotate in place.

---

You should now have enough information to write a pretty good obstacle avoidance program. If you're having trouble, it's often helpful to write out your desired behavior and a rough outline of the algorithm on paper before trying to code it. You can also start with a simpler obstacle avoidance strategy, identify any cases where it fails, and gradually make it better. Or maybe a simple strategy is all you need!

[I'll post a working Arduino script here]() once the meeting is done.

#### Potential improvements

We can now drive around avoiding obstacles. However, we are essentially just driving randomly. Now that we know the basics tools for driving around without hitting things, we want to be able to the following 
- Drive exact distances, drive at exact speeds, turn precisely, etc.
- Given a map of the room we're in, figure out where we are in the room
- Knowing where we are in the room, figure out the best route to a different location and drive to that location
- When we aren't given a map of the room, build a map of the room

We'll be looking at ways to solve each of these problems in the coming weeks


*If you have any questions, comments, or concerns, message me on Slack or email jacob.gloudemans@vanderbilt.edu*