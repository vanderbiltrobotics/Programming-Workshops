# Introduction to Robot Operating System (ROS)

### What is ROS?

From the ROS website...

> ROS is an open-source, meta-operating system for your robot. It provides the services you would expect from an operating system, including hardware abstraction, low-level device control, implementation of commonly-used functionality, message-passing between processes, and package management. It also provides tools and libraries for obtaining, building, writing, and running code across multiple computers.

ROS provides a set of tools that make it easy to break complex robotics problems into sub-problems, develop solutions for each sub-problem, and run each solution simultaneously to achieve the overall task. This probably sounds pretty vague at the moment, but once we get into the core concepts of ROS and work through some examples, it will make a lot more sense what this means and why it's very useful. 


### Why is ROS?

Consider the robotic mining system we're trying to design. Clearly there are lots of sub-problems that each must be solved for the robot to work. We need to control the drive-train, control the dig system, detect obstacles, figure out where the robot is relative to the map of the world, and more. While there is some information that needs to be passed between each these subsystems (for instance a route planner will need to know the locations of obstacles in order to avoid them), the actual operations on that iniformation are independent. Not considering what inputs are required, the code that identifies obstacles from camera frames is totally independent from the code that computes the best path between two points. 

One way to write software to do all this would be to write lots of different classes that each solve part of the problem, then have one big file that brings the whole system together in a coordinated way. We'd have a library for localization, a library for object detection, a library for motor control, etc., and then a program that includes each of those libraries and combines all of their functionality to control the robot. While this strategy could certainly work, it has many limitations which make it undesireable.

- Our robotic system might have multiple devices which are connected on a network, each of which needs to run parts of the code. The above strategy doesn't give us an easy way to launch all the pieces of this code simultaneously, nor does it provide an easy way for those devices to relay information
- We may have lots of different versions of each of the subsystems. There are easier solutions to each problem and harder solutions, each of which will have their own advantages and drawbacks. We want an easy way to switch between those versions without having to rewrite and recompile parts of our code
- The above strategy will be harder to manage, especially as the project's complexity grows

ROS solves these problems by allowing us to separate the complex problem into different units. Each unit solves part of the problem and can send and recieve messages from other units. Additionally, we can specify which device on our network each unit will be run on, as well as which "version" of the unit we want to run, all without rewriting or recompiling anything.


### Core concepts of ROS

#### Nodes, Topics

A **node** is simply an executable that uses ROS to communicate with other nodes

A **message** is a piece of information that is passed between nodes. There are many types of messages, from simple things like 8-bit integers, to complex data structures such as images.

A **topic** is a channel on which messages are passed. A node can *subscribe* to topics (listen for messages), *publish* to topics, or both. A single topic may have multiple subscibers which listen to it or multiple publishers which write messages to it.

As an example, consider a simple, 2-node system. One node will publish increasing integers on a topic called "count." The other node will subscribe to the "count" topic and print the message "Hello World, [count]" to the screen whenver the count is a multiple of 100. This basic example uses each of the concepts described above. 

While this example is very simple and not very useful, it's easy to see how this could be expanded to larger problems. For example, in our robot, there could be a node for obstacle detection, a node for route planning, a node for localization, etc. Because a few of the other nodes need to know the locations of any obstacles, the obstacle detection node can publish that information on an "obstacles" topic. The localization and route planning nodes can then subscribe to that topic and use it to inform their decisions. 

This structure allows us to clearly separate each component of our system and gives an easy way for each component to communicate. Additionally, when we are launching the nodes (we'll cover this later), we can specify whether we want the node to run on our local system or if there's another device that we want it to run on. Provided that the other system is really there and that it has any relevant packages installed, the node will run just as we want and the communication across topics will all work exactly the same way.


#### Roscore

You may be wondering how the communication between nodes is actually taking place. The ROS *master* runs on one of the systems in the network and essentially tells all of the nodes how they should communicate. For instance, if one node publishes to the "count" topic, and two other nodes subsribe to it, the master will establish the connection between the publisher and each of the subscribers so that whenever a new message is published, each of the subsribers receives it. In order for us to launch any ROS nodes, we need to first start a ros master. To do this, we start something called *roscore* which basically starts the master running as well as a node called *rosout* which behaves much like stdout would. 


#### Packages

Packages are the basic software units of ROS. A package may contain executable files (nodes), libraries, scripts, launch files, and more. Packages are a way for us to divide up the code for our project. For instance we may have a few different versions of our obstacle detection node. We would group these together in a package called "obstacle_detection." We would then have another package for our localization code, another for drive train control, and so on. 

Every package contains the following two files:
1. package.xml - this file just provides some metadata about the package such as its name, license information, as well as any dependencies for the package
2. CMakeLists.txt - this file specifies how the package should be built when whenever we compile


#### Catkin & CMake (Ugh)

Catkin is the build system for ROS. It as an extension of the CMake build system specifically designed for making it easier to build ROS packages. C++ is a compiled language so before we can run the programs we write, we need to generate an executable file from our code. Catkin fulfils this role, ensuring that all libraries are linked properly and that executables are built. 

The package.xml and CMakeLists.txt files are what tell catkin what files to build, what dependencies each package has, what needs to link to what, etc. Thus, every package that we wish to compile needs to have these two files. We group these files within a *catkin workspace*. A catkin workspace is bascially a group of packages that we want to compile at the same time. So for example, all the packages for our system will be within a single catkin workspace. When we use the command `catkin_make` within that workspace, catkin will detect all the packages (everything with the two necessary files) and compile any of the packages that have changed since the previous compiliation.


#### Running nodes or groups of nodes

Once we've written all the nodes we need for our application and built the relevant packages, it's time to actually run the nodes. There are a few ways to do this. One is to use the `rosrun <package_name> <node_name>` command. This will launch the single node specified (note that we need to start roscore running before we can do this). If we just want to test one or a few nodes, this can be a fine way to go. Often however, we have a bunch of nodes we want to launch at the same time, possibly across multiple systems. We may also want to publish certain parameters (more on those later) or change the behavior of our system based on command line arguments. To do this, we use files called *launch files*. These are xml-type files which let us specify lots of nodes to launch at once as well as any parameters we want to publish. To use a launch file, we run the command `roslaunch <package_name <launch_file_name.launch>`. 


### What's next?

- How to set up ROS on your computer
- How to set up a catkin workspace
- How to create a ROS package and basic nodes for publshing and subscribing
- How to write CMakeLists files properly
- How to write launch files
- List of common ROS commands
- How will we use version control with ROS?

 
