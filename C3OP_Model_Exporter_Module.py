import os
import sys
import struct
import bpy
import bmesh
from bpy_extras.object_utils import object_data_add
from mathutils import Vector
import math


script_file = os.path.realpath(__file__)
directory = os.path.dirname(script_file)
sys.path.append(directory)

import C3OP_Helping_File_Manager_Module
from C3OP_Model_Importer_Module import C3_Operator_Model_Importer
import C3OP_Warnings

PHY_section_names = ['v_body']    # Later ....



class C3_Operator_Model_Exporter:
    output_path = ""
    reference_path = ""
    @staticmethod
    def exportC3UsingRef(outputPath, refPath):
        isGarment = False
        scene = bpy.context.scene
            
        print('openning file')
        file = C3OP_Helping_File_Manager_Module.C3OP_Helping_File_Reader(refPath)
        file.load()
        fileWriter = C3OP_Helping_File_Manager_Module.C3OP_Helping_File_Writer(outputPath)
        Magic1 = file.readString(0x10)
        fileWriter.writeString(Magic1)
        while True:
            Magic2 = file.readString(0x3)
            Magic = file.readByte()
            sectSize = file.readInt()
            sectionStart = file.getPointer()
            vertCount = 0
            nsize = file.readInt()
            nsize_w = 0
            try:
                meshName = file.readString(nsize)     # may fail with some names such as model 490020
                nsize_w = nsize
            except:
                file.setPointer(sectionStart + nsize + 4)
                meshName = "mesh01"
                nsize_w = 6
            print("Section name is: " + meshName)
            if meshName == "v_armet":
                isGarment = True
            if (meshName in PHY_section_names) or (not isGarment and Magic2 != "MOT"):   # if not garemnt, then suppose it has one PHY, just replace it.
                print('Reading vertices properites from the reference')
                file.readInt()
                #vertCount_r = file.readInt()
                vertCount_r = file.readInt() + file.readInt()
                #file.readInt()
                
                Vert_array = []
                UV_array = []
                Unknown1_array = []
                Unknown2_array = []
                Unknown3_array = []
                Unknown4_array = []
                Unknown5_array = []
                for a in range(vertCount_r):
                    vx = file.readFloat()
                    vy = file.readFloat()
                    vz = file.readFloat()
                    if Magic == 0x20:
                        file.setPointer(file.getPointer() + 0x24)
                    tu = (file.readFloat())
                    tv = 1 - (file.readFloat())
                    Vert_array.append(Vector((vx,vy,vz)))
                    UV_array.append((tu,tv))
                    Unknown1_array.append(file.readInt())
                    Unknown2_array.append(file.readInt())
                    Unknown3_array.append(file.readInt())
                    Unknown4_array.append(file.readFloat())
                    Unknown5_array.append(file.readFloat())
                
                FaceCount_r = file.readInt() + file.readInt()
                offsetToAdditional_r = (nsize + 4) + vertCount_r*(20+20) + (4+4+4)+ FaceCount_r*(2+2+2) + (4 + 4)
                if Magic == 0x20:
                    offsetToAdditional_r = offsetToAdditional_r + 0x24 * vertCount_r
                additional_size = sectSize - offsetToAdditional_r
                
                print('getting current mesh properties')
                obj = bpy.context.active_object
                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(obj.data)
                original_vertices = obj.data.vertices
                vertCount = len(original_vertices)
                vertices = []
                for v in original_vertices:
                    vertices.append(obj.matrix_world @ v.co)
                    
                faces = bm.faces
                FaceCount = len(bm.faces)
                sectSize_w = (nsize_w + 4) + vertCount*(20+20) + (4+4+4)+ FaceCount*(2+2+2) + (4 + 4) + additional_size
                if Magic == 0x20:
                    sectSize_w = sectSize_w + 0x24 * vertCount
                uvs_x = [None]*vertCount
                uvs_y = [None]*vertCount
                
                print(sectSize_w)
                print(sectSize)
                
                bm.verts.ensure_lookup_table()
                bm.edges.ensure_lookup_table()   
                bm.faces.ensure_lookup_table()
                
                
                uv_layer = bm.loops.layers.uv.verify()
                for f in bm.faces:
                    for l in f.loops:
                        luv = l[uv_layer]
                        uvs_x[l.vert.index] = luv.uv.x
                        uvs_y[l.vert.index] = 1-luv.uv.y
                
                Unknown1_w_array = [None]*vertCount
                Unknown2_w_array = [None]*vertCount
                Unknown3_w_array = [None]*vertCount
                Unknown4_w_array = [None]*vertCount
                Unknown5_w_array = [None]*vertCount
                print('Using reference to approximate vertices properties')
                for a in range(vertCount):
                    index = 0
                    min = 1000000.0
                    for b in range(vertCount_r):
                        t = (Vert_array[b].x - vertices[a].x)*(Vert_array[b].x - vertices[a].x) + (Vert_array[b].y - vertices[a].y)*(Vert_array[b].y - vertices[a].y) + (Vert_array[b].z - vertices[a].z)*(Vert_array[b].z - vertices[a].z)
                        t = math.sqrt(t)
                        if t < min:
                            min = t
                            index = b
                    Unknown1_w_array[original_vertices[a].index] = Unknown1_array[index]
                    Unknown2_w_array[original_vertices[a].index] = Unknown2_array[index]
                    Unknown3_w_array[original_vertices[a].index] = Unknown3_array[index]
                    Unknown4_w_array[original_vertices[a].index] = Unknown4_array[index]
                    Unknown5_w_array[original_vertices[a].index] = Unknown5_array[index]
                    
                
                
                print('**** Writing the patched section ****')
                fileWriter.writeString(Magic2)
                fileWriter.writeByte(Magic)
                fileWriter.writeInt(sectSize_w)
                fileWriter.writeInt(nsize_w)
                fileWriter.writeString(meshName)
                offset = 4 + nsize_w
                fileWriter.writeInt(0)
                fileWriter.writeInt(vertCount)
                offset = 12 + nsize_w
                fileWriter.writeInt(0)
                
                for a in range(vertCount):
                    fileWriter.writeFloat(vertices[a].x)
                    fileWriter.writeFloat(vertices[a].y)
                    fileWriter.writeFloat(vertices[a].z)
                    if Magic == 0x20:
                        fileWriter.fillZeros(0x24)
                    fileWriter.writeFloat(uvs_x[a])
                    fileWriter.writeFloat(1-uvs_y[a])
                    fileWriter.writeInt(Unknown1_w_array[a])
                    fileWriter.writeInt(Unknown2_w_array[a])
                    fileWriter.writeInt(Unknown3_w_array[a])
                    fileWriter.writeFloat(Unknown4_w_array[a])
                    fileWriter.writeFloat(Unknown5_w_array[a])
                    offset = 16 + nsize_w + (a+1)*(20) + a*(0x14)
                    
                fileWriter.writeInt(FaceCount)
                offset = offset + 0x14 + 4
                fileWriter.writeInt(0)
                for f in faces:
                    verts = f.verts
                    fileWriter.writeShort(verts[0].index)
                    fileWriter.writeShort(verts[1].index)
                    fileWriter.writeShort(verts[2].index)
                
                fileWriter.writeBinaryString(file.data[sectionStart+offsetToAdditional_r:sectionStart+sectSize])
                

                
            else:
                print('Writing the ' + Magic2 + ' section found at ' + format(sectionStart-8, '02x'))
                fileWriter.writeBinaryString(file.data[sectionStart-8: sectionStart+sectSize])
                
            
                #print("~~~~~~~~~~~~~~~~~~~~~~~~")
            
            if (file.setPointer(sectionStart+sectSize)) >= len(file):
                fileWriter.close()
                break
                        




import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator


class C3OP_Save_C3_Mesh_UI(Operator, ExportHelper):

    bl_idname = "c3op.save_c3_mesh_ui"
    bl_label = "Save C3 File"
    
    filename_ext = ".c3"
    filter_glob: StringProperty(
        default='*.c3;*.C3',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        
        C3_Operator_Model_Exporter.output_path = self.filepath
        C3_Operator_Model_Exporter.exportC3UsingRef(C3_Operator_Model_Exporter.output_path, C3_Operator_Model_Importer.c3_path)

        return {'FINISHED'}