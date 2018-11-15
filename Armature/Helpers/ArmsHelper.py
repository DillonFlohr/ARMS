from enum import Enum

class ArmsValue(Enum):
	box = 'box'
	sphere = 'sphere'
	name = 'name'
	color = 'color'
	sides = 'sides'
	radius = 'radius'
	position = 'position'
	parent = 'parent'
	child = 'child'
	constants = 'constants'
	non_colliding_groups = 'non_colliding_group'

shapes = {
	'box': 0,
	'sphere': 0
}

joints = {
	'ball_and_socket': 0
}

def get_required_value(body, value):
	if value in body:
		return body[value]
	else:
		if ArmsValue.name.value in body:
			print(f"Error: {body[ArmsValue.name.value]} is missing the required attribute: {value}.")
		else:
			print(f"Error: An object is missing the required attribute: {value}")
		quit()

def get_optional_value(body, value):
	if value in body:
		return body[value]
	else:
		if value == ArmsValue.color.value:
			return [0, 0, 1]

def get_shape_by_name(target_name, armsDict):
	result = None
	for shape in shapes:
		if shape in armsDict:
			for item in armsDict[shape]:
				if item[ArmsValue.name.value] == target_name:
					result = item

	if result != None:
		return result
	else:
		print(f"Shape with name {target_name} does not exist. \nExiting the program.")
		quit()

# A shape is a root unless there is a joint with that shape as a child
def shape_is_root(shape_name, arms):
	is_root = True
	for joint_type in joints:
		if joint_type in arms:
			for joint in arms[joint_type]:
				if (joint['child'] == shape_name):
					is_root = False
					
	return is_root