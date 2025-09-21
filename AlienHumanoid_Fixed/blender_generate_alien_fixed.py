# blender_generate_alien_fixed.py
# Generates a SINGLE smooth alien mesh, rigs, animates, exports FBX.
# Run:
#   "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe" --background --python blender_generate_alien_fixed.py

import bpy, math, os

# -------------------------
# Setup
# -------------------------
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for datablock in (bpy.data.meshes, bpy.data.materials, bpy.data.armatures, bpy.data.actions):
        for b in list(datablock):
            datablock.remove(b, do_unlink=True)

clear_scene()

here = os.path.dirname(__file__)
tex_dir = os.path.join(here, "Textures")
export_fbx = os.path.join(here, "alien_humanoid_fixed.fbx")

# -------------------------
# Build Alien Mesh
# -------------------------
parts = []


def add_part(create_fn, **kwargs):
    """Execute the primitive add operator and return the shaded object."""
    create_fn(**kwargs)
    obj = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    parts.append(obj)
    return obj


# Core body volumes -----------------------------------------------------
head = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.14,
    location=(0.0, 0.0, 1.92),
)
head.scale = (0.9, 1.15, 1.25)

crest = add_part(
    bpy.ops.mesh.primitive_cone_add,
    radius1=0.06,
    radius2=0.0,
    depth=0.42,
    location=(0.0, -0.02, 2.04),
)
crest.rotation_euler = (math.radians(-120.0), 0.0, 0.0)

torso = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.18,
    location=(0.0, 0.0, 1.48),
)
torso.scale = (1.05, 0.75, 1.32)

rib_plate = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.17,
    location=(0.0, 0.08, 1.46),
)
rib_plate.scale = (0.75, 0.35, 0.55)

pelvis = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.12,
    location=(0.0, 0.0, 1.1),
)
pelvis.scale = (0.95, 0.7, 0.65)

abdomen = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.13,
    location=(0.0, -0.05, 1.25),
)
abdomen.scale = (0.85, 0.55, 0.9)

tail = add_part(
    bpy.ops.mesh.primitive_cone_add,
    radius1=0.08,
    radius2=0.01,
    depth=0.6,
    location=(0.0, -0.12, 1.0),
)
tail.rotation_euler = (math.radians(-65.0), 0.0, 0.0)


def add_cylinder(radius, depth, location, rotation=(0.0, 0.0, 0.0), scale=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location)
    obj = bpy.context.active_object
    obj.rotation_euler = rotation
    if scale is not None:
        obj.scale = scale
    return add_part(lambda **kw: None)


def add_limb_pair(cfgs):
    objs = []
    for side, x_sign in (("L", 1.0), ("R", -1.0)):
        params = cfgs(side, x_sign)
        objs.append(add_cylinder(**params))
    return objs


# Arms ------------------------------------------------------------------
shoulder_pad_L = add_part(
    bpy.ops.mesh.primitive_cone_add,
    radius1=0.12,
    radius2=0.02,
    depth=0.3,
    location=(0.26, 0.05, 1.62),
)
shoulder_pad_L.rotation_euler = (math.radians(110.0), 0.0, math.radians(12.0))
shoulder_pad_R = add_part(
    bpy.ops.mesh.primitive_cone_add,
    radius1=0.12,
    radius2=0.02,
    depth=0.3,
    location=(-0.26, 0.05, 1.62),
)
shoulder_pad_R.rotation_euler = (math.radians(110.0), 0.0, math.radians(-12.0))

def arm_cfg(side, x_sign):
    base_z = 1.52
    return {
        "radius": 0.05 if side == "L" else 0.05,
        "depth": 0.44,
        "location": (0.28 * x_sign, -0.02, base_z),
        "rotation": (math.radians(12.0), 0.0, math.radians(-10.0 * x_sign)),
        "scale": (1.0, 1.0, 1.15),
    }

add_limb_pair(arm_cfg)


def forearm_cfg(side, x_sign):
    return {
        "radius": 0.043,
        "depth": 0.46,
        "location": (0.5 * x_sign, -0.04, 1.32),
        "rotation": (math.radians(18.0), 0.0, math.radians(-6.0 * x_sign)),
        "scale": (1.0, 1.0, 1.2),
    }

add_limb_pair(forearm_cfg)

def hand_cfg(side, x_sign):
    return {
        "radius": 0.055,
        "depth": 0.25,
        "location": (0.68 * x_sign, 0.02, 1.12),
        "rotation": (math.radians(12.0), 0.0, math.radians(-2.0 * x_sign)),
        "scale": (1.0, 0.8, 1.2),
    }

add_limb_pair(hand_cfg)

finger_cluster_L = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.07,
    location=(0.78, 0.06, 1.02),
)
finger_cluster_L.scale = (1.2, 0.6, 0.5)
finger_cluster_R = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.07,
    location=(-0.78, 0.06, 1.02),
)
finger_cluster_R.scale = (1.2, 0.6, 0.5)


# Legs ------------------------------------------------------------------
def thigh_cfg(side, x_sign):
    return {
        "radius": 0.07,
        "depth": 0.52,
        "location": (0.16 * x_sign, 0.0, 1.0),
        "rotation": (math.radians(-6.0), 0.0, math.radians(-2.0 * x_sign)),
        "scale": (1.0, 1.0, 1.1),
    }

add_limb_pair(thigh_cfg)


def calf_cfg(side, x_sign):
    return {
        "radius": 0.06,
        "depth": 0.54,
        "location": (0.18 * x_sign, 0.02, 0.64),
        "rotation": (math.radians(10.0), 0.0, math.radians(-4.0 * x_sign)),
        "scale": (1.0, 0.95, 1.18),
    }

add_limb_pair(calf_cfg)


def foot_cfg(side, x_sign):
    return {
        "radius": 0.055,
        "depth": 0.26,
        "location": (0.2 * x_sign, 0.16, 0.26),
        "rotation": (math.radians(78.0), 0.0, math.radians(-3.0 * x_sign)),
        "scale": (1.0, 0.85, 1.0),
    }

add_limb_pair(foot_cfg)

heel_L = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.05,
    location=(0.2, -0.04, 0.2),
)
heel_L.scale = (0.8, 0.5, 1.0)
heel_R = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.05,
    location=(-0.2, -0.04, 0.2),
)
heel_R.scale = (0.8, 0.5, 1.0)

kneecap_L = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.05,
    location=(0.18, 0.1, 0.87),
)
kneecap_L.scale = (0.9, 0.7, 0.5)
kneecap_R = add_part(
    bpy.ops.mesh.primitive_uv_sphere_add,
    radius=0.05,
    location=(-0.18, 0.1, 0.87),
)
kneecap_R.scale = (0.9, 0.7, 0.5)

neck = add_part(
    bpy.ops.mesh.primitive_cylinder_add,
    radius=0.065,
    depth=0.28,
    location=(0.0, 0.0, 1.74),
)
neck.scale = (0.9, 0.9, 1.2)

bpy.ops.object.select_all(action='DESELECT')
for obj in parts:
    obj.select_set(True)
bpy.context.view_layer.objects.active = head
bpy.ops.object.join()
body = bpy.context.active_object

# Weld vertices
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.003)
bpy.ops.object.mode_set(mode='OBJECT')

# Subdivision + Triangulate
sub = body.modifiers.new("Subsurf",'SUBSURF'); sub.levels=2
tri = body.modifiers.new("Triangulate",'TRIANGULATE')
bpy.ops.object.modifier_apply(modifier=sub.name)
bpy.ops.object.modifier_apply(modifier=tri.name)

# UV unwrap
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
bpy.ops.object.mode_set(mode='OBJECT')

# -------------------------
# Material Setup
# -------------------------
skin = bpy.data.materials.new("Alien_Skin_Mat"); skin.use_nodes=True
nt = skin.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location=(300,0)
bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location=(0,0)
nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

def tex_node(fname, loc, colorspace='sRGB'):
    node = nt.nodes.new("ShaderNodeTexImage"); node.location=loc
    node.image = bpy.data.images.load(os.path.join(tex_dir,fname))
    if colorspace=='Non-Color':
        node.image.colorspace_settings.name='Non-Color'
    return node

tex_base = tex_node("Alien_BaseColor.png", (-400,120))
nt.links.new(tex_base.outputs["Color"], bsdf.inputs["Base Color"])

tex_r = tex_node("Alien_Roughness.png", (-400,-80),'Non-Color')
nt.links.new(tex_r.outputs["Color"], bsdf.inputs["Roughness"])

tex_n = tex_node("Alien_Normal.png", (-650,-20),'Non-Color')
nmap = nt.nodes.new("ShaderNodeNormalMap"); nmap.location=(-250,-20)
nt.links.new(tex_n.outputs["Color"], nmap.inputs["Color"])
nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])

body.data.materials.append(skin)

# -------------------------
# Armature + Animation
# -------------------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object
arm.name = "AlienArmature"
eb = arm.data.edit_bones

root = eb["Bone"]
root.name = "root"
root.head = (0.0, 0.0, 0.0)
root.tail = (0.0, 0.0, 0.1)

pelvis = eb.new("pelvis")
pelvis.head = (0.0, 0.0, 1.05)
pelvis.tail = (0.0, 0.0, 1.25)
pelvis.parent = root

spine = eb.new("spine")
spine.head = pelvis.tail
spine.tail = (0.0, 0.0, 1.55)
spine.parent = pelvis

chest = eb.new("chest")
chest.head = spine.tail
chest.tail = (0.0, 0.0, 1.72)
chest.parent = spine

neckb = eb.new("neck")
neckb.head = chest.tail
neckb.tail = (0.0, 0.0, 1.9)
neckb.parent = chest

headb = eb.new("head")
headb.head = neckb.tail
headb.tail = (0.0, 0.0, 2.12)
headb.parent = neckb


def make_limb(side, x_sign):
    clav = eb.new(f"clavicle.{side}")
    clav.head = (0.1 * x_sign, 0.0, 1.68)
    clav.tail = (0.28 * x_sign, 0.04, 1.7)
    clav.parent = chest

    upper = eb.new(f"upper_arm.{side}")
    upper.head = clav.tail
    upper.tail = (0.48 * x_sign, -0.02, 1.48)
    upper.parent = clav

    fore = eb.new(f"lower_arm.{side}")
    fore.head = upper.tail
    fore.tail = (0.68 * x_sign, -0.06, 1.22)
    fore.parent = upper

    hand = eb.new(f"hand.{side}")
    hand.head = fore.tail
    hand.tail = (0.78 * x_sign, 0.02, 1.05)
    hand.parent = fore


for suffix, sign in (("L", 1.0), ("R", -1.0)):
    make_limb(suffix, sign)


def make_leg(side, x_sign):
    thigh = eb.new(f"thigh.{side}")
    thigh.head = (0.14 * x_sign, 0.0, 1.05)
    thigh.tail = (0.18 * x_sign, 0.04, 0.65)
    thigh.parent = pelvis

    calf = eb.new(f"calf.{side}")
    calf.head = thigh.tail
    calf.tail = (0.2 * x_sign, 0.08, 0.28)
    calf.parent = thigh

    foot = eb.new(f"foot.{side}")
    foot.head = calf.tail
    foot.tail = (0.24 * x_sign, 0.3, 0.1)
    foot.parent = calf

    toe = eb.new(f"ball.{side}")
    toe.head = foot.tail
    toe.tail = (0.24 * x_sign, 0.46, 0.1)
    toe.parent = foot


for suffix, sign in (("L", 1.0), ("R", -1.0)):
    make_leg(suffix, sign)


tail_bone = eb.new("tail")
tail_bone.head = (0.0, -0.08, 1.1)
tail_bone.tail = (0.0, -0.32, 0.9)
tail_bone.parent = pelvis

bpy.ops.object.mode_set(mode='OBJECT')

# Parent mesh
body.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# Export FBX
bpy.ops.export_scene.fbx(
    filepath=export_fbx,
    use_selection=False,
    apply_scale_options='FBX_SCALE_ALL',
    bake_anim=True,
    add_leaf_bones=False,
    object_types={'ARMATURE','MESH'},
    path_mode='AUTO'
)
print("Exported:", export_fbx)
