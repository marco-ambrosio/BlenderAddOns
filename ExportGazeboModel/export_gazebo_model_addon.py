bl_info = {
    "name": "Export Gazebo Model",
    "blender": (3, 3, 0),
    "category": "Import-Export",
}


import os
import shutil
from glob import glob
from string import Template
import string

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ConfigTemplate:
    
    template = Template(
    '''\
<?xml version="1.0" ?>
<model>
    <name>${model_name}</name>
    <version>1.0</version>
    <sdf version="1.6">model.sdf</sdf>
    <author>
        <name>${author_name}</name>
        <email>${author_email}</email>
    </author>
    <description></description>
</model>\
    ''')
    
    
class SdfTemplate:
    
    template = Template(
    '''\
<?xml version='1.0'?>
<sdf version="1.6">
  <model name="${model_name}">
    <link name='link'>
      <pose>0 0 0 0 0 0</pose>
      <gravity>1</gravity>
      <self_collide>0</self_collide>
      <kinematic>0</kinematic>
      <enable_wind>0</enable_wind>
      <visual name='visual'>
        <pose>0 0 0 0 0 0</pose>
        <geometry>
          <mesh>
            <uri>${mesh_path}</uri>
          </mesh>
        </geometry>
        <transparency>0</transparency>
        <cast_shadows>1</cast_shadows>
      </visual>
      <collision name='collision'>
        <laser_retro>0</laser_retro>
        <max_contacts>10</max_contacts>
        <pose>0 0 0 0 0 0</pose>
        <geometry>
          <mesh>
            <uri>${mesh_path}</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    <static>1</static>
    <allow_auto_disable>1</allow_auto_disable>
  </model>
</sdf>\
    ''')

class GazeboModel:
    
    def export(self, overwrite):
        ''' Execute all the operations to export a model for Gazebo 11 '''
        
        self.base_path = bpy.path.abspath('//')
        self.model_name = bpy.path.basename(bpy.context.blend_data.filepath)[:-6]
        if not overwrite:
            ''' do something to avoid overwriting an already exported model '''
            pass
        
        self.create_folders()
        self.export_meshes()
        self.create_sdf()
        
        return {'FINISHED'}
    
    def create_folders(self):
        ''' Create the folder structure and save paths into class variables '''
        
        self.model_folder = os.path.join(
            self.base_path, self.model_name)
            
        self.meshes_folder = os.path.join(
            self.model_folder, 'meshes')
            
        os.makedirs(self.meshes_folder, exist_ok=True)
        
    
    def export_meshes(self):
        ''' Export obj and textures '''
        
        filepath = os.path.join(
            self.meshes_folder, self.model_name + '.obj')
        
        # Export mesh as OBJ
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.export_scene.obj(
            filepath=filepath,
            check_existing=True,
            use_mesh_modifiers=True,
            use_normals=True,
            use_uvs=True,
            use_materials=True,
            path_mode='STRIP',
            axis_forward='X',
            axis_up='Z')
        
        # Export textures files
        unpacked = False
        for img in bpy.data.images:
            if img.source == 'FILE':
                name = img.name.rstrip(string.digits + '.')
                if img.packed_file is not None:
                    unpacked = True
                    img.unpack()
                    img.pack()
                    
                    shutil.copy2(
                        os.path.join(bpy.path.abspath('//textures'), name),
                        os.path.join(self.meshes_folder, name))   
                else:
                    shutil.copy2(
                        bpy.path.abspath(img.filepath),
                        os.path.join(self.meshes_folder, name))

        # clean unpacked textures
        if unpacked:
            shutil.rmtree(bpy.path.abspath('//textures'), ignore_errors=False)
            

            
    
    def create_sdf(self):

        with open(os.path.join(
            self.model_folder, 'model.sdf'), 'w') as f:
            
            f.write(SdfTemplate().template.substitute({
                "model_name": self.model_name,
                "mesh_path": f"model://{self.model_name}/meshes/{self.model_name+'.obj'}",
             }))
                         
                
        with open(os.path.join(
            self.model_folder, 'model.config'), 'w') as f:
            
             f.write(ConfigTemplate().template.substitute({
                "model_name": self.model_name,
                "author_name": "TODO",
                "author_email": "TODO@TODO.now"
             }))
             

class ExportGazeboModel(Operator, ExportHelper):
    
    bl_idname = 'export_gazebo_model.data'
    bl_label = "Export Gazebo Model"
    
    filename_ext = '.sdf'
    
    filter_glob: StringProperty(
        default='*',
        options={'HIDDEN'},
        maxlen=255,
    )
    
    overwrite: BoolProperty(
        name="Overwrite Existing",
        description="Overwrite an existing model with the same name",
        default=True,
    )
    
    def execute(self, context):
        gazebo_model = GazeboModel()        
        return gazebo_model.export(self.overwrite)
    


def menu_func_export(self, context):
    self.layout.operator(ExportGazeboModel.bl_idname, text="Export Gazebo Model (.sdf, .obj)")
    

def register():
    bpy.utils.register_class(ExportGazeboModel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportGazeboModel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)



if __name__ == "__main__":
    register()
    

    # test call
#    bpy.ops.export_gazebo_model.data('INVOKE_DEFAULT')

