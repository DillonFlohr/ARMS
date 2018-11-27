from Interfaces import IArmsCreator
from Helpers import ArmsHelper as ah

from pathlib import Path
import re
import pdb

shapes = ah.shapes
joints = ah.joints
ArmsValue = ah.ArmsValue

class SdfCreator(IArmsCreator.IArmsCreator):
    def __init__(self):
        self.__arms = None
        self.__models = None

    @property
    def file_extension(self):
        return ".sdf"

    def can_create(self, fileType):
        return re.search('--sdf', fileType, re.I) != None

    def create_file(self, armsDict):
        self.__arms = armsDict

        template_path = Path("Creators/templates/flat_world.sdf")
        template_string = template_path.read_text()

        self.__create_models()

        return template_string.format(
            models = self.__models
        )

    def __create_models(self):
        for group_of_things in self.__arms:
            if group_of_things in shapes:
                for thing in self.__arms[group_of_things]:
                    #link variables
                    name = ah.get_required_value(thing, ArmsValue.name.value)
                    position = thing[ArmsValue.position.value]
                    if ah.shape_is_root(name, self.__arms):
                        new_model = f"""
    <model name='model_{name}'>
        {self.__create_link_text(thing)}
        {self.__create_joints_from(name)}
        {self.__create_child_links(ah.get_children_of(thing[ArmsValue.name.value], self.__arms))}
    </model>
    """
                        self.__models = f'{self.__models}{new_model}'

    def __create_child_links(self, children, result = ""):
        for shape in children:
            result = f'{result}{self.__create_link_text(ah.get_shape_by_name(shape, self.__arms))}'
            result = f'{result}{self.__create_joints_from(shape)}'
            result = f'{result}{self.__create_child_links(children[shape])}'

        return result

    #Creates all the joints that are from some shape.
    def __create_joints_from(self, shape_name):
        result = ""

        shape_joints = {}

        for group in self.__arms:
            if group in joints:
                shape_joints[group] = []
                for joint in self.__arms[group]:
                    if joint['parent'] == shape_name:
                        shape_joints[group].append(joint)
        for group in shape_joints:
            for joint in shape_joints[group]:
		#TODO: change to get_required_value and pass in joint
                parent_position = ah.get_shape_by_name(joint['parent'], self.__arms)['position']
                child_position = ah.get_shape_by_name(joint['child'], self.__arms)['position']
                axis = ah.get_optional_value(joint, 'axis')
                position = joint['relative_position']
                
                ###########################################################################################
                # Gazebo parses the joints pose from the child link. Hence the [Parent - Child + position]#
                # This puts the joint's position in the right place relative to the parent.               #
                ###########################################################################################
                result = f"""{result}
    <joint name='{joint['name']}' type='{group}'>
      <parent>{joint['parent']}</parent>
      <child>{joint['child']}</child>
      <pose frame=''>{parent_position[0] - child_position[0] + position[0]} {parent_position[1] - child_position[1] + position[1]} {parent_position[2] - child_position[2] + position[2]} 0 -0 0</pose>
      <axis>
        <xyz>{axis[0]} {axis[1]} {axis[2]}</xyz>
        <use_parent_model_frame>0</use_parent_model_frame>
        <limit>
          <lower>-1.79769e+308</lower>
          <upper>1.79769e+308</upper>
          <effort>-1</effort>
          <velocity>-1</velocity>
        </limit>
        <dynamics>
          <spring_reference>0</spring_reference>
          <spring_stiffness>0</spring_stiffness>
          <damping>0</damping>
          <friction>0</friction>
        </dynamics>
      </axis>
      <physics>
        <ode>
          <limit>
            <cfm>0</cfm>
            <erp>0.2</erp>
          </limit>
          <suspension>
            <cfm>0</cfm>
            <erp>0.2</erp>
          </suspension>
        </ode>
      </physics>
    </joint>
        """

        return result

    def __create_link_text(self, shape):
        name = ah.get_required_value(shape, ArmsValue.name.value)
        position = shape[ArmsValue.position.value]
        if ArmsValue.radius.value in shape:
            shape_type = "sphere"
            radius = ah.get_required_value(shape, ArmsValue.radius.value)
            size = f"<radius>{radius}</radius>"
        elif ArmsValue.sides.value in shape:
            shape_type = "box"
            sides = ah.get_required_value(shape, ArmsValue.sides.value)
            size = f"<size>{sides[0]} {sides[1]} {sides[2]}</size>"
        
        return f"""
        <link name='{name}'>
            <inertial>
                <mass>1</mass>
                <inertia>
                    <ixx>0.1</ixx>
                    <ixy>0</ixy>
                    <ixz>0</ixz>
                    <iyy>0.1</iyy>
                    <iyz>0</iyz>
                    <izz>0.1</izz>
                </inertia>
            </inertial>
            <pose frame=''>{position[0]} {position[1]} {position[2]} 0 -0 0</pose>
            <collision name='collision'>
                <geometry>
                    <{shape_type}>
                        {size}
                    </{shape_type}>
                </geometry>
                <max_contacts>10</max_contacts>
                <surface>
                    <contact>
                        <ode/>
                    </contact>
                    <bounce/>
                    <friction>
                        <torsional>
                            <ode/>
                        </torsional>
                        <ode/>
                    </friction>
                </surface>
            </collision>
            <visual name='visual'>
                <geometry>
                    <{shape_type}>
                        {size}
                    </{shape_type}>
                </geometry>
                <material>
                    <script>
                        <name>Gazebo/White</name>
                        <uri>file://media/materials/scripts/gazebo.material</uri>
                    </script>
                </material>
            </visual>
            <self_collide>0</self_collide>
            <kinematic>0</kinematic>
        </link>
        """
