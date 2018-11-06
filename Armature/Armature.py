try:
	import toml
except:
	print("\n**************************************\n\
Please install toml to use Armature.py\n\
> pip install toml\n\
**************************************\n")
	quit()
import sys
import pprint as pp
from pathlib import Path
from enum import Enum
import copy
import getopt

from Providers import ArmsCreatorProvider
from Helpers import ArmsHelper as ah

shapes = ah.shapes
joints = ah.joints
ArmsValue = ah.ArmsValue

#parsed as dictionary data from the .arms/toml file
arms = None

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
					#check if item type is a shape or joint
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
					#otherwise it is a parameter of a macro
					else:
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
	this_parent_position = ah.get_required_value(ah.get_shape_by_name(parent_name, arms), 'position')
	for child in parent_tree:
		this_child = ah.get_shape_by_name(child, arms)
		this_child['position'] = [0, 0, 0]
		this_child_relative_position = ah.get_required_value(this_child, 'relative_position')
		this_child['position'][0] = this_parent_position[0] + this_child_relative_position[0]
		this_child['position'][1] = this_parent_position[1] + this_child_relative_position[1]
		this_child['position'][2] = this_parent_position[2] + this_child_relative_position[2]
		convert_shape_positions(child, parent_tree[child])

def make_joint_positions_relative_to_parent_shape():
	for joint_type in joints:
		if joint_type in arms:
			for joint in arms[joint_type]:
				parent = ah.get_required_value(joint, 'parent')
				parent_position = ah.get_required_value(ah.get_shape_by_name(parent, arms), 'position')
				joint['position'] = [0, 0, 0]
				joint_relative_position = ah.get_required_value(joint, 'relative_position')
				joint['position'][0] = parent_position[0] + joint_relative_position[0]
				joint['position'][1] = parent_position[1] + joint_relative_position[1]
				joint['position'][2] = parent_position[2] + joint_relative_position[2]

def main():
	args = sys.argv
	#options supported by Armature
	long_options = ["drawstuff"] #"sdf"]

	#Get all the options, if there is an invalid option, quit
	try:
		opts, args = getopt.gnu_getopt(sys.argv, "", long_options)
	except getopt.GetoptError as e:
		print(e)
		quit()

	file_to_parse = None
	where_to_save = None

	#If not input file was given
	if len(args) == 1:
		print("\
Please give one argument as the ARMS file to parse, and a second, optional, argument as the save location.\n\
\ni.e. >python Armature.py my/super/cool/file.arms where/i/want/to/save")
		quit()
	else:
		file_to_parse = Path(args[1])

	#If no options are given, ask for them
	if len(opts) < 1:
		print("\
Please give options to select the type of file you'd like Armature to produce.\n\
\ni.e. >python Armature.py --drawstuff my/super/cool/file.arms where/i/want/to/save\n\
\nSupported Files:\n\
--drawstuff (.cpp file that you can use with the ODE demos)\n")
		quit()

	#Translate the ARMS syntax into a dictionary
	global arms
	arms = toml.loads(file_to_parse.read_text())

	convert_macros()
	convert_constants()

	make_shape_positions_relative_to_parents()
	make_joint_positions_relative_to_parent_shape()

	#Get all the creators
	creators = ArmsCreatorProvider.AllArmsCreators()

	#For every option 
	for opt in opts:
		opt = opt[0]
		for creator in creators:
			#Write to a file if creator was requested in the command line options
			if creator.CanCreate(opt):
				#Get the save location
				if len(args) > 2:
					where_to_save = Path(f"{args[2]}/{file_to_parse.stem}{creator.file_extension}")
				else:
					where_to_save = Path(f"./{file_to_parse.stem}{creator.file_extension}")
				where_to_save.write_text(creator.CreateFile(arms))

main()