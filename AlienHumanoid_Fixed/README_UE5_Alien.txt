Alien Humanoid — Fixed Single-Mesh Export (Blender 4.3)
======================================================
Run:
  Windows:
    "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe" --background --python blender_generate_alien_fixed.py
Outputs:
  alien_humanoid_fixed.fbx  (single smooth mesh, rigged, Idle+Walk baked)
  /Textures/*.png           (BaseColor, Normal, Roughness, Emissive)
UE5 Import:
  - Skeletal Mesh: ON
  - Import Animations: ON
  - Assign materials manually after import.
