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
def add_part(op, **kwargs):
    op(**kwargs)
    obj = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    parts.append(obj)
    return obj

head = add_part(bpy.ops.mesh.primitive_uv_sphere_add, radius=0.12, location=(0,0,1.75))
torso = add_part(bpy.ops.mesh.primitive_uv_sphere_add, radius=0.16, location=(0,0,1.45)); torso.scale=(0.9,0.7,1.2)
pelvis = add_part(bpy.ops.mesh.primitive_uv_sphere_add, radius=0.11, location=(0,0,1.12)); pelvis.scale=(0.9,0.7,0.6)

def add_cyl(r, d, loc):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc)
    return add_part(lambda **kw: None)  # active object already set

upper_arm_L = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.045, depth=0.35, location=(0.22,0.0,1.45))
lower_arm_L = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.04, depth=0.35, location=(0.40,0.0,1.25))
upper_arm_R = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.045, depth=0.35, location=(-0.22,0.0,1.45))
lower_arm_R = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.04, depth=0.35, location=(-0.40,0.0,1.25))
upper_leg_L = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.06, depth=0.45, location=(0.12,0.0,0.95))
lower_leg_L = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.055, depth=0.45, location=(0.12,0.0,0.60))
upper_leg_R = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.06, depth=0.45, location=(-0.12,0.0,0.95))
lower_leg_R = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.055, depth=0.45, location=(-0.12,0.0,0.60))
neck = add_part(bpy.ops.mesh.primitive_cylinder_add, radius=0.055, depth=0.18, location=(0,0,1.62))

# Join all parts into one mesh
for p in parts: p.select_set(True)
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
bpy.ops.object.armature_add(enter_editmode=True, location=(0,0,1.0))
arm = bpy.context.active_object; arm.name="AlienArmature"
eb = arm.data.edit_bones
eb["Bone"].name="root"; eb["root"].head=(0,0,1.05); eb["root"].tail=(0,0,1.15)

spine=eb.new("spine"); spine.head=(0,0,1.15); spine.tail=(0,0,1.55); spine.parent=eb["root"]
neckb=eb.new("neck"); neckb.head=(0,0,1.55); neckb.tail=(0,0,1.68); neckb.parent=spine
headb=eb.new("head"); headb.head=(0,0,1.68); headb.tail=(0,0,1.78); headb.parent=neckb

bpy.ops.object.mode_set(mode='OBJECT')

# Parent mesh
body.select_set(True); bpy.context.view_layer.objects.active=arm
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
