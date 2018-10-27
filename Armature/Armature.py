try:
	import toml
except:
	print("\n**************************************\nPlease install toml to use Armature.py\n> pip install toml\n**************************************\n")
	quit()
import sys
import pprint as pp
from pathlib import Path
from enum import Enum
import copy

class ArmsValue(Enum):
	box = 'box'
	sphere = 'sphere'
	name = 'name'
	color = 'color'
	sides = 'sides'
	radius = 'radius'
	position = 'position'
	joint_type = 'joint_type'
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

#parsed as dictionary data from the .arms/toml file
arms = None

def get_shape_by_name(target_name):
	result = None
	for shape in shapes:
		if shape in arms:
			for item in arms[shape]:
				if item[ArmsValue.name.value] == target_name:
					result = item

	if result != None:
		return result
	else:
		print(f"Shape with name {target_name} does not exist. \nExiting the program.")
		quit()

def get_optional_value(body, value):
	if value in body:
		return body[value]
	else:
		if value == ArmsValue.color.value:
			return [0, 0, 1]

def get_required_value(body, value):
	if value in body:
		return body[value]
	else:
		if ArmsValue.name.value in body:
			print(f"Error: {body[ArmsValue.name.value]} is missing the required attribute: {value}.")
		else:
			print(f"Error: An object is missing the required attribute: {value}")
		quit()

def get_constant(target_const):
	result = None
	#strip $ off string
	target_const = target_const[1:]
	if ArmsValue.constants.value in arms:
		constants = arms[ArmsValue.constants.value][0]
		for var in constants:
			if var == target_const:
				result = constants[var]
	
	if result != None:
		return result
	else:
		print(f"Constant name {target_const} does not exist. \nExiting the program.")
		quit()

def get_parameter(param_list, target):
	#strip the $ of the target
	stripped_target = target[1:]

	#A parameter is optional, if it doesn't exist, a const will supply the value
	if stripped_target in param_list:
		return param_list[stripped_target]
	else:
		return target


def convert_macros():
	if 'macro' in arms:
		for macro in arms['macro']:
			current_macro = arms['macro'][macro][0]
			for macro_call in arms[macro]:
				parameter_list = {}
				for item_type in current_macro:
					#if the current item_type is a list, it is a list of objects
					if item_type in shapes or item_type in joints:
						for item in current_macro[item_type]:
							new_item = copy.deepcopy(item)
							for value in new_item:
								if type(new_item[value]) == str:
									if (is_constant_call(new_item[value])):
										new_item[value] = get_parameter(parameter_list, new_item[value])
								if type(new_item[value]) == list:
									for i in range(0, len(new_item[value])):
										if type(new_item[value][i]) == str:
											if (is_constant_call(new_item[value][i][0])):
												new_item[value][i] = get_parameter(parameter_list, new_item[value][i])
							if item_type not in arms:
								arms[item_type] = []
							arms[item_type].append(new_item)
					else:
						#otherwise it is a parameter of a macro
						if item_type in macro_call:
							parameter_list[item_type] = macro_call[item_type]
						else:
							parameter_list[item_type] = current_macro[item_type]

def is_constant_call(target):
	return target[0] == '$'

def convert_constants():
	global arms
	for group in arms:
		if group != 'macro':
			for item in arms[group]:
				for value in item:
					if type(item[value]) == str:
						if (is_constant_call(item[value])):
							item[value] = get_constant(item[value])
					if type(item[value]) == list:
						for i in range(0, len(item[value])):
							if type(item[value][i]) == str:
								if (is_constant_call(item[value][i][0])):
									item[value][i] = get_constant(item[value][i])

# A shape is a root unless there is a joint with that shape as a child
def shape_is_root(shape_name):
	is_root = True
	for joint_type in joints:
		if joint_type in arms:
			for joint in arms[joint_type]:
				if (joint['child'] == shape_name):
					is_root = False
					
	return is_root

#Recursively get the children of some parent shape
def get_children_of(parent_name):
	result = {}
	for joint_type in joints:
		if joint_type in arms:
			for joint in arms[joint_type]:
				if (joint['parent'] == parent_name):
					result[joint['child']] = get_children_of(joint['child'])

	return result

def make_shape_positions_relative_to_parents():
	#tree of parents and children
	ancestor_tree = {}

	#Get all the roots
	for shape_type in shapes:
		if shape_type in arms:
			for shape in arms[shape_type]:
				if (shape_is_root(shape[ArmsValue.name.value])):
					ancestor_tree[shape[ArmsValue.name.value]] = {}

	for root in ancestor_tree:
		ancestor_tree[root] = get_children_of(root)

	for root in ancestor_tree:
		convert_shape_positions(root, ancestor_tree[root])

#Recursively set the position of parent's children, then do the same for the children's children
def convert_shape_positions(parent_name, parent_tree):
	this_parent_position = get_required_value(get_shape_by_name(parent_name), 'position')
	for child in parent_tree:
		this_child = get_shape_by_name(child)
		this_child['position'] = [0, 0, 0]
		this_child_relative_position = get_required_value(this_child, 'relative_position')
		this_child['position'][0] = this_parent_position[0] + this_child_relative_position[0]
		this_child['position'][1] = this_parent_position[1] + this_child_relative_position[1]
		this_child['position'][2] = this_parent_position[2] + this_child_relative_position[2]
		convert_shape_positions(child, parent_tree[child])

def make_joint_positions_relative_to_parent_shape():
	for joint_type in joints:
		if joint_type in arms:
			for joint in arms[joint_type]:
				parent = get_required_value(joint, 'parent')
				parent_position = get_required_value(get_shape_by_name(parent), 'position')
				joint['position'] = [0, 0, 0]
				joint_relative_position = get_required_value(joint, 'relative_position')
				joint['position'][0] = parent_position[0] + joint_relative_position[0]
				joint['position'][1] = parent_position[1] + joint_relative_position[1]
				joint['position'][2] = parent_position[2] + joint_relative_position[2]


#Start of ODE specific functions
def create_non_colliding_groups():
	result = ""

	if "non_colliding_groups" in arms:
		groups = arms["non_colliding_groups"][0]
		for group in groups:
			new_group = f"""//Generated by Armature
	unordered_map<dGeomID, int> no_collision_map_{group};
	"""
			result = f'{result}{new_group}'
			for shape in groups[group]:
				new_shape = f"no_collision_map_{group}[geom_{shape}] = 0;\n	"
				result = f'{result}{new_shape}'
			result = f'{result}\n	no_collision_groups.push_back(no_collision_map_{group});\n	'
	
	return result


def create_joints():
	result = ""
	
	for joint_type in joints:
		if joint_type in arms:
			for joint in arms[joint_type]:
				joint_name = get_required_value(joint, ArmsValue.name.value)
				joint_position = get_required_value(joint, ArmsValue.position.value)
				if joint_type == 'ball_and_socket':
					#get parent and child
					parent = get_shape_by_name(get_required_value(joint, ArmsValue.parent.value))
					child = get_shape_by_name(get_required_value(joint, ArmsValue.child.value))
					#get their positions and names
					parent_position = get_required_value(parent, ArmsValue.position.value)
					parent_name = get_required_value(parent, ArmsValue.name.value)
					child_position = get_required_value(child, ArmsValue.position.value)
					child_name = get_required_value(child, ArmsValue.name.value)

					new_joint = f"""//Generated by Armature
	dJointID {joint_name} = dJointCreateBall(world, 0);
	dJointAttach({joint_name}, body_{parent_name}, body_{child_name});
	dJointSetBallAnchor({joint_name}, {joint_position[0]}, {joint_position[1]}, {joint_position[2]});
	"""
					result = f'{result}{new_joint}'


	return result

def body_variables():
	result = ""

	#spheres
	if ArmsValue.sphere.value in arms:
		for body in arms[ArmsValue.sphere.value]:
			new_body = f"""//Gernerated by Armature
static dBodyID body_{body[ArmsValue.name.value]};
static dGeomID geom_{body[ArmsValue.name.value]};
"""
			result = f'{result}{new_body}'

	#boxes
	if 'box' in arms:
		for body in arms['box']:
			sides = get_required_value(body, ArmsValue.sides.value)

			new_body = f"""//Gernerated by Armature
static dBodyID body_{body[ArmsValue.name.value]};
static dGeomID geom_{body[ArmsValue.name.value]};
const float sides_{body[ArmsValue.name.value]}[3] = {{ {sides[0]}, {sides[1]}, {sides[2]} }};
"""
			result = f'{result}{new_body}'

	return result

def reset_bodies():
	result = ""
	
	#spheres
	if ArmsValue.sphere.value in arms:
		for body in arms[ArmsValue.sphere.value]:
			name = get_required_value(body, ArmsValue.name.value)
			position = get_required_value(body, ArmsValue.position.value)

			new_code = f"""
	//Generated by Armature
	dQuaternion q{name};
	dQSetIdentity(q{name});
	dBodySetPosition(body_{name}, {position[0]}, {position[1]}, {position[2]});
	dBodySetQuaternion(body_{name}, q{name});
	dBodySetLinearVel(body_{name}, 0, 0, 0);
	dBodySetAngularVel(body_{name}, 0, 0, 0);
	"""

			result = f'{result}{new_code}'

	#boxes
	if 'box' in arms:
		for body in arms['box']:
			name = get_required_value(body, ArmsValue.name.value)
			position = get_required_value(body, ArmsValue.position.value)

			new_code = f"""
	//Generated by Armature
	dBodySetPosition(body_{name}, {position[0]}, {position[1]}, {position[2]});
	dBodySetLinearVel(body_{name}, 0, 0, 0);
	dBodySetAngularVel(body_{name}, 0, 0, 0);
"""

			result = f'{result}{new_code}'
	
	return result

def draw_bodies():
	result = ""

	#spheres
	if ArmsValue.sphere.value in arms:
		for body in arms[ArmsValue.sphere.value]:
			name = get_required_value(body, ArmsValue.name.value)
			color = get_optional_value(body, ArmsValue.color.value)
			radius = get_required_value(body, ArmsValue.radius.value)

			new_code = f"""
	//Generated by Armature
	dsSetColor({color[0]}, {color[1]}, {color[2]});
	const dReal *SPos_{name} = dBodyGetPosition(body_{name});
	const dReal *SRot_{name} = dBodyGetRotation(body_{name});
	float spos_{name}[3] = {{ SPos_{name}[0], SPos_{name}[1], SPos_{name}[2] }};
	float srot_{name}[12] = {{ SRot_{name}[0], SRot_{name}[1], SRot_{name}[2], SRot_{name}[3], SRot_{name}[4], SRot_{name}[5], SRot_{name}[6], SRot_{name}[7], SRot_{name}[8], SRot_{name}[9], SRot_{name}[10], SRot_{name}[11] }};
	dsDrawSphere
	(
		spos_{name},
		srot_{name},
		{radius}
	);
	"""

			result = f'{result}{new_code}'
	
	#boxes
	if 'box' in arms:
		for body in arms['box']:
			name = get_required_value(body, ArmsValue.name.value)
			color = get_optional_value(body, ArmsValue.color.value)
			sides = get_required_value(body, ArmsValue.sides.value)

			new_code = f"""
	//Generated by Armature
	dsSetColor({color[0]}, {color[1]}, {color[2]});
	dsDrawBox(dBodyGetPosition(body_{name}),
		dBodyGetRotation(body_{name}), sides_{name});
"""

			result = f'{result}{new_code}'

	

	return result

def create_shapes():
	result = ""

	#spheres
	if ArmsValue.sphere.value in arms:
		for body in arms[ArmsValue.sphere.value]:
			name = get_required_value(body, ArmsValue.name.value)
			radius = get_required_value(body, ArmsValue.radius.value)
			position = get_required_value(body, ArmsValue.position.value)

			new_code = f"""
	//Generated by Armature
	//Create Sphere_{name}
	body_{name} = dBodyCreate(world);
	dMassSetSphere(&m, 1, {radius});
	dBodySetMass(body_{name}, &m);
	geom_{name} = dCreateSphere(0, {radius});
	dGeomSetBody(geom_{name}, body_{name});
	dBodySetPosition(body_{name}, {position[0]}, {position[1]}, {position[2]});
	dSpaceAdd(space, geom_{name});
	"""
			result = f'{result}{new_code}'

	#boxes
	if 'box' in arms:
		for body in arms['box']:
			name = get_required_value(body, ArmsValue.name.value)
			sides = get_required_value(body, ArmsValue.sides.value)
			position = get_required_value(body, ArmsValue.position.value)

			new_code = f"""
	//Generated by Armature
	//Create Box_{name}
	body_{name} = dBodyCreate(world);
	geom_{name} = dCreateBox(0, {sides[0]}, {sides[1]}, {sides[2]});
	dGeomSetBody(geom_{name}, body_{name});
	m.setBox(1, 1,1,1);
	dBodySetMass(body_{name}, &m);
	dBodySetPosition(body_{name}, {position[0]}, {position[1]}, {position[2]});
	dSpaceAdd(space, geom_{name});
"""

			result = f'{result}{new_code}'

	return result

def main():

	args = sys.argv

	file_to_parse = None
	where_to_save = None

	if len(args) == 1:
		print("Please give one argument as the ARMS file to parse, and a second, optional, argument as the save location.\n\
		i.e. >python Armature.py my/super/cool/file.arms where/i/want/to/save")
		quit()

	if len(args) > 1:
		file_to_parse = Path(args[1])

	if len(args) > 2:
		where_to_save = Path(f"{args[2]}/{file_to_parse.stem}_ODE.cpp")
	else:
		where_to_save = Path(f"./{file_to_parse.stem}_ODE.cpp")

	global arms
	arms = toml.loads(file_to_parse.read_text())

	template_path = Path("templates/basic_template.txt")
	template_string = template_path.read_text()

	convert_macros()
	convert_constants()

	make_shape_positions_relative_to_parents()
	make_joint_positions_relative_to_parent_shape()

	#pp.pprint(arms)

	if type(arms) is dict:
		where_to_save.write_text(template_string.format(
		create_shapes = create_shapes(),
		draw_bodies = draw_bodies(),
		reset_bodies = reset_bodies(),
		body_variables = body_variables(),
		create_joints = create_joints(),
		create_non_colliding_groups = create_non_colliding_groups())
		)

main()