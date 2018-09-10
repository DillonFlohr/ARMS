import toml
import sys
from pathlib import Path

#parsed as dictionary data from the .arms/toml file
arms = None

def body_variables():
    result = ""

    #Ex.
#   static dBodyID sphbody0;
#   static dGeomID sphgeom0;

#   static dBodyID sphbody1;
#   static dGeomID sphgeom1;


    for body in arms['sphere']:
        new_body = f"""//Gernerated by Armature
static dBodyID body_{body['name']};
static dGeomID geom_{body['name']};
"""
        result = f'{result}{new_body}'

    return result

def reset_bodies():
    #EX.
    # float sx0 = 0.0f, sy0 = 0.00f, sz0 = 5.15;

	# dQuaternion q0;
	# dQSetIdentity(q0);
	# dBodySetPosition(sphbody0, sx0, sy0, sz0);
	# dBodySetQuaternion(sphbody0, q0);
	# dBodySetLinearVel(sphbody0, 0, 0, 0);
	# dBodySetAngularVel(sphbody0, 0, 0, 0);

	# float sx1 = 0.05f, sy1 = 0.01f, sz1 = 7.15;

	# dQuaternion q1;
	# dQSetIdentity(q1);
	# dBodySetPosition(sphbody1, sx1, sy1, sz1);
	# dBodySetQuaternion(sphbody1, q1);
	# dBodySetLinearVel(sphbody1, 0, 0, 0);
	# dBodySetAngularVel(sphbody1, 0, 0, 0);
    result = ""

    for body in arms['sphere']:
        name = body['name']
        position = body['position']

        new_code = f"""
	//Generated by Armature
	float sx{name} = {position[0]}f, sy{name} = {position[1]}f, sz{name} = {position[2]}f;
	dQuaternion q{name};
	dQSetIdentity(q{name});
	dBodySetPosition(body_{name}, sx{name}, sy{name}, sz{name});
	dBodySetQuaternion(body_{name}, q{name});
	dBodySetLinearVel(body_{name}, 0, 0, 0);
	dBodySetAngularVel(body_{name}, 0, 0, 0);
"""

        result = f'{result}{new_code}'
    #print(result)
    return result

def draw_bodies():
    #EX.
    # dsSetColor(1, 0, 1);
	# const dReal *SPos0 = dBodyGetPosition(sphbody0);
	# const dReal *SRot0 = dBodyGetRotation(sphbody0);
	# float spos0[3] = { SPos0[0], SPos0[1], SPos0[2] };
	# float srot0[12] = { SRot0[0], SRot0[1], SRot0[2], SRot0[3], SRot0[4], SRot0[5], SRot0[6], SRot0[7], SRot0[8], SRot0[9], SRot0[10], SRot0[11] };
	# dsDrawSphere
	# (
	# 	spos0,
	# 	srot0,
	# 	RADIUS
	# );

    result = ""

    for body in arms['sphere']:
        name = body['name']
        colors = body['color']
        radius = body['radius']

        new_code = f"""
	//Generated by Armature
	dsSetColor({colors[0]}, {colors[1]}, {colors[2]});
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

    return result

def create_shapes():
    #EX.
    # //Create Sphere0
	# sphbody0 = dBodyCreate(world);
	# dMassSetSphere(&m, 1, RADIUS);
	# dBodySetMass(sphbody0, &m);
	# sphgeom0 = dCreateSphere(0, RADIUS);
	# dGeomSetBody(sphgeom0, sphbody0);
	# dSpaceAdd(space, sphgeom0);

    result = ""

    for body in arms['sphere']:
        name = body['name']
        colors = body['color']
        radius = body['radius']

        new_code = f"""
	//Generated by Armature
	//Create Sphere_{name}
	body_{name} = dBodyCreate(world);
	dMassSetSphere(&m, 1, {radius});
	dBodySetMass(body_{name}, &m);
	geom_{name} = dCreateSphere(0, {radius});
	dGeomSetBody(geom_{name}, body_{name});
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

	template_path = Path("basic_template.txt")
	template_string = template_path.read_text()

	if type(arms) is dict:
		where_to_save.write_text(template_string.format(
		create_shapes = create_shapes(), 
		draw_bodies = draw_bodies(), 
		reset_bodies = reset_bodies(), 
		body_variables = body_variables())
		)

main()