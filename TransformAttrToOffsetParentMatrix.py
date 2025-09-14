import maya.cmds as cmds

class Transform:
    # Stores Translate, Rotate, Scale as 3 tuples (thx Birbe)
    def __init__(self, t:tuple, r:tuple, s:tuple):
        self.t = t
        self.r = r
        self.s = s
        
    def __str__(self) -> str:
        return f"T: {self.t}, R: {self.r}, S: {self.s}"

all_nodes: dict[str, Transform] = {}

def get_transform_attr():
    # refresh sel & fill nodes
    all_nodes.clear()
    sel = cmds.ls(sl=True, type="transform", long=True) or []
    if not sel:
        cmds.warning("You gotta select at least one object dummy!")
        return
    
    for node in sel:
        t = cmds.getAttr(node + ".translate")[0]
        r = cmds.getAttr(node + ".rotate")[0]
        s = cmds.getAttr(node + ".scale")[0]
        all_nodes[node] = Transform(t, r, s)

        print("Node:", node)
        print("  Translate:", t)
        print("  Rotate:   ", r)
        print("  Scale:    ", s)
        print("-" * 40, "\n")
    print("Number of nodes:", len(all_nodes))

def set_offset_parent_matrix():
    
    if not all_nodes:
        cmds.warning("Dictionary empty! Run get_transform_attr() first.")
        return

    for node, tf in all_nodes.items():
        if not cmds.objExists(node):
            cmds.warning("Missing node: " + node)
            continue

        # make a unique temp transform
        temp = cmds.createNode("transform")
        try:
            # copy SRT to temp
            cmds.setAttr(temp + ".translate", *tf.t)
            cmds.setAttr(temp + ".rotate",    *tf.r)
            cmds.setAttr(temp + ".scale",     *tf.s)

            # grab world matrix of that temp 
            mat = cmds.xform(temp, q=True, m=True, ws=True)

            # apply to OPM
            cmds.setAttr(node + ".offsetParentMatrix", *mat, type="matrix")

            # zero SRT on the node (skip if locked/connected)
            for attr, val, tpe in (("translate", (0,0,0), "double3"),
                                   ("rotate",    (0,0,0), "double3"),
                                   ("scale",     (1,1,1), "double3")):
                plug = f"{node}.{attr}"
                if not cmds.getAttr(plug, l=True) and not (cmds.listConnections(plug, s=True, d=False) or []):
                    cmds.setAttr(plug, *val, type=tpe)

        finally:
            # always delete temp, even if something errors
            if cmds.objExists(temp):
                cmds.delete(temp)

    print(f"Done. Baked {len(all_nodes)} node(s) into offsetParentMatrix.")

# Run
get_transform_attr()
set_offset_parent_matrix()
