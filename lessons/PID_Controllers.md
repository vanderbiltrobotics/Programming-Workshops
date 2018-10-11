# PID Controllers

### Control Systems

Consider the following scenario: Theres a point located along a line. You have a knob that you can turn which controls the velocity of the point along that line. The farther to the right you turn the knob, the faster to the right the point moves, and the farther left you turn the knob, the farther left the point moves. Now suppose you are given a target position and your goal is to move the point to the target position, preferrably as quickly as possible. Chances are, this would be pretty easy to do. While the point is far away from the target, you move it quickly towards the target. As the point nears the target, you gradually slow it down until finally, you bring it to a stop when its position mathces the target. 

This scenario is an example of a control system. This system has the following features:
- An *output*: this is the value we care about. In this case it's the position of the point along the line
- A *target* or *input*: this is the desired value for the output. The goal of the system is to get the output to match the target
- A *controller*: this is the entity that has influence over the system. The controller can change the *manipulated variable*. In this example, the manipulated variable is the point's speed and the controller is you, the person controlling the speed.
- A *plant* or *controlled system*: this is the system which takes the manipulated variable as input and produces the output. In this example, that would be the point.
- An *error signal*: this is the difference between the output and the target value. In a control system, the error signal is fed back into the controller so that the controller can determine what it needs to do to minimize the error.

In this example, the controller was a person. Generally, however, our goal is for the system to work without human intervention. We want to design a controller programatically so that it will always keep the output close to the target. 

#### More examples

While the above example may seem rather useless, this type of system is very common. I'll list a few examples here but if you keep an eye out, you'll start to see that these systems actually occur all over the place.

- A house heating system
output = temperature of the house
target = temperature setting on the thermostat
controller = the thermostat
manipulated variable = on / off status of the heating units in the house
plant = heating unit
error = difference between the temperature setting and the actual temperature (read from a thermometer somewhere)

- An Arduino is connected to a DC motor. The Arduino has a target speed that it's trying to spin the motor at. It can control the motor by setting the voltage applied to the motor. An encoder on the motor sends information about the speed of the motor back to the Arduino. 
output = motor speed
target = desired motor speed
controller = the Arduino
manipulated variable = voltage applied to motor
plant = motor
error = target speed minus actual speed (read from encoder)

- You are driving down the highway in a car, trying to stay in the center of your lane. 
output = the car's actual position in the lane
target = the center of the lane
controller = you
manipulated variable = the position of the steering wheel
plant = the car
error = distance between the center of the lane and the car's actual position

### Designing a controller

Our goal is to design a controller that will keep the output close to our target value at all times. The controller takes the error signal as an input and produces a signal controlling the manipulated variable as output. A good type of controller which works for a wide variety of systems is called a PID controller. The letters P, I, and D stand for Proportional, Integral, and Derivative. We'll explore each of these components individually.

#### (P)roportional gain

The simplest way that we can quickly minimize the error in the system is to set our controlled variable proportionally to the error signal. If there is a large error, we send a large output signal. If the error is smaller, the output signal should be small. This is the approach we used in the first example, controlling a point along a line. When the point was far from the target, we move it quickly towards the target. As the point got nearer to the target, we moved it more slowly. Once the point reached the target, we stopped moving it entirely. We can model this behavior mathematically usign the following pseudocode

```
current_error = target_value - actual_value
output_sig = P_gain * current_error
apply(output_sig)
```

Notice that by changing the value of `P_gain`, we can change the speed at which we approach the target. A high P_gain will cause us to approach faster than if we use a lower P_gain. In real applications, the controller can't act infinitely fast, so if the P_gain is set to high, the output may overshoot the target value or even oscillate out of control.

We can design a working controller for some systems using only proportional control. For instance, in the first example, proportional control is all that we need to move the point to the target. 

The [pid_simulator_speed.py](code/PID-Simulation/pid_simulator_speed.py) simulation code is modelled after that first example. In this simulation, the controller can adjust the speed of the object at each timestep as it tries to get the object's position to match the target position. Play around with different values of P, as well as different target behaviors (try the sine wave target array or randomly wandering target array) to try and get a feel for how the P gain effects the system. 

#### (I)ntegral gain

A proportional gain alone will not always be good enough. Consider another system where instead of controlling the speed of the object, we can only control the force applied to the object. Imagine that we're trying to lift an object to a certain height. If there was no external force, we could get such a system to work just fine. If we know the mass of the object, we can just determine what force is required to accelerate the object to any given velocity at each timestep. So this system is really no different than the simple speed control example. The difference arises when we apply an external force such as gravity. In this case, the force that the controller commands will be greater than the net force that is actually applied to the object (because we subtract the force from gravity). The object will rise but level off below the actual target height. The higher the value of P we use, the closer the object will get to the target position, but it will never quite reach it. 

This leads to what we call a *steady state error*. Once the output has converged on a value (the state is steady) there is still an error. To fix this, we need to incorporate an integral term. The integral is exactly what it sounds like. As the system runs, we continually integrate the error, multply that accumulated error by another gain (I_gain), and add the result to the output determined by the proportional componenet of the controller. 

```
current_error = target_value - actual_value
integrated_error += current_error
output_sig = P_gain * current_error
output_sig += I_gain * integrated_error
apply(output_sig)
```

The I term gives us information about the 'error history.' If there has been no error, the integral term does nothing. However, if we have a steady state error, the integral of the error will quickly grow and adjust the output to eliminate that error. This prevents errors from persisting in the system over a long period of time. 

In the force-control example, if the position starts to level off below the target position, the integral sum will quickly grow and the applied force will increase until the error is eliminated. 

The [pid_simulator_force_speed.py](code/PID-Simulation/pid_simulator_force_speed.py) simulation code is modelled after this example. In this simulation, the controller can adjust the force applied to the object at each timestep as it tries to get the object's position to match the target position. In this simulation, a desired speed is calculated using the PID gains, and then the force is set such that it will accelerate the object to that speed (this differs from [pid_simulator_force.py](code/PID-Simulation/pid_simulator_force.py) where the PID gains directly determine the output force). Play around with different values of P and I to get a feel for how each influences the system. 


#### (D)erivative gain

In the I gain example, we were able to set the force so as to acheive a target speed because we knew the mass of the object. But what if we didn't know the mass of the object? In that case, our controller has to directly set the applied force (Take a look at pid_simulator_force.py and pid_simulator_force_speed.py to see the distinction). This makes our problem a little trickier. Run the force-only simulation with just a P gain to see why. The applied force will only be zero when we are already at the target position. But when the applied force is zero, the object is still moving at some velocity, it just isn't accellerating any more. So rather than approaching the target value, this controller causes the objcect to oscillate around it. It also isn't clear how an I gain would help us fix this. The error isn't consistently positive or negative.

Here, the problem is that we're approaching the object too fast. By the time the controller realizes that it's reached the object, it's already speeding past it. Here, we can improve the controller by using a Derivative term. When we're chosing the applied force, we can calculate how quickly the error is changing and adjsut accordingly. If the error is quickly decreasing, we should adjust the force in the opposite direction so that we don't overshoot. If the error is rapidly increasing, we should do the same. If the error is constant, this term shouldn't do anything. 

```
current_error = target_value - actual_value
error_slope = (previous_error - current_error) / elapsed_time
output_sig = P_gain * current_error
output_sig += D_gain * error_slope
apply(output_sig)
previous_error = current_error
```

Try manipulating the value of the D_gain in pid_simulator_force.py to see if you can get the system to stablize. 

#### Summary

The P term does most of the work. It always tries to steer the manipulated varibale in the direction that will reduce the error. 

The I term is important in systems where other factors impact the system, leading to consistent errors in the output. If any error is persistent over a long period, the I gain will eliminate it. 

The D term helps prevent overshoot by damping the system whenever the error is changing too quickly. 

While almost every system will use at least a P term, the I and D terms are generally incorporated based on the specifics of the system. PI, PD, and PID controllers are each used in a variety of situations.

### PID controllers for the competition robot

A few places where we will difinitely use some variant of a PID controller
- Controlling the speed or position of the wheels
- Controlling the speed of the digging mechanism digging mechanism
- Driving accurately along a line or an arc, making accurate turns

It's pretty likely that they will come up in other parts of the robot as well, and if you do future work in robotics, you will 100% encounter PID controllers again.

### Useful links

- [This YouTube playlist](https://www.youtube.com/watch?v=wkfEZmsQqiA&list=PLn8PRpmsu08pQBgjxYFXSsODEF3Jqmm-y) is really good - it's a little more conceptual but the first few videos should be really helpful

- If this topic is interesting to you, check out [Brian Douglas's YouTube channel](https://www.youtube.com/user/ControlLectures), he has lots of really good control systems videos

- If you [type "PID controller example" into YouTube](https://www.youtube.com/results?search_query=pid+controller+example), you'll find lots of interesting appllications 

- [Here](https://www.csimn.com/CSI_pages/PIDforDummies.html) is another good article on PID controllers