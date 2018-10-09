try:
	import toml
except:
	print("\n**************************************\nPlease install toml to use Armature.py\n> pip install toml\n**************************************\n")
	quit()
import sys
import pprint
from pathlib import Path
from enum import Enum

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
	'sphere': 0,
	'joint': 0
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
			print(f"Error: Something is missing a name.")
		quit()

def get_constant(target_var):
	result = None
	if ArmsValue.constants.value in arms:
		constants = arms[ArmsValue.constants.value][0]
		for var in constants:
			if var == target_var:
				result = constants[var]
	
	if result != None:
		return result
	else:
		print(f"Constant name {target_var} does not exist. \nExiting the program.")
		quit()

def convert_constants():
	global arms
	for shape in shapes:
		if shape in arms:
			for items in arms[shape]:
				for key in items:
					if type(items[key]) == str:
						if (items[key][0] == "$"):
							items[key] = get_constant(items[key][1:])
					if type(items[key]) == list:
						for i in range(0, len(items[key])):
							if type(items[key][i]) == str:
								if (items[key][i][0] == "$"):
									items[key][i] = get_constant(items[key][i][1:])

#Recursively set the position of parent's children, then do the same for the children's children
def convert_positions(parent_name, parent_tree, is_root):
	this_parent_position = get_shape_by_name(parent_name)['position']
	for child in parent_tree:
		this_child_position = get_shape_by_name(child)['position']
		this_child_position[0] += this_parent_position[0]
		this_child_position[1] += this_parent_position[1]
		this_child_position[2] += this_parent_position[2]
		convert_positions(child, parent_tree[child], False)


# A shape is a root unless there is a joint with that shape as a child
def shape_is_root(shape_name):
	is_root = True
	if 'joint' in arms:
		for joint in arms['joint']:
			if (joint['child'] == shape_name):
				is_root = False
	return is_root

#Recursively get the children of some parent shape
def get_children_of(parent_name):
	result = {}
	if 'joint' in arms:
		for joint in arms['joint']:
			if (joint['parent'] == parent_name):
				result[joint['child']] = get_children_of(joint['child'])

	return result

def make_positions_relative_to_parents():
	#tree of parents and children
	ancestor_tree = {}

	#Get all the roots
	for shape_type in shapes:
		if shape_type in arms and shape_type != 'joint':
			for shape in arms[shape_type]:
				if (shape_is_root(shape[ArmsValue.name.value])):
					ancestor_tree[shape[ArmsValue.name.value]] = {}

	for root in ancestor_tree:
		ancestor_tree[root] = get_children_of(root)

	for root in ancestor_tree:
		convert_positions(root, ancestor_tree[root], True)

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

	if 'joint' in arms:
		for joint in arms['joint']:
			joint_name = get_required_value(joint, ArmsValue.name.value)
			if get_required_value(joint, ArmsValue.joint_type.value) == 'ball':
				#get parent and child
				parent = get_shape_by_name(get_required_value(joint, ArmsValue.parent.value))
				child = get_shape_by_name(get_required_value(joint, ArmsValue.child.value))
				#get their positions and names
				parent_position = get_required_value(parent, ArmsValue.position.value)
				parent_name = get_required_value(parent, ArmsValue.name.value)
				child_position = get_required_value(child, ArmsValue.position.value)
				child_name = get_required_value(child, ArmsValue.name.value)
				#set ball joint axis to middle of parent and child
				axis_x = (parent_position[0] + child_position[0])/2
				axis_y = (parent_position[1] + child_position[1])/2
				axis_z = (parent_position[2] + child_position[2])/2

				new_joint = f"""//Generated by Armature
	dJointID {joint_name} = dJointCreateBall(world, 0);
	dJointAttach({joint_name}, body_{parent_name}, body_{child_name});
	dJointSetBallAnchor({joint_name}, {axis_x}, {axis_y}, {axis_z});
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
	dBodySetPosition(body_{name}, {position[0]}f, {position[1]}f, {position[2]}f);
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
	dBodySetPosition(body_{name}, {position[0]}f, {position[1]}f, {position[2]}f);
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

	convert_constants()

	make_positions_relative_to_parents()

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