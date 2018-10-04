# Ubuntu and ROS setup

While experimental versions exist for Windows and Mac, ROS is only fully supported on Linux machines. Ubuntu is the best option for using ROS at present. Therefore, it would be ideal if everyone on the programming team has access to some machine that's running Ubuntu so they have the ability to use ROS when they need to.

We'll be using Ubuntu 16.04 with ROS Kinetic for our ROS codebase this year. Below I've linked to guides for installing everything you'll need. While it's not absolutely necessary that you have linux installed, you should, at the very least, have access to a linux system. Installing it using a virtual machine or setting up dual boot are the best options as you'll then have access to Ubuntu as long as you have your laptop, plus you'll still be able to use your computer in all the same ways you usually do. Ubuntu Mate, which supports ROS, can be set up on a Raspberry Pi so that is another option. Finally, the server in Plant Ops is running Ubuntu 16.04 so logging into that system remotely is another option.

### Ubuntu Installation


##### Windows users


###### Using a virtual machine


[Here is a good tutorial](https://www.codeooze.com/windows-10/windows-10-ubuntu-vbox/) for installing Ubuntu on a Windows system using VirtualBox

[And here is a video](https://www.youtube.com/watch?v=GGorVpzZQwA) if you'd prefer that which walks through installing Ubuntu using VirtualBox


###### Using a hard drive partition

Follow [this guide](https://itsfoss.com/install-ubuntu-1404-dual-boot-mode-windows-8-81-uefi/) to set up a dual boot system. This will enable you to boot to either Windows or Ubuntu whenever you start your computer. [This tutorial](https://www.tecmint.com/install-ubuntu-16-04-alongside-with-windows-10-or-8-in-dual-boot/) also looks pretty good


##### Mac


###### Using a virtual machine

[Here's a written tutorial](https://www.simplehelp.net/2015/06/09/how-to-install-ubuntu-on-your-mac/) for Ubuntu installation on Mac using VirtualBox 

And [here is a video](https://www.youtube.com/watch?v=sNixOS6mHlU)


###### Using a hard drive partition

While dual boot is certainly still an option for Mac users, I've read that it actually tends to run better using a virtual machine. As a virtual machine is safer and easier to set up, I don't reccommend setting up dualboot for a Mac. However, if you want to try it anyway, [here](https://www.maketecheasier.com/install-dual-boot-ubuntu-mac/) is a tutorial that goes through the steps.


##### Raspberry pi

[Here are the steps](http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi) to get ROS running on a Raspberry pi. This can be done using the standard RPi operating system (Raspbian Jessie) or using Ubuntu Mate, a lightweight version of Ubuntu. Either option should work but I reccomend using Ubuntu Mate. 

### ROS installation

Follow the [steps on the ROS website](http://wiki.ros.org/kinetic/Installation/Ubuntu) for setting up ROS on your linux system. Make sure you install Kinetic and not a different version


### Other reccomended software

I suggest downloading [CLion](https://www.jetbrains.com/clion/download/#section=linux) on your Ubuntu system. This is a nice IDE that should make it easier to build and debug ROS packages without having to rely quite so much on the terminal

I also reccomend installing [GitKraken](https://support.gitkraken.com/how-to-install). This is similar to GitHub desktop (which doesn't have a linux version) and will make it easier to do version control with Git and GitHub.