import maya.cmds as cmds

sel = cmds.ls(sl=True, type="transform") or []

for obj in sel:
    shapes = cmds.listRelatives(obj, s=True, type="nurbsCurve") or []
    if not shapes:
        continue  # skip if it's not a nurbs curve control
    
    t = cmds.getAttr(obj + ".translate")[0]
    r = cmds.getAttr(obj + ".rotate")[0]
    s = cmds.getAttr(obj + ".scale")[0]
    
    if not (t == (0,0,0) and r == (0,0,0) and s == (1,1,1)):
        print(obj, "needs freezing!!")

