bl_info = {
    "name": "Export Gazebo Model",
    "version": (0, 1, 0),
    "blender": (3, 3, 0),
    "category": "Import-Export",
}

import bpy
from .export_gazebo_model_addon import ExportGazeboModel

def menu_func_export(self, context):
    self.layout.operator(
        ExportGazeboModel.bl_idname, text="Gazebo Model (.sdf, .obj)"
    )

def register():
    bpy.utils.register_class(ExportGazeboModel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportGazeboModel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)