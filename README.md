# Automated Robot Markup Syntax
Markup syntax for generating files for use in multiple robotic simulation environments.

# About
Much like Markdown is used for easily formatting and creating stylized text. ARMS's goal is to create a simple and easily modifiable syntax for robot specifications across many simulation environments. So instead of learning the APIs of multiple environments, anybody can just learn ARMS and have the files needed to get their robot into their chosen environment.

The first environment ARMS will target is the Open Dynamics Engine. https://bitbucket.org/odedevs/ode/overview

# Getting Started

### To run Armature:
- Install toml
> pip install toml
- Run:
> python Armature.py my/file/location.toml where/I/want/to/save

### To see ODE in action:
- >git clone https://bitbucket.org/odedevs/ode
- Navigate to odedevs-ode-841a072b124c/build/
- Run:
 >premake4.exe --only-single --with-demos vs2010
- Open Visual Studio 2017
- Click File/Open/File...
- Navigate to **odedevs-ode-841a072b124c\build\vs2010\ode.sln**
- Right click any of the demo_* projects and click "Set as StartUp Project"
- Click "Local Windows Debugger" in the top bar of Visual Studio

    You can put any .cpp file genterated by Armature into an ODE demo's associated .cpp file to see the results of a ARMS file.

# Syntax Specification v0.5.0
Below is a list of configurations currently supported by ARMS

## Shapes:
```
[[Sphere]]
position = [0, 0, 0] #Position in world space
radius = 1.0 #Radius of the sphere
name = "ball" #Name that is used to reference this shape in joint.
color = [1, 0, 0] #color in RGB
```

```
[[Box]]
position = [0, 0, 0] #Position in world space
sides = [1.0, 1.0, 1.0] #Sides in length, width, height
name = "box" #Name that is used to reference this shape in joint
color = [1, 0, 0] #color in RGB
```

## Joints:
```
[[joint]]
joint_type = "ball" #Type of this joint (Type will move into square brackets in the future)
name = "ball_joint" 
parent = "ball" #parent shape
child = "box" #child shape
```
## Functionality:
```
[[non_colliding_groups]] #objects named in a group will not collide with each other
group1 = ["box1", "box2", "big_box"]
group2 = ["box3", "box4", "big_box"]
```
```
#Constants can be used with $ syntax
[[Constants]]
color = [1, 0, 1]
size = 1.0

#Ex:
[[box]]
sides = ["$size", "$size", "$size"]
color = "$color"
```

# Roadmap
Trello Board: https://trello.com/b/xtciB7o8/arms

# Contact

Project Lead: Dr. Anthony J. Clark ([anthonyjclark](https://github.com/anthonyjclark))

Lead Developer: Dillon Flohr ([dillonflohr](https://github.com/DillonFlohr))
