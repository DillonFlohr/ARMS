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
> python Armature.py --selectedFileType my/file/location.toml where/I/want/to/save

### To see ODE in action:
- Download the repository https://bitbucket.org/odedevs/ode
- Navigate to odedevs-ode-841a072b124c/build/
- Run:
 >premake4.exe --only-single --with-demos vs2010
- Open Visual Studio 2017
- Click File/Open/File...
- Navigate to **odedevs-ode-841a072b124c\build\vs2010\ode.sln**
- Right click any of the demo_* projects and click "Set as StartUp Project"
- Click "Local Windows Debugger" in the top bar of Visual Studio

    You can put any .cpp file genterated by Armature into an ODE demo's associated .cpp file to see the results of a ARMS file.

## Export Options for v0.7.0 or later:
Below are the currently supported export options.

> --drawstuff
> --sdf
# Syntax Specification v0.7.0
Below is a list of configurations currently supported by ARMS



## Shapes:
```
[[sphere]]
position = [0, 0, 0] #Position in world space
relative_position = [0, 0, 0] #Position relative to this shapes parent
radius = 1.0 #Radius of the sphere
name = "ball" #Name that is used to reference this shape in joints and groups
color = [1, 0, 0] #color in RGB
```

```
[[box]]
position = [0, 0, 0] #Position in world space
relative_position = [0, 0, 0] #Position relative to this shapes parent
sides = [1.0, 1.0, 1.0] #Sides in length, width, height
name = "box" #Name that is used to reference this shape in joints and groups
color = [1, 0, 0] #color in RGB
```

## Joints:

```
[[ball_and_socket]]
name = "ball_joint" 
parent = "ball" #parent shape's name
child = "box" #child shape's name
relative_position = [0.0, 1.0, -1.0] #This position is relative to the parent
```

### Currently, the following joints are only supported in SDF.

```
[[revolute]]
name = "rev_joint_1"
axis = [0, 1, 0]
relative_position = [1, 0, 0]
parent = "body"
child = "wheel1"
```

```
[[prismatic]]
name = "pris_joint_1"
axis = [1, 0, 0]
relative_position = [1.0, 0.0, 0.0]
parent = "box1"
child = "box2"
upper_limit = 0.5
lower_limit = -0.5
```

Note that a joint's relative positon is relative to the parent shape.

As of v0.5.7, when a shape is a child, it requires the relative_position attribute. This may change to having 'position' automatically be the relative position and a 'is_child' attribute required in future versions of ARMS.
## Functionality:
### Non-Colliding Groups:
```
[[non_colliding_groups]] #objects named in a group will not collide with each other
group1 = ["box1", "box2", "big_box"]
group2 = ["box3", "box4", "big_box"]
```
### Constants:
```
#Constants can be used with $ syntax
[[constants]]
color = [1, 0, 1]
size = 1.0

#Ex:
[[box]]
sides = ["$size", "$size", "$size"]
color = "$color"
```
### Macros:

A macro is a group of shapes/joints that can be repeatedly called and given parameters.

Constants (strings beginning with '$') in a macro object will first be given the value of the matching macro parameter. If there is no matching parameter the cooresponding global constant will be used.

```
# macro definition with parameter list
[[macro.attach_sphere]]
parent_name = ""
my_name = ""
joint_name = ""

    # shape in the macro attach_sphere
    [[macro.attach_sphere.ball_and_socket]]
    name = "$joint_name"
    parent = "$parent_name"
    child = "$my_name"
    relative_position = [0.0, 0.5, 0.0]

    # shape in the macro attach_sphere
    [[macro.attach_sphere.sphere]]
    name = "$my_name"
    radius = 0.5
    color = "$box_color"
    relative_position = [0.0, 1.0, 0.0]

# regular shape creation
[[sphere]]
name = "ball1"
radius = "$radius"
position = [1.0, -0.5, 10.0]

# macro call, the shape above is passed in as the parent
[[attach_sphere]]
parent_name = "ball1"
my_name = "first_attatched_sphere"
joint_name = "random_joint_name"

# another macro call, this time the shape created in the macro
# above is given as the parent of this macro shape
[[attach_sphere]]
parent_name = "first_attatched_sphere"
my_name = "second_attatched_sphere"
joint_name = "random_joint_name"
```


# Roadmap
Trello Board: https://trello.com/b/xtciB7o8/arms

# Contact

Project Lead: Dr. Anthony J. Clark ([anthonyjclark](https://github.com/anthonyjclark))

Lead Developer: Dillon Flohr ([dillonflohr](https://github.com/DillonFlohr))
