
# mayaScripts

<details><summary>READ ME</summary>
<p>

PURPOSE:
These scripts were created using version Maya 2022 and Python 3. I am a beginner coder and 3D animator so any feedback is welcome. These scripts have helped me with faster workflows in my classes. All scripts can be middle mouse dragged and converted into shelf buttons for easy access.

GOALS:
As an aspiring TD in production or gaming I took classes through CGMA to learn Maya and other 3D animation software. The code is heavily commented because they are intended as tools for animation or modeling students who do not typically look at the MEL or python script editor. I created small scripts with the intent of solving a few challenges I faced in Maya as well as optimizing the workflow for modelers and animators:

GOAL 1: As a beginner, the Maya interface has a lot of new tools. An example is the image plane which you cannot pull up by searching the help menu in Maya. I created the front facing camera view image plane script so I wouldn't have to remember where the image plane button is located. <b>This will help me or other beginners new to Maya when we can't remember where this tool is that is often used for setting up a model.</b>

GOAL 2: <b>Following goal 1, the same script helps with creating efficiency of tools themselves and interdependencies of tools to save time.</b> The script was applicable to the following scenarios from class and outside class:
  - Scenario 1: Using the image plane laying out vertices or blocking out anatomically correct shapes for a model like a robot
  - Scenario 2: Using this script in conjunction with the CV curve tool to quickly trace bottles for a scene. If I need to make quite a few different bottles, this script will help shorten the setup time.
  - Scenario 3: Using this script for modeling a lotion bottle to block out the shape using geometry

GOAL 3: <b>The script for mixamo T-rig pose was created to shorten set up time for animating my robot character using a mixamo rig.</b> Since the characters have to always start in T-pose, this script will come in handy for avoiding repition of manual set up steps. I wanted to also script the mapping assignment of joints in humanIK but this script was more complex so unfortunately this would have to be done in a refactor once I understood more.

GOAL 4: The scripts for the autorig_leg an autorig_arm scripts were created separately for me to learn the differences between the two workflows. The scripts are part of a button UI script that allows each function to run on button presses. 

GOAL 5: Familiarizing myself further with the Maya Python API and creating an autorig, I added the ball_autorig script. This is mainly used for reference for building other autorig tools and will help me with refactoring my leg and arm scripts, in addition to building a complete autorig in the future.  

Credit to: David Mooy for teaching the class on Introduction to Maya and sparking my curiosity in coding
           Chris Zurbrigg for tutorials on creating tools in the Maya Python API.
           Alexander Richter, TD for my Maya Python class


