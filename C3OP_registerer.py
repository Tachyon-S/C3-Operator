bl_info = {
    "name": "C3 Operator",
	"description": "Import-Export C3 Files.",
	"author": "Tachyon!",
    "version": (2, 0),
    "blender": (2, 80, 0),
	"doc_url":  "TODO",
	"tracker_url": "TODO",
    "category": "Import-Export",
}


import bpy
import sys
import os

script_file = os.path.realpath(__file__)
directory = os.path.dirname(script_file)
sys.path.append(directory)

import C3OP_Model_Importer_Module
import C3OP_Model_Exporter_Module
import C3OP_Menu


def register():
    bpy.utils.register_class(C3OP_Model_Importer_Module.C3OP_Open_C3_Mesh_UI)
    bpy.utils.register_class(C3OP_Model_Importer_Module.C3OP_Open_Texture_UI)
    bpy.utils.register_class(C3OP_Model_Importer_Module.C3OP_Open_Animation_UI)
    bpy.utils.register_class(C3OP_Model_Exporter_Module.C3OP_Save_C3_Mesh_UI)
    bpy.utils.register_class(C3OP_Model_Exporter_Module.C3OP_Save_C3_With_Armature_UI)
    
    bpy.utils.register_class(C3OP_Menu.TOPBAR_MT_C3_Operator_Menu)
    	
    bpy.types.TOPBAR_MT_editor_menus.append(C3OP_Menu.TOPBAR_MT_C3_Operator_Menu.menu_draw)


def unregister():
    bpy.utils.unregister_class(C3OP_Model_Importer_Module.C3OP_Open_C3_Mesh_UI)
    bpy.utils.unregister_class(C3OP_Model_Importer_Module.C3OP_Open_Texture_UI)
    bpy.utils.unregister_class(C3OP_Model_Importer_Module.C3OP_Open_Animation_UI)
    bpy.utils.unregister_class(C3OP_Model_Exporter_Module.C3OP_Save_C3_Mesh_UI)
    bpy.utils.unregister_class(C3OP_Model_Exporter_Module.C3OP_Save_C3_With_Armature_UI)
    
    bpy.utils.unregister_class(C3OP_Menu.TOPBAR_MT_C3_Operator_Menu)
    
    bpy.types.TOPBAR_MT_editor_menus.remove(C3OP_Menu.TOPBAR_MT_C3_Operator_Menu.menu_draw)


	
	
if __name__ == "__main__":
    register()