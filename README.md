# C3-Operator
Blender scripts to import/export C3 models.

#### version: 2.1.0
#### Blender Tested Versions: 2.8+


Example: the model `003194790.C3` posed freely.
![2](https://user-images.githubusercontent.com/84657141/119335019-72ac2c80-bc94-11eb-948a-c03d0aa9b78c.png)
![ezgif-4-ae81d637973e](https://user-images.githubusercontent.com/84657141/119988335-a9ed4700-bfce-11eb-8e33-cb1f1f857f5b.gif)


## How to use it
### Installation
Download the zip archive from the [latest release](https://github.com/Tachyon-S/C3-Operator/releases/tag/v2.1.0).

In Blender go to Edit > Preferences > Add-ons > Install > choose the the zip archive you downloaded.
Then check the box in front of the add-on name if not checked.
Once installed, "C3 Operator" menu will appear on the upper left bar.

### Notes About Importing
- To import animation make sure you select the armature and not the mesh.
- TO import texture make sure you select the mesh and not the armature.
- Imported models are usually large. You may want to increase your view clipping end found in the (N) menu.
- With the release you can find models, texture and animations to test with and use as Model Y in the export process (see below).

### Export
Let's call the model we want to export X.
- Bake all different materials and textures into a single texture.
- To avoid working directly with bones and weights, we are going to copy the weights from another model. import the model you are going to mimic its weights. Don't import any other model after it as the path is used in the next step. We will call this model Y. Make sure X is scaled and posed similar to how Y is in order for weights to works correctly.
- C3 does not support seams. Instead they duplicate vertices and edges. C3 models are unpacked literally. Therefore just before exporting choose all your seams in edges edit mode, then from the right click menu choose Edge Split.
- Now choose the mesh X (not the armature) and choose Save C3 Model from C3 Operator menu.


## Changelog
V 2.0.0:
- Interaction through GUI
- No need to chagne the engine to cycles.
- Added export functionality

## Limitations and Issues
- Tested on garments.

## References
- [This post on Xentax](https://forum.xentax.com/viewtopic.php?t=5582) is what inspired me to start this project.
