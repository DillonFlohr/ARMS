/*************************************************************************
 *                                                                       *
 * Open Dynamics Engine, Copyright (C) 2001,2002 Russell L. Smith.       *
 * All rights reserved.  Email: russ@q12.org   Web: www.q12.org          *
 *                                                                       *
 * This library is free software; you can redistribute it and/or         *
 * modify it under the terms of EITHER:                                  *
 *   (1) The GNU Lesser General Public License as published by the Free  *
 *       Software Foundation; either version 2.1 of the License, or (at  *
 *       your option) any later version. The text of the GNU Lesser      *
 *       General Public License is included with this library in the     *
 *       file LICENSE.TXT.                                               *
 *   (2) The BSD-style license that is included with this library in     *
 *       the file LICENSE-BSD.TXT.                                       *
 *                                                                       *
 * This library is distributed in the hope that it will be useful,       *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the files    *
 * LICENSE.TXT and LICENSE-BSD.TXT for more details.                     *
 *                                                                       *
 *************************************************************************/

#include <vector>
#include <ode/ode.h>
#include <drawstuff/drawstuff.h>
#include "texturepath.h"

#ifdef dDOUBLE
#define dsDrawBox dsDrawBoxD
#endif

static dSpaceID space;
static dWorldID world;
static dJointGroupID contactgroup;

//Gernerated by Armature
static dBodyID body_ball1;
static dGeomID geom_ball1;
//Gernerated by Armature
static dBodyID body_ball2;
static dGeomID geom_ball2;
//Gernerated by Armature
static dBodyID body_ball23;
static dGeomID geom_ball23;
//Gernerated by Armature
static dBodyID body_ball24;
static dGeomID geom_ball24;
//Gernerated by Armature
static dBodyID body_ball25;
static dGeomID geom_ball25;
//Gernerated by Armature
static dBodyID body_ball26;
static dGeomID geom_ball26;
//Gernerated by Armature
static dBodyID body_ball27;
static dGeomID geom_ball27;

dBodyID body;
dGeomID geom;
const float sides[3] = { 1,1,1 };


void start()
{
	puts("Controls:");
	puts("   SPACE - reset bodies");
}

static void reset_bodies(void)
{

	//Generated by Armature
	float sxball1 = 0.2f, syball1 = 0.0f, szball1 = 5.0f;
	dQuaternion qball1;
	dQSetIdentity(qball1);
	dBodySetPosition(body_ball1, sxball1, syball1, szball1);
	dBodySetQuaternion(body_ball1, qball1);
	dBodySetLinearVel(body_ball1, 0, 0, 0);
	dBodySetAngularVel(body_ball1, 0, 0, 0);

	//Generated by Armature
	float sxball2 = 0.0f, syball2 = 0.3f, szball2 = 8.0f;
	dQuaternion qball2;
	dQSetIdentity(qball2);
	dBodySetPosition(body_ball2, sxball2, syball2, szball2);
	dBodySetQuaternion(body_ball2, qball2);
	dBodySetLinearVel(body_ball2, 0, 0, 0);
	dBodySetAngularVel(body_ball2, 0, 0, 0);

	//Generated by Armature
	float sxball23 = 0.0f, syball23 = 0.4f, szball23 = 18.0f;
	dQuaternion qball23;
	dQSetIdentity(qball23);
	dBodySetPosition(body_ball23, sxball23, syball23, szball23);
	dBodySetQuaternion(body_ball23, qball23);
	dBodySetLinearVel(body_ball23, 0, 0, 0);
	dBodySetAngularVel(body_ball23, 0, 0, 0);

	//Generated by Armature
	float sxball24 = 0.0f, syball24 = -0.2f, szball24 = 2.0f;
	dQuaternion qball24;
	dQSetIdentity(qball24);
	dBodySetPosition(body_ball24, sxball24, syball24, szball24);
	dBodySetQuaternion(body_ball24, qball24);
	dBodySetLinearVel(body_ball24, 0, 0, 0);
	dBodySetAngularVel(body_ball24, 0, 0, 0);

	//Generated by Armature
	float sxball25 = 0.0f, syball25 = -0.1f, szball25 = 15.0f;
	dQuaternion qball25;
	dQSetIdentity(qball25);
	dBodySetPosition(body_ball25, sxball25, syball25, szball25);
	dBodySetQuaternion(body_ball25, qball25);
	dBodySetLinearVel(body_ball25, 0, 0, 0);
	dBodySetAngularVel(body_ball25, 0, 0, 0);

	//Generated by Armature
	float sxball26 = 0.2f, syball26 = 0.0f, szball26 = 12.0f;
	dQuaternion qball26;
	dQSetIdentity(qball26);
	dBodySetPosition(body_ball26, sxball26, syball26, szball26);
	dBodySetQuaternion(body_ball26, qball26);
	dBodySetLinearVel(body_ball26, 0, 0, 0);
	dBodySetAngularVel(body_ball26, 0, 0, 0);

	//Generated by Armature
	float sxball27 = 0.0f, syball27 = 0.0f, szball27 = 10.0f;
	dQuaternion qball27;
	dQSetIdentity(qball27);
	dBodySetPosition(body_ball27, sxball27, syball27, szball27);
	dBodySetQuaternion(body_ball27, qball27);
	dBodySetLinearVel(body_ball27, 0, 0, 0);
	dBodySetAngularVel(body_ball27, 0, 0, 0);

}

static void nearCallback(void *, dGeomID o1, dGeomID o2)
{
	// exit without doing anything if the two bodies are connected by a joint
	dBodyID b1 = dGeomGetBody(o1);
	dBodyID b2 = dGeomGetBody(o2);

	const int MAX_CONTACTS = 8;
	dContact contact[MAX_CONTACTS];

	int numc = dCollide(o1, o2, MAX_CONTACTS,
		&contact[0].geom,
		sizeof(dContact));

	for (int i = 0; i < numc; i++) {
		contact[i].surface.mode = dContactSoftERP | dContactSoftCFM | dContactApprox1 | dContactSlip1 | dContactSlip2;
		contact[i].surface.mu = 50.0; // was: dInfinity
		contact[i].surface.soft_erp = 0.96;
		contact[i].surface.soft_cfm = 2.00;
		dJointID c = dJointCreateContact(world, contactgroup, contact + i);
		dJointAttach(c, b1, b2);
	}
}

void simLoop(int pause)
{
	if (!pause) {
		dSpaceCollide(space, 0, &nearCallback);
		dWorldQuickStep(world, 0.01);
		dJointGroupEmpty(contactgroup);
	}


	//Generated by Armature
	dsSetColor(1.0, 0.0, 0.0);
	const dReal *SPos_ball1 = dBodyGetPosition(body_ball1);
	const dReal *SRot_ball1 = dBodyGetRotation(body_ball1);
	float spos_ball1[3] = { SPos_ball1[0], SPos_ball1[1], SPos_ball1[2] };
	float srot_ball1[12] = { SRot_ball1[0], SRot_ball1[1], SRot_ball1[2], SRot_ball1[3], SRot_ball1[4], SRot_ball1[5], SRot_ball1[6], SRot_ball1[7], SRot_ball1[8], SRot_ball1[9], SRot_ball1[10], SRot_ball1[11] };
	dsDrawSphere
	(
		spos_ball1,
		srot_ball1,
		0.5
	);

	//Generated by Armature
	dsSetColor(0.0, 0.0, 1.0);
	const dReal *SPos_ball2 = dBodyGetPosition(body_ball2);
	const dReal *SRot_ball2 = dBodyGetRotation(body_ball2);
	float spos_ball2[3] = { SPos_ball2[0], SPos_ball2[1], SPos_ball2[2] };
	float srot_ball2[12] = { SRot_ball2[0], SRot_ball2[1], SRot_ball2[2], SRot_ball2[3], SRot_ball2[4], SRot_ball2[5], SRot_ball2[6], SRot_ball2[7], SRot_ball2[8], SRot_ball2[9], SRot_ball2[10], SRot_ball2[11] };
	dsDrawSphere
	(
		spos_ball2,
		srot_ball2,
		0.5
	);

	//Generated by Armature
	dsSetColor(0.0, 0.0, 1.0);
	const dReal *SPos_ball23 = dBodyGetPosition(body_ball23);
	const dReal *SRot_ball23 = dBodyGetRotation(body_ball23);
	float spos_ball23[3] = { SPos_ball23[0], SPos_ball23[1], SPos_ball23[2] };
	float srot_ball23[12] = { SRot_ball23[0], SRot_ball23[1], SRot_ball23[2], SRot_ball23[3], SRot_ball23[4], SRot_ball23[5], SRot_ball23[6], SRot_ball23[7], SRot_ball23[8], SRot_ball23[9], SRot_ball23[10], SRot_ball23[11] };
	dsDrawSphere
	(
		spos_ball23,
		srot_ball23,
		0.4
	);

	//Generated by Armature
	dsSetColor(1.0, 1.0, 0.0);
	const dReal *SPos_ball24 = dBodyGetPosition(body_ball24);
	const dReal *SRot_ball24 = dBodyGetRotation(body_ball24);
	float spos_ball24[3] = { SPos_ball24[0], SPos_ball24[1], SPos_ball24[2] };
	float srot_ball24[12] = { SRot_ball24[0], SRot_ball24[1], SRot_ball24[2], SRot_ball24[3], SRot_ball24[4], SRot_ball24[5], SRot_ball24[6], SRot_ball24[7], SRot_ball24[8], SRot_ball24[9], SRot_ball24[10], SRot_ball24[11] };
	dsDrawSphere
	(
		spos_ball24,
		srot_ball24,
		0.5
	);

	//Generated by Armature
	dsSetColor(0.0, 1.0, 1.0);
	const dReal *SPos_ball25 = dBodyGetPosition(body_ball25);
	const dReal *SRot_ball25 = dBodyGetRotation(body_ball25);
	float spos_ball25[3] = { SPos_ball25[0], SPos_ball25[1], SPos_ball25[2] };
	float srot_ball25[12] = { SRot_ball25[0], SRot_ball25[1], SRot_ball25[2], SRot_ball25[3], SRot_ball25[4], SRot_ball25[5], SRot_ball25[6], SRot_ball25[7], SRot_ball25[8], SRot_ball25[9], SRot_ball25[10], SRot_ball25[11] };
	dsDrawSphere
	(
		spos_ball25,
		srot_ball25,
		0.6
	);

	//Generated by Armature
	dsSetColor(1.0, 0.0, 1.0);
	const dReal *SPos_ball26 = dBodyGetPosition(body_ball26);
	const dReal *SRot_ball26 = dBodyGetRotation(body_ball26);
	float spos_ball26[3] = { SPos_ball26[0], SPos_ball26[1], SPos_ball26[2] };
	float srot_ball26[12] = { SRot_ball26[0], SRot_ball26[1], SRot_ball26[2], SRot_ball26[3], SRot_ball26[4], SRot_ball26[5], SRot_ball26[6], SRot_ball26[7], SRot_ball26[8], SRot_ball26[9], SRot_ball26[10], SRot_ball26[11] };
	dsDrawSphere
	(
		spos_ball26,
		srot_ball26,
		0.8
	);

	//Generated by Armature
	dsSetColor(0.0, 0.0, 1.0);
	const dReal *SPos_ball27 = dBodyGetPosition(body_ball27);
	const dReal *SRot_ball27 = dBodyGetRotation(body_ball27);
	float spos_ball27[3] = { SPos_ball27[0], SPos_ball27[1], SPos_ball27[2] };
	float srot_ball27[12] = { SRot_ball27[0], SRot_ball27[1], SRot_ball27[2], SRot_ball27[3], SRot_ball27[4], SRot_ball27[5], SRot_ball27[6], SRot_ball27[7], SRot_ball27[8], SRot_ball27[9], SRot_ball27[10], SRot_ball27[11] };
	dsDrawSphere
	(
		spos_ball27,
		srot_ball27,
		0.3
	);

	dsDrawBox(dBodyGetPosition(body),
		dBodyGetRotation(body), sides);

}

void command(int c)
{
	switch (c) {
	case ' ':
		reset_bodies();
		break;
	}
}

int main(int argc, char **argv)
{
	dMass m;

	dInitODE();

	// setup pointers to drawstuff callback functions
	dsFunctions fn;
	fn.version = DS_VERSION;
	fn.start = &start;
	fn.step = &simLoop;
	fn.command = &command;
	fn.stop = 0;
	fn.path_to_textures = DRAWSTUFF_TEXTURE_PATH;

	//Create world
	world = dWorldCreate();
	dWorldSetGravity(world, 0, 0, -0.98);
	dWorldSetQuickStepNumIterations(world, 50); // <-- increase for more stability

	//Create 'ground'
	space = dSimpleSpaceCreate(0);
	contactgroup = dJointGroupCreate(0);
	dGeomID ground = dCreatePlane(space, 0, 0, 1, 0);


	//Generated by Armature
	//Create Sphere_ball1
	body_ball1 = dBodyCreate(world);
	dMassSetSphere(&m, 1, 0.5);
	dBodySetMass(body_ball1, &m);
	geom_ball1 = dCreateSphere(0, 0.5);
	dGeomSetBody(geom_ball1, body_ball1);
	dSpaceAdd(space, geom_ball1);

	//Generated by Armature
	//Create Sphere_ball2
	body_ball2 = dBodyCreate(world);
	dMassSetSphere(&m, 1, 0.5);
	dBodySetMass(body_ball2, &m);
	geom_ball2 = dCreateSphere(0, 0.5);
	dGeomSetBody(geom_ball2, body_ball2);
	dSpaceAdd(space, geom_ball2);

	//Generated by Armature
	//Create Sphere_ball23
	body_ball23 = dBodyCreate(world);
	dMassSetSphere(&m, 1, 0.4);
	dBodySetMass(body_ball23, &m);
	geom_ball23 = dCreateSphere(0, 0.4);
	dGeomSetBody(geom_ball23, body_ball23);
	dSpaceAdd(space, geom_ball23);

	//Generated by Armature
	//Create Sphere_ball24
	body_ball24 = dBodyCreate(world);
	dMassSetSphere(&m, 1, 0.5);
	dBodySetMass(body_ball24, &m);
	geom_ball24 = dCreateSphere(0, 0.5);
	dGeomSetBody(geom_ball24, body_ball24);
	dSpaceAdd(space, geom_ball24);

	//Generated by Armature
	//Create Sphere_ball25
	body_ball25 = dBodyCreate(world);
	dMassSetSphere(&m, 1, 0.6);
	dBodySetMass(body_ball25, &m);
	geom_ball25 = dCreateSphere(0, 0.6);
	dGeomSetBody(geom_ball25, body_ball25);
	dSpaceAdd(space, geom_ball25);

	//Generated by Armature
	//Create Sphere_ball26
	body_ball26 = dBodyCreate(world);
	dMassSetSphere(&m, 1, 0.8);
	dBodySetMass(body_ball26, &m);
	geom_ball26 = dCreateSphere(0, 0.8);
	dGeomSetBody(geom_ball26, body_ball26);
	dSpaceAdd(space, geom_ball26);

	//Generated by Armature
	//Create Sphere_ball27
	body_ball27 = dBodyCreate(world);
	dMassSetSphere(&m, 1, 0.3);
	dBodySetMass(body_ball27, &m);
	geom_ball27 = dCreateSphere(0, 0.3);
	dGeomSetBody(geom_ball27, body_ball27);
	dSpaceAdd(space, geom_ball27);

	body = dBodyCreate(world);
	geom = dCreateBox(space, 1,1,1);
	dGeomSetBody(geom, body);
	dMass mass;
	mass.setBox(1, 1,1,1);
	dBodySetMass(body, &mass);


	reset_bodies();

	// run simulation
	dsSimulationLoop(argc, argv, 640, 480, &fn);

	dJointGroupDestroy(contactgroup);
	dWorldDestroy(world);
	dGeomDestroy(ground);
	dSpaceDestroy(space);

	dCloseODE();
}