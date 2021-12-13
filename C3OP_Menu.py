import bpy

class TOPBAR_MT_C3_Operator_Menu(bpy.types.Menu):
    """C3 Operator Menu"""
    bl_label = "C3 Operator"

    def draw(self, context):
        layout = self.layout
        #layout.menu("TOPBAR_MT_C3_Operator_Menu_Import", text="Import C3 File")
        layout.operator("c3op.open_c3_mesh_ui", text="Import C3 Model")
        layout.operator("c3op.open_texture_ui", text="Import Texture")
        layout.operator("c3op.open_animation_ui", text="Import C3 Animation")
        layout.operator("c3op.save_c3_mesh_ui", text="Save C3 Model")

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_C3_Operator_Menu", text = "C3 Operator")

