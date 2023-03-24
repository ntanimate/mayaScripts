import maya.cmds as cmds


body_part = 'leg' # body part can be specified

locator_select = cmds.ls(body_part + '*_loc')
	
loc_5 = body_part + '_e_l_loc'
loc_4 = loc_5.replace('_e', '_d')
loc_3 = loc_5.replace('_e', '_c')
loc_2 = loc_5.replace('_e', '_b')
loc_1 = loc_5.replace('_e', '_a')
 

def locator_create():
	
	list_locators = [loc_1, loc_2, loc_3, loc_4, loc_5]
	
	for loc in list_locators:
		cmds.spaceLocator(n = loc)
	
	locator_select = cmds.ls(body_part + '*_loc')
		
	if list_locators == [loc_1, loc_2, loc_3, loc_4, loc_5]:
		print('SUCCESS, locators for ' + body_part.upper() + ' created:' + str(locator_select))    
	else:
		print('WARNING: Recreate locators.')
		
	for locator in locator_select:
		if locator == loc_5:
			cmds.setAttr(loc_5 + '.translateZ', 5)
		elif locator == loc_4:
			cmds.setAttr(loc_4 + '.translateZ', 3)
		elif locator == loc_3:
			cmds.setAttr(loc_3 + '.translateY', 1.2)
		elif locator == loc_2:
			cmds.setAttr(loc_2 + '.translateY', 21)
			cmds.setAttr(loc_2 + '.translateZ', 2)
		elif locator == loc_1:
			cmds.setAttr(loc_1 + '.translateY', 40) 
		cmds.scale(5, 5, 5, locator, absolute = True)

	# Orient locators
	for locator in locator_select:
		if locator in locator_select[0:3]:
			cmds.rotate(90, 0, -90, locator, absolute = True)
		else:
			cmds.rotate(0, -90, 0, locator, absolute = True)

	print('Aligned locators X down and Y up for ' + body_part.upper())


def group_locators():
   locator_select = cmds.ls(body_part + '*_loc')
	
   number_locators = len(locator_select)        

   for lr in range(1, number_locators):    
	   cmds.parent(locator_select[lr], locator_select[lr - 1])
	
   print('ACTION NEEDED: Move locators to ' + body_part + ' position')

# Select groups to move
'''cmds.select(loc_1)
cmds.select(loc_2)
cmds.select(loc_4)
'''


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
	jnts = cmds.ls(body_part + '*_jnt', sl = True, type = 'joint')
	size = len(jnts)
	
	for jr in range(1, size):              # skips the first joint
	   cmds.parent(jnts[jr], jnts[jr - 1]) # parents the 2nd joint to the 1st joint

# Create ik Handles
def create_ikh():   

	locator_select = cmds.ls(body_part + '*_loc')

	#create prefix helper
	top_l_jnt = locator_select[0].split('loc')[0] + 'jnt'
	middle_l_jnt = locator_select[2].split('loc')[0] + 'jnt'
	end_l_jnt = locator_select[3].split('loc')[0] + 'jnt'
	
	# Freeze transform on rotation, create helper script
	
	cmds.makeIdentity(top_l_jnt, apply = True, rotate = True)
	cmds.makeIdentity(middle_l_jnt, apply = True, rotate = True)
	cmds.makeIdentity(end_l_jnt, apply = True, rotate = True)
	
	# Create IK chain for ankle, ball, toe
	
	cmds.select(top_l_jnt, hierarchy = True)
	l_chain = cmds.ls(sl = True)
	end_ankle_jnt = l_chain[-3]
	end_toe_jnt = l_chain[-2]
	end_toe_end_jnt = l_chain[-1]
	
	rpIK_node_ankle = cmds.ikHandle(sol = 'ikRPsolver', startJoint = top_l_jnt, endEffector = end_ankle_jnt)
	scIK_node_foot = cmds.ikHandle(sol = 'ikSCsolver', startJoint = middle_l_jnt, endEffector = end_toe_jnt)
	scIK_node_toe = cmds.ikHandle(sol = 'ikSCsolver', startJoint = end_l_jnt, endEffector = end_toe_end_jnt)
	
	rpIK_ankle = cmds.rename(rpIK_node_ankle[0], (top_l_jnt + '_rpIK'))
	scIK_foot = cmds.rename(scIK_node_foot[0], (middle_l_jnt + '_scIK'))
	scIK_toe = cmds.rename(scIK_node_toe[0], (end_l_jnt + '_scIK'))
	
	rpIK_eff_ankle = cmds.rename(rpIK_node_ankle[1], (top_l_jnt + '_eff'))
	scIK_eff_foot = cmds.rename(scIK_node_foot[1], (middle_l_jnt + '_eff'))
	scIK_eff_toe = cmds.rename(scIK_node_toe[1], (end_l_jnt + '_eff'))
	
	print('SUCCESS, created ik handles for' + ' ankle, ball, toe')

# Hides the locator guides
#cmds.setAttr(locator_select[0] + '.visiblity', 0)

def create_pv():
	cmds.spaceLocator(name = 'pv_l_' + body_part + '_loc')
	pv_pos = cmds.xform(body_part + '_b_l_loc', q=True, ws=True, t=True)
	cmds.xform('pv_l_' + body_part + '_loc', ws=True, t=pv_pos)
	cmds.setAttr('pv_l_' + body_part + '_loc.translateZ', 8) # negative value for arm, positive 8 for leg
	cmds.poleVectorConstraint('pv_l_' + body_part + '_loc', body_part + '_a_l_jnt_rpIK', weight = 1)
	
	print('SUCCESS, created pole vector for ' + body_part.upper())



def rename_jnt():
	leg_jnts = cmds.select('leg_*l_jnt', replace = True)
	for jnt in leg_jnts:
		cmds.rename(jnt, jnt.split('l_jnt'))
		