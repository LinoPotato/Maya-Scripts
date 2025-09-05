import maya.cmds as cmds

# Get the selection (driver first, driven second)
sel = cmds.ls(sl=True)
if len(sel) != 2:
    cmds.error("Please select two objects: driver first, driven second.")

driver = sel[0]
driven = sel[1]

#connectAttr() needs attribute names as strings in "nodeName.attributeName" 
#format, so we have to build that string manually. Yeah shuck!

# Connect translate attributes
cmds.connectAttr(driver + ".translate", driven + ".translate", force=True)

