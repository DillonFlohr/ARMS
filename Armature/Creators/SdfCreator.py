from Interfaces import IArmsCreator
from Helpers import ArmsHelper as ah

from pathlib import Path
import re

shapes = ah.shapes
joints = ah.joints
ArmsValue = ah.ArmsValue

class SdfCreator(IArmsCreator.IArmsCreator):
    def __init__(self):
        self.__arms = None

    @property
    def file_extension(self):
        return ".sdf"

    def CanCreate(self, fileType):
        return re.search('--sdf', fileType, re.I) != None

    def CreateFile(self, armsDict):
        self.__arms = armsDict

        template_path = Path("Creators/templates/flat_world.sdf")
        template_string = template_path.read_text()

        return template_string.format(
            models = self.__create_models()
        )

    def __create_models(self):
        result = ""

        for group_of_things in self.__arms:
            if group_of_things in shapes:
                for thing in self.__arms[group_of_things]:
                    #link variables
                    name = thing[ArmsValue.name.value]
                    position = thing[ArmsValue.position.value]
                    radius = None
                    sides = None
                    if group_of_things == 'sphere':
                        radius = ah.get_required_value(thing, ArmsValue.radius.value)
                        size = f"<radius>{radius}</radius>"
                    elif group_of_things == 'box':
                        sides = ah.get_required_value(thing, ArmsValue.sides.value)
                        size = f"<size>{sides[0]} {sides[1]} {sides[2]}</size>"
                    if ah.shape_is_root(thing, self.__arms):
                        new_model = f"""
    <model name='{name}_model'>
        <pose frame=''>{position[0]} {position[1]} {position[2]} 0 -0 0</pose>
        <link name='source_{name}'>
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
            <collision name='collision'>
                <geometry>
                    <{group_of_things}>
                        {size}
                    </{group_of_things}>
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
                    <{group_of_things}>
                        {size}
                    </{group_of_things}>
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
    </model>
    """
                    result = f'{result}{new_model}'
        return result
