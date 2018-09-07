import toml

toml_string = """
#parent shape
[car]
body = "cube"
color = "blue"
#this for dimensions
width = 5
length = 7
height = 2
#or this
dimensions = [5, 7, 2]
    #joint syntax
    #parent.joint_type.child
    [car.hinge.front_left_wheel]
    axis = [0, 1, 1]
    anchor = [0, 1, 0]
        #child specification
        [front_left_wheel]
        body = "sphere"
        radius = "1"
        color = "red"
    [car.hinge.front_right_wheel]
    axis = [0, -1, 1]
    anchor = [0, 1, 0]
        #child specification
        [front_right_wheel]
        body = "sphere"
        radius = "1"
        color = "red"
    [car.hinge.back_left_wheel]
    axis = [0, 1, 1]
    anchor = [0, 1, 0]
        #child specification
        [back_left_wheel]
        body = "sphere"
        radius = "1"
        color = "red"
    [car.hinge.back_right_wheel]
    axis = [0, -1, 1]
    anchor = [0, 1, 0]
        #child specification
        [back_right_wheel]
        body = "sphere"
        radius = "1"
        color = "red"
"""

parsed_toml = toml.loads(toml_string)

print(parsed_toml)