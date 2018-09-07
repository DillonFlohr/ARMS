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
	float sxball2 = 0.0f, syball2 = 0.0f, szball2 = 8.0f;
	dQuaternion qball2;
	dQSetIdentity(qball2);
	dBodySetPosition(body_ball2, sxball2, syball2, szball2);
	dBodySetQuaternion(body_ball2, qball2);
	dBodySetLinearVel(body_ball2, 0, 0, 0);
	dBodySetAngularVel(body_ball2, 0, 0, 0);

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


	reset_bodies();

	// run simulation
	dsSimulationLoop(argc, argv, 640, 480, &fn);

	dJointGroupDestroy(contactgroup);
	dWorldDestroy(world);
	dGeomDestroy(ground);
	dSpaceDestroy(space);

	dCloseODE();
}

