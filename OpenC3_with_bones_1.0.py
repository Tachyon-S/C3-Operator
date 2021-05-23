bl_info = {
    "name": "C3 Operator",
    "author": "Tachyon!",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "File > C3 Operator",
    "description": "Import/Export C3 models",
    "warning": "It does not work with all models. Do not forget to set the engine to Cycles.",
    "wiki_url": "https://github.com/Tachyon-S/C3-Operator",
    "category": "Add Mesh",
    }



import os
import struct
import bpy
import bmesh
from bpy_extras.object_utils import object_data_add
from mathutils import Vector

class MyFile:
    def __init__(self, path, pointer=0):
        self.path = path
        self.pointer = pointer
        self.file = open(path, 'rb')
        self.length = 0
    
    def load(self):
        self.file.seek(0)
        self.data = self.file.read()
        self.length = len(self.data)

    def readInt(self, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        integer = struct.unpack('<i', self.data[pointer:pointer+4])[0]
        self.pointer = self.pointer + 4
        return integer
    def readByte(self, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        byte = struct.unpack('<b', self.data[pointer:pointer+1])[0]
        self.pointer = self.pointer + 1
        return byte
    def readShort(self, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        s = struct.unpack('<H', self.data[pointer:pointer+2])[0]
        
        self.pointer = self.pointer + 2
        return s
    def readFloat(self, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        f = struct.unpack('<f', self.data[pointer:pointer+4])[0]
        self.pointer = self.pointer + 4
        return f
    def readString(self, length, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        text = self.data[pointer:pointer+length].decode()
        self.pointer = self.pointer + length
        return text
    def setPointer(self, value):
        self.pointer = value
        return self.pointer
    def getPointer(self):
        return self.pointer
    def __len__(self):
        return self.length









def importC3(filePath, texturePath):
    scene = bpy.context.scene
    
    meshes = []
    print('openning file')
    file = MyFile(filePath)
    file.load()
    Magic1 = file.readString(0x10)
    MOT_number = 0
    while True:
        Magic2 = file.readString(0x3)
        Magic = file.readByte()
        sectSize = file.readInt()
        sectionStart = file.getPointer()
        vertCount = 0
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
                file.readInt()
        
        Vert_array = []
        UV_array = []
        Face_array = []
        Bone1_indices = []
        Bone2_indices = []
        Weight1 = []
        Weight2 = []
        '''if Magic == 0x20:
            for a in range(vertCount):
                vx = file.readFloat()
                vy = file.readFloat()
                vz = file.readFloat()
                file.setPointer(file.getPointer() + 0x24)
                tu = (file.readFloat()) * 1
                tv = (file.readFloat()) * -1
                file.setPointer(file.getPointer() + 0x14)
                Vert_array.append(Vector((vx,vy,vz)))
                #Vert_array.append((nx,ny,nz))
                UV_array.append(Vector((tu,tv,0)))'''
                
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
            file.readInt()
            for a in range(FaceCount):
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
            scene.objects.active = new_object
            new_object.select = True
            
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            for v in new_object.data.vertices:
                try:
                    new_object.vertex_groups['c3_bone_'+str(Bone1_indices[v.index])]
                except:
                    new_object.vertex_groups.new('c3_bone_'+str(Bone1_indices[v.index]))
                
                new_object.vertex_groups['c3_bone_'+str(Bone1_indices[v.index])].add([v.index], Weight1[v.index], 'REPLACE')
                
                try:
                    new_object.vertex_groups['c3_bone_'+str(Bone2_indices[v.index])]
                except:
                    new_object.vertex_groups.new('c3_bone_'+str(Bone2_indices[v.index]))
                
                new_object.vertex_groups['c3_bone_'+str(Bone2_indices[v.index])].add([v.index], Weight2[v.index], 'REPLACE')
            
            
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(new_mesh)

            uv_layer = bm.loops.layers.uv.verify()
            bm.faces.layers.tex.verify()

            for f in bm.faces:
                for l in f.loops:
                    luv = l[uv_layer]
                    luv.uv = UV_array[l.vert.index]

            bmesh.update_edit_mesh(new_mesh)
            bpy.ops.object.mode_set(mode='OBJECT')
            new_material = bpy.data.materials.new('material')
            new_material.use_nodes = True
            node_tree = new_material.node_tree
            bsdf = node_tree.nodes["Diffuse BSDF"]
            
            node = node_tree.nodes.new("ShaderNodeTexImage")
            node.select = True
            node_tree.nodes.active = node
            node.image = bpy.data.images.load(os.path.abspath(texturePath))
            node_tree.links.new(bsdf.inputs['Color'], node.outputs['Color'])
            new_object.data.materials.append(new_material)
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
                bpy.context.scene.objects.link(arm_obj)
                arm_obj.select = True
                bpy.context.scene.objects.active = arm_obj
                bpy.ops.object.mode_set(mode='EDIT')
                for a in range(number_of_bones):
                    file.setPointer(file.getPointer() + 4*12)
                    bone_x = file.readFloat()
                    bone_y = file.readFloat()
                    bone_z = file.readFloat()
                    bone = arm_obj.data.edit_bones.new('c3_bone_'+ str(a))
                    bone.head = (bone_x,bone_y,bone_z)
                    bone.tail = (bone_x,bone_y,bone_z-1.0)
                    file.readInt()
        
        
        if (file.setPointer(sectionStart+sectSize)) >= len(file):
            break
        
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects['v_body'].select = True
    bpy.context.scene.objects['v_body_arm_obj'].select = True
    bpy.context.scene.objects.active = bpy.context.scene.objects['v_body_arm_obj']
    bpy.ops.object.parent_set(type='ARMATURE')
        
    #return objectCollection, meshes



PHY_section_names = ['v_body']
filePath = 'C:\\Users\\......\\003194790.C3'
texturePath = 'C:\\Users\\......\003194790.dds'
importC3(filePath, texturePath)
print("============  DONE!  =================")

 