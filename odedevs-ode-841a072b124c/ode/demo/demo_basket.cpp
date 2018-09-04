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

#define RADIUS 0.20

static dSpaceID space;
static dWorldID world;
static dJointGroupID contactgroup;

static dBodyID sphbody0;
static dGeomID sphgeom0;

static dBodyID sphbody1;
static dGeomID sphgeom1;

void start()
{
	puts("Controls:");
	puts("   SPACE - reset ball(s)");
}

static void reset_ball(void)
{
	float sx0 = 0.0f, sy0 = 0.00f, sz0 = 5.15;

	dQuaternion q0;
	dQSetIdentity(q0);
	dBodySetPosition(sphbody0, sx0, sy0, sz0);
	dBodySetQuaternion(sphbody0, q0);
	dBodySetLinearVel(sphbody0, 0, 0, 0);
	dBodySetAngularVel(sphbody0, 0, 0, 0);

	float sx1 = 0.05f, sy1 = 0.01f, sz1 = 7.15;

	dQuaternion q1;
	dQSetIdentity(q1);
	dBodySetPosition(sphbody1, sx1, sy1, sz1);
	dBodySetQuaternion(sphbody1, q1);
	dBodySetLinearVel(sphbody1, 0, 0, 0);
	dBodySetAngularVel(sphbody1, 0, 0, 0);
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

	dsSetColor(1, 0, 1);
	const dReal *SPos0 = dBodyGetPosition(sphbody0);
	const dReal *SRot0 = dBodyGetRotation(sphbody0);
	float spos0[3] = { SPos0[0], SPos0[1], SPos0[2] };
	float srot0[12] = { SRot0[0], SRot0[1], SRot0[2], SRot0[3], SRot0[4], SRot0[5], SRot0[6], SRot0[7], SRot0[8], SRot0[9], SRot0[10], SRot0[11] };
	dsDrawSphere
	(
		spos0,
		srot0,
		RADIUS
	);

	dsSetColor(1, 0, 0);
	const dReal *SPos1 = dBodyGetPosition(sphbody1);
	const dReal *SRot1 = dBodyGetRotation(sphbody1);
	float spos1[3] = { SPos1[0], SPos1[1], SPos1[2] };
	float srot1[12] = { SRot1[0], SRot1[1], SRot1[2], SRot1[3], SRot1[4], SRot1[5], SRot1[6], SRot1[7], SRot1[8], SRot1[9], SRot1[10], SRot1[11] };
	dsDrawSphere
	(
		spos1,
		srot1,
		RADIUS
	);
}

void command(int c)
{
	switch (c) {
	case ' ':
		reset_ball();
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

	//Create Sphere0
	sphbody0 = dBodyCreate(world);
	dMassSetSphere(&m, 1, RADIUS);
	dBodySetMass(sphbody0, &m);
	sphgeom0 = dCreateSphere(0, RADIUS);
	dGeomSetBody(sphgeom0, sphbody0);
	dSpaceAdd(space, sphgeom0);

	//Create Sphere1
	sphbody1 = dBodyCreate(world);
	dMassSetSphere(&m, 1, RADIUS);
	dBodySetMass(sphbody1, &m);
	sphgeom1 = dCreateSphere(0, RADIUS);
	dGeomSetBody(sphgeom1, sphbody1);
	dSpaceAdd(space, sphgeom1);

	reset_ball();

	// run simulation
	dsSimulationLoop(argc, argv, 640, 480, &fn);

	dJointGroupDestroy(contactgroup);
	dWorldDestroy(world);
	dGeomDestroy(ground);
	dSpaceDestroy(space);

	dCloseODE();
}