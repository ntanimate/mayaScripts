import maya.cmds as cmds

import os

body_part = 'arm' # body part can be specified

locator_select = cmds.ls(body_part + '*_loc')
	
loc_3 = body_part + '_c_l_loc'
loc_2 = loc_3.replace('_c', '_b')
loc_1 = loc_3.replace('_c', '_a')

 

def locator_create():
	
	list_locators = [loc_1, loc_2, loc_3]
	
	for loc in list_locators:
		cmds.spaceLocator(n = loc)
	
	locator_select = cmds.ls(body_part + '*_loc')
		
	if list_locators == [loc_1, loc_2, loc_3]:
		print('SUCCESS, locators for ' + body_part.upper() + ' created:' + str(locator_select))    
	else:
		print('WARNING: Recreate locators.')

	# Start position for locators
	for locator in locator_select:
		if locator == loc_3:
			cmds.setAttr(loc_3 + '.translateY', 1.2)
		elif locator == loc_2:
			cmds.setAttr(loc_2 + '.translateY', 21.2)
			cmds.setAttr(loc_2 + '.translateZ', 2)
		elif locator == loc_1:
			cmds.setAttr(loc_1 + '.translateY', 40) 
		cmds.scale(5, 5, 5, locator, absolute = True)
	
	# Orient locators
	for locator in locator_select:
		if locator in locator_select[0:3]:
			cmds.rotate(-90, 0, -90, locator, absolute = True)

	print('Aligned locators X down and Y up for ' + body_part.upper())

def group_locators():
   locator_select = cmds.ls(body_part + '*_loc')
	
   number_locators = len(locator_select)        

   for lr in range(1, number_locators):    
	   cmds.parent(locator_select[lr], locator_select[lr - 1])
  
   print('ACTION NEEDED: Move locators to ' + body_part + ' position')

   cmds.setAttr(locator_select[0] + '.rotateZ', -25)
   cmds.setAttr(locator_select[0] + '.rotateX', -2)

def create_joints():

	action = cmds.confirmDialog(title = 'ACTION NEEDED',
						message = 'Did you align the locators to the model ' + body_part + ' location' + '?',
						button = ['Yes', 'No'],
						cancelButton = 'No')

	if action == 'Yes':
		
	   locator_select = cmds.ls(body_part + '*_loc')
	   for locator in locator_select: 
		   prefix = locator.split('loc')
		   cmds.select(cl = True)
		   jnt = cmds.joint(n = prefix[0] + 'jnt')
		   cmds.delete(cmds.parentConstraint(locator, jnt))
		
		   print('SUCCESS, created joints for ' + body_part.upper())
	else:
		print('Your model will not line up with the joints. Please move locator before adding joints.')


	

def parent_joints():
	cmds.select(body_part + '*jnt', replace = True)
	jnts = cmds.ls(body_part + '*jnt', sl = True, type = 'joint')
	size = len(jnts)
	
	for jr in range(1, size):              # skips the first joint
	   cmds.parent(jnts[jr], jnts[jr - 1]) # parents the 2nd joint to the 1st joint

# Create ik Handles

def create_ikh():
	locator_select = cmds.ls(body_part + '*_loc')

	top_l_jnt = locator_select[0].split('loc')[0] + 'jnt'
	
	
	# Freeze transform on rotation
	
	cmds.makeIdentity(top_l_jnt, apply = True, rotate = True)
	
	
	# Create IK chain for ankle, ball, toe
	top_l_jnt = locator_select[0].split('loc')[0] + 'jnt'

	cmds.select(top_l_jnt, hierarchy = True)

	l_chain = cmds.ls(sl = True)

	end_elbow_jnt = l_chain[-1]
	
	
	rpIK_node_elbow = cmds.ikHandle(sol = 'ikRPsolver', startJoint = top_l_jnt, endEffector = end_elbow_jnt)
	
	
	rpIK_elbow = cmds.rename(rpIK_node_elbow[0], (top_l_jnt + '_rpIK'))
	
	
	rpIK_eff_elbow = cmds.rename(rpIK_node_elbow[1], (top_l_jnt + '_eff'))
	
	print('SUCCESS, created ik handles for' + ' arm')

# Hides the locator guides
#cmds.setAttr(locator_select[0] + '.visiblity', 0)

def create_pv():
	cmds.spaceLocator(name = 'pv_l_' + body_part + '_loc')
	pv_pos = cmds.xform(body_part + '_b_l_loc', q=True, ws=True, t=True)
	cmds.xform('pv_l_' + body_part + '_loc', ws=True, t=pv_pos)
	cmds.setAttr('pv_l_' + body_part + '_loc.translateZ', -15) # negative value for arm, positive 8 for leg
	cmds.poleVectorConstraint('pv_l_' + body_part + '_loc', body_part + '_a_l_jnt_rpIK', weight = 1)
	
	print('SUCCESS, created pole vector for ' + body_part.upper())



