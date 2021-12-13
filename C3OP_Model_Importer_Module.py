import os
import sys
import struct
import bpy
import bmesh
from bpy_extras.object_utils import object_data_add
from mathutils import Vector


script_file = os.path.realpath(__file__)
directory = os.path.dirname(script_file)
sys.path.append(directory)

import C3OP_Helping_File_Manager_Module
import C3OP_Warnings
PHY_section_names = ['v_body'] # What to do about it?





class C3_Operator_Model_Importer:
    c3_path = ""
    texture_path = ""
    animation_path = ""
    
    @staticmethod
    def importC3(filePath):
        #scene = bpy.context.scene        # for Blender 2.79
        scene = bpy.context.collection    # for Blender 2.8+
        meshes = []
        print('openning file')
        file = C3OP_Helping_File_Manager_Module.C3OP_Helping_File_Reader(filePath)
        file.load()
        Magic1 = file.readString(0x10)
        MOT_number = 0
        while True:
            Magic2 = file.readString(0x3)
            Magic = file.readByte()
            sectSize = file.readInt()
            sectionStart = file.getPointer()
            vertCount = 0
            vertCount2 = 0
            if Magic2 == "PHY":
                print("Found PHY section at: 0x{:08x}".format(sectionStart-8))
                print("Section has type: 0x{:02x}".format(Magic))
                nsize = file.readInt()
                meshName = file.readString(nsize)
                print("Section name is: " + meshName)
                if meshName in PHY_section_names:
                    file.readInt()
                    vertCount = file.readInt()
                    print("The section contains " + str(vertCount) + " vertices")
                    vertCount2 = file.readInt()
                    print("The section contains " + str(vertCount2) + " vertices of type 2")
            
            Vert_array = []
            UV_array = []
            Face_array = []
            Bone1_indices = []
            Bone2_indices = []
            Weight1 = []
            Weight2 = []
            if Magic == 0x20:
                for a in range(vertCount + vertCount2):
                    vx = file.readFloat()
                    vy = file.readFloat()
                    vz = file.readFloat()
                    file.setPointer(file.getPointer() + 0x24)
                    tu = (file.readFloat())
                    tv = 1 - (file.readFloat())
                    Vert_array.append(Vector((vx,vy,vz)))
                    UV_array.append(Vector((tu,tv,0)))
                    
                    file.readInt()
                    Bone1_indices.append(file.readInt())
                    Bone2_indices.append(file.readInt())
                    Weight1.append(file.readFloat())
                    Weight2.append(file.readFloat())
                    
            if Magic == 0x34:
                for a in range(vertCount):
                    vx = file.readFloat()
                    vy = file.readFloat()
                    vz = file.readFloat()
                    tu = (file.readFloat())
                    tv = 1 - (file.readFloat())
                    Vert_array.append(Vector((vx,vy,vz)))
                    UV_array.append((tu,tv))
                    
                    file.readInt()
                    Bone1_indices.append(file.readInt())
                    Bone2_indices.append(file.readInt())
                    Weight1.append(file.readFloat())
                    Weight2.append(file.readFloat())
                    
            
            if len(Vert_array) > 0:
                FaceCount = file.readInt()
                print("The section contains " + str(FaceCount) + " faces")
                FaceCount2 = file.readInt()
                print("The section contains " + str(FaceCount2) + " faces of type 2")
                for a in range(FaceCount + FaceCount2):
                    f1 = (file.readShort()) #+ 1
                    f2 = (file.readShort()) #+ 1
                    f3 = (file.readShort()) #+ 1
                    Face_array.append([f1,f2,f3]) #save faces to Face_array

            if len(Vert_array) > 0:
                
                new_mesh = bpy.data.meshes.new(meshName)
                new_mesh.from_pydata(Vert_array, [], Face_array)
                new_mesh.update()
                meshes.append(new_mesh)
                new_object = bpy.data.objects.new(meshName, new_mesh)
                
                scene.objects.link(new_object)
                bpy.context.view_layer.objects.active = new_object # Blender 2.8+
                #new_object.select = True    # Blender 2.79
                bpy.context.active_object.select_set(state=True) # Blender 2.8+
                
                
                bpy.ops.object.mode_set(mode='OBJECT')
                
                for v in new_object.data.vertices:
                    try:
                        new_object.vertex_groups['c3_bone_'+str(Bone1_indices[v.index])]
                    except:
                        new_object.vertex_groups.new(name = ('c3_bone_'+str(Bone1_indices[v.index])))
                    
                    new_object.vertex_groups['c3_bone_'+str(Bone1_indices[v.index])].add([v.index], Weight1[v.index], 'REPLACE')
                    
                    try:
                        new_object.vertex_groups['c3_bone_'+str(Bone2_indices[v.index])]
                    except:
                        new_object.vertex_groups.new(name = ('c3_bone_'+str(Bone2_indices[v.index])))
                    
                    new_object.vertex_groups['c3_bone_'+str(Bone2_indices[v.index])].add([v.index], Weight2[v.index], 'REPLACE')
                
                
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(new_mesh)

                uv_layer = bm.loops.layers.uv.verify()
                #bm.faces.layers.tex.verify() # is this line needed ?

                for f in bm.faces:
                    for l in f.loops:
                        luv = l[uv_layer]
                        try:
                            luv.uv = UV_array[l.vert.index]
                        except:
                            luv.uv = UV_array[l.vert.index].xy

                bmesh.update_edit_mesh(new_mesh)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # make the bmesh the object's mesh
                #bm.to_mesh(mesh)  
                #bm.free()  # always do this when finished
                print("~~~~~~~~~~~~~~~~~~~~~~~~")
            
            if Magic2 == "MOT":
                MOT_number = MOT_number + 1
                print("Found MOT section at: 0x{:08x}".format(sectionStart-8))
                print("Section has type: 0x{:02x}".format(Magic))
                number_of_bones = file.readInt()
                file.readInt()
                type_of_key_frame = file.readString(4)
                file.readInt()
                print("MOT section type is: " + type_of_key_frame)
                if MOT_number == 4:
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.select_all(action='DESELECT')
                    
                    arm = bpy.data.armatures.new("v_body_arm")
                    arm_obj = bpy.data.objects.new("v_body_arm_obj", arm)
                    scene.objects.link(arm_obj)
                    #arm_obj.select = True
                    #scene.objects.active = arm_obj
                    bpy.context.view_layer.objects.active = arm_obj    # Blender 2.8+
                    arm_obj.select_set(state=True)   # Blender 2.8+
                    bpy.ops.object.mode_set(mode='EDIT')
                    for a in range(number_of_bones):
                        file.setPointer(file.getPointer() + 4*12)
                        bone_x = file.readFloat()
                        bone_y = file.readFloat()
                        bone_z = file.readFloat()
                        bone = arm_obj.data.edit_bones.new('c3_bone_'+ str(a))
                        bone.head = (bone_x,bone_y,bone_z)
                        bone.tail = (bone_x,bone_y + 1.0,bone_z)
                        file.readInt()
            
            
            if (file.setPointer(sectionStart+sectSize)) >= len(file):
                break
            
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        #scene.objects['v_body'].select_set(state=True)   # Blender 2.8+
        new_object.select_set(state=True)   # Blender 2.8+
        #scene.objects['v_body_arm_obj'].select_set(state=True)   # Blender 2.8+
        arm_obj.select_set(state=True)   # Blender 2.8+
        bpy.context.view_layer.objects.active = arm_obj #bpy.context.scene.objects['v_body_arm_obj']
        bpy.ops.object.parent_set(type='ARMATURE')
            
        #return objectCollection, meshes
    
    @staticmethod
    def importTex(texturePath):
        if bpy.context.active_object.type != 'MESH':
            C3OP_Warnings.ShowMessageBox("The active object is not of type MESH")
            return
        
        bpy.ops.object.mode_set(mode='OBJECT')
        new_material = bpy.data.materials.new('material')
        new_material.use_nodes = True
        #new_object.data.materials.append(new_material)
        node_tree = new_material.node_tree
        node_tree.nodes.remove(node_tree.nodes["Principled BSDF"])
        #bsdf = node_tree.nodes["Diffuse BSDF"]
        bsdf = node_tree.nodes.new("ShaderNodeBsdfDiffuse")
        output = node_tree.nodes["Material Output"]
                
        node = node_tree.nodes.new("ShaderNodeTexImage")
        node.select = True
        node_tree.nodes.active = node
        node.image = bpy.data.images.load(os.path.abspath(texturePath))
        node_tree.links.new(bsdf.inputs['Color'], node.outputs['Color'])
        node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
                            
        bpy.context.view_layer.objects.active.data.materials.append(new_material)
        
    
    @staticmethod
    def importAnimation(animation_path):
        
        if bpy.context.active_object.type != 'ARMATURE':
            C3OP_Warnings.ShowMessageBox("The active object is not of type ARMATURE")
            return
        
        print('openning th animation file')
        file = C3OP_Helping_File_Reader_Module.C3OP_Helping_File_Reader(animation_path)
        file.load()
        Magic1 = file.readString(0x10)
        MOT_number = 0
        while MOT_number < 4:
            MOT_number = MOT_number + 1
            Magic2 = file.readString(0x3)
            Magic = file.readByte()
            sectSize = file.readInt()
            sectionStart = file.getPointer()
            
            
            if MOT_number == 4:
                boneCount = file.readInt()
                frameCount = file.readInt()
                file.readString(4) # ZKEY
                file.readInt()
                
                #armature = bpy.data.objects[arm_name]
                #bpy.context.view_layer.objects.active = armature
                armature = bpy.context.view_layer.objects.active
                bpy.ops.object.mode_set(mode='POSE')
                
                last_rot_1 = [0]*boneCount
                last_rot_2 = [0]*boneCount
                last_rot_3 = [0]*boneCount
                last_rot_4 = [0]*boneCount
                last_loc_x = [0]*boneCount
                last_loc_y = [0]*boneCount
                last_loc_z = [0]*boneCount
                    
                while True:
                    frameNumber = file.readShort()
                    if frameNumber == frameCount -1:
                        break
                    
                    for j in range(boneCount):
                        rot_1 = file.readFloat()
                        rot_2 = file.readFloat()
                        rot_3 = file.readFloat()
                        rot_4 = file.readFloat()
                        loc_x = file.readFloat()
                        loc_y = file.readFloat()
                        loc_z = file.readFloat()
                        
                        if frameNumber > 0:
                            v1 = Vector((rot_1,rot_2,rot_3,rot_4))
                            v2 = Vector((last_rot_1[j],last_rot_2[j],last_rot_3[j],last_rot_4[j]))
                            v = v2 - v1
                            v_alternative = v2 + v1
                            
                            
                            if v_alternative.length < v.length:
                                print(frameNumber)
                                print(j)
                                print(v.length)
                                print(v_alternative.length)
                                rot_1 = -rot_1
                                rot_2 = -rot_2
                                rot_3 = -rot_3
                                rot_4 = -rot_4
                        try:
                            armature.pose.bones["c3_bone_"+str(j)].rotation_quaternion = (rot_4,rot_1,rot_2,rot_3)
                            armature.pose.bones["c3_bone_"+str(j)].location = (loc_x,loc_y,loc_z)
                            armature.pose.bones["c3_bone_"+str(j)].keyframe_insert(data_path='location', frame=frameNumber*5)
                            armature.pose.bones["c3_bone_"+str(j)].keyframe_insert(data_path='rotation_quaternion', frame=frameNumber*5)
                        except:
                            continue
                        
                        
                        last_rot_1[j] = rot_1
                        last_rot_2[j] = rot_2
                        last_rot_3[j] = rot_3
                        last_rot_4[j] = rot_4
                        last_loc_x[j] = loc_x
                        last_loc_y[j] = loc_y
                        last_loc_z[j] = loc_z
                
                
            
            file.setPointer(sectionStart+sectSize)
        bpy.ops.object.mode_set(mode='OBJECT')


import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

class C3OP_Open_C3_Mesh_UI(Operator, ImportHelper):

    bl_idname = "c3op.open_c3_mesh_ui"
    bl_label = "Open C3 File"
    
    filter_glob: StringProperty(
        default='*.c3;*.C3',
        options={'HIDDEN'}
    )
    

    def execute(self, context):
        
        C3_Operator_Model_Importer.c3_path = self.filepath
        #importer = C3_Operator_Model_Importer()
        C3_Operator_Model_Importer.importC3(C3_Operator_Model_Importer.c3_path)
        
        return {'FINISHED'}

class C3OP_Open_Texture_UI(Operator, ImportHelper):

    bl_idname = "c3op.open_texture_ui"
    bl_label = "Open Texture Image"
    
    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp;*.dds',
        options={'HIDDEN'}
    )
    

    def execute(self, context):
        
        C3_Operator_Model_Importer.texture_path = self.filepath
        #importer = C3_Operator_Model_Importer()
        C3_Operator_Model_Importer.importTex(C3_Operator_Model_Importer.texture_path)

        return {'FINISHED'}
        




class C3OP_Open_Animation_UI(Operator, ImportHelper):

    bl_idname = "c3op.open_animation_ui"
    bl_label = "Open C3 Animation"
    
    filter_glob: StringProperty(
        default='*.c3;*.C3',
        options={'HIDDEN'}
    )
    

    def execute(self, context):
        
        C3_Operator_Model_Importer.animation_path = self.filepath
        #importer = C3_Operator_Model_Importer()
        C3_Operator_Model_Importer.importAnimation(C3_Operator_Model_Importer.animation_path)

        return {'FINISHED'}