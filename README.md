# C3-Operator
Blender scripts to import/export C3 models.

#### version: 1.0
#### Blender Tested Versions: 2.79

## How to use it
## Import 
- Download the script.
- Open Blender.
- Remove the cube :p (as usual) by pressing x or delete on the cube.
- On the upper bar there is a drop down menu. Change the engine to Cycles.
![1](https://user-images.githubusercontent.com/84657141/119251950-eb868800-bbb1-11eb-9172-a9d53345ed00.png)
- Change the UI view to scripting.
![1](https://user-images.githubusercontent.com/84657141/119251987-1e308080-bbb2-11eb-880f-9da0d5dc4aa2.png)
- Open the script `OpenC3_with_bones` using the open button you find below on the scripting panel to the left.
- Go to the end of the script once opened and change the the variable `filePath` and `texturePath` to the path of the model `.c3` and the texture `.dds` you want to import respectively.
- Click `Run Script` (it is found to the right of the open button you clicked previously).

## Limitations and Issues
- Tested on garments.
- Does not work for all c3 files (not even all garments).

## References
- [This post on Xentax](https://forum.xentax.com/viewtopic.php?t=5582) is what inspired me to start this project.
