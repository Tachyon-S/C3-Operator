# C3-Operator
Blender scripts to import/export C3 models.

#### version: 2.3
#### Blender Tested Versions: 2.8+


Example: the model `003194790.C3` posed freely.
![2](https://user-images.githubusercontent.com/84657141/119335019-72ac2c80-bc94-11eb-948a-c03d0aa9b78c.png)
![ezgif-4-ae81d637973e](https://user-images.githubusercontent.com/84657141/119988335-a9ed4700-bfce-11eb-8e33-cb1f1f857f5b.gif)


## How to use it
### Installation
Download the zip archive from the [latest release](https://github.com/Tachyon-S/C3-Operator/releases) and the [reference files](https://github.com/Tachyon-S/C3-Operator/releases/tag/References).

In Blender go to Edit > Preferences > Add-ons > Install > choose the the zip archive you downloaded.
Then check the box in front of the add-on name if not checked.
Once installed, "C3 Operator" menu will appear on the upper left bar.

### Notes About Importing
- To import animation make sure you select the armature and not the mesh.
- TO import texture make sure you select the mesh and not the armature.
- Imported models are usually large. You may want to increase your view clipping end found in the (N) menu.
- With the release you can find models, texture and animations to test with and use as Model Y in the export process (see below).

### Export
Let's call the model we want to export X (keep a copy of it).
- Bake all different materials and textures into a single texture.
- To avoid working directly with bones and weights, we are going to copy the weights from another model. import the model you are going to mimic its weights. Don't import any other model after it as the path is used in the next step. We will call this model Y. Make sure X is scaled and posed similar to how Y is in order for weights to works correctly.
- C3 does not support seams. Instead they duplicate vertices and edges. C3 models are unpacked literally. Therefore just before exporting choose all your seams in edges edit mode, then from the right click menu choose Edge Split.
- Make sure that all the faces are triangles. You can use the utility `Faces > Triangulate Faces` in edit mode after choosing all faces.
- Now choose the mesh X (not the armature) and choose Save C3 Model from C3 Operator menu.
- This exporting process works for weapons as well, choose a weapon that is similar to the one you want to export and use it as a reference.
- It is recommended to use models of subtype 0x34 than those of subtype 0x20. Check the [wiki](https://github.com/Tachyon-S/C3-Operator/wiki/C3-Garment-Structure) for the defintion of subtype.

## Changelog
V 2.0.0:
- Interaction through GUI
- No need to chagne the engine to cycles.
- Added export functionality

V 2.1.0:
- Import/Export Weapons
- Use models of subtype 0x20 as reference for export (still experimental).

## TODO
- Normalize different scales, positions and orientations of models and animations.  
  * Figure out how C3 engine handles different scales.
- Translate Bone system between c3 and blender.
  * Add export with custom bones function.
- Convert (a reduced version of) Blender uv system to C3 uv system.
  * Automate the process of doubling seams.
- include hair and effects.

## Limitations and Issues
- Tested on garments.


## Common Error Messages and Workarounds.
- Always apply transformations to your mesh: in object mode `Object > Apply > All transformations`.
- If `required argument is not a float` got shown while you are trying to export the c3 try going into edit mode, select all the vertices then `Mesh > Merge > By Distance`. Make sure the distance is small (by defualt it is, mostly no need to change it).

## References
- [This post on Xentax](https://forum.xentax.com/viewtopic.php?t=5582) is what inspired me to start this project.
