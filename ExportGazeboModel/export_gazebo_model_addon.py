import os
import shutil
from glob import glob
import string

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from .templates.sdf_template import SdfTemplate
from .templates.config_template import ConfigTemplate


class ExportGazeboModel(Operator, ExportHelper):
    bl_idname = "export_gazebo_model.data"
    bl_label = "Export Gazebo Model"

    filename_ext = ""

    filter_glob: StringProperty(
        default="*",
        options={"HIDDEN"},
        maxlen=255,
    )



    def execute(self, context):
        """Execute all the operations to export a model for Gazebo 11"""

        self.base_path = bpy.path.abspath("//")
        self.model_name = bpy.path.basename(bpy.context.blend_data.filepath)[:-6]
        self.export_name = bpy.path.basename(self.filepath)

        if self.check_existing:
            """do something to avoid overwriting an already exported model"""
            pass

        self.create_folders()
        self.export_meshes()
        self.create_sdf()

        return {"FINISHED"}
    


    def create_folders(self):
        """Create the folder structure and save paths into class variables"""

        self.export_folder = os.path.join(self.base_path, self.export_name)

        self.meshes_folder = os.path.join(self.export_folder, "meshes")

        os.makedirs(self.meshes_folder, exist_ok=True)

    

    def export_meshes(self):
        """Export obj and textures"""

        filepath = os.path.join(self.meshes_folder, self.model_name + ".obj")

        # Export mesh as OBJ
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        bpy.ops.export_scene.obj(
            filepath=filepath,
            check_existing=True,
            use_mesh_modifiers=True,
            use_normals=True,
            use_uvs=True,
            use_materials=True,
            path_mode="STRIP",
            axis_forward="X",
            axis_up="Z",
        )

        # Export textures files
        unpacked = False
        for img in bpy.data.images:
            if img.source == "FILE":
                name = img.name.rstrip(string.digits + ".")
                #  if texture files are packed into the blend file
                # unpack them temporarily and pack them again
                if img.packed_file is not None:
                    unpacked = True
                    img.unpack()
                    img.pack()

                    shutil.copy2(
                        os.path.join(bpy.path.abspath("//textures"), name),
                        os.path.join(self.meshes_folder, name),
                    )
                else:
                    shutil.copy2(
                        bpy.path.abspath(img.filepath),
                        os.path.join(self.meshes_folder, name),
                    )

        # clean unpacked textures
        if unpacked:
            shutil.rmtree(bpy.path.abspath("//textures"), ignore_errors=False)



    def create_sdf(self):
        ''' Write the SDF and config files '''

        with open(os.path.join(self.export_folder, "model.sdf"), "w") as f:
            f.write(
                SdfTemplate().template.substitute(
                    {
                        "model_name": self.model_name,
                        "mesh_path": f"model://{self.export_name}/meshes/{self.model_name+'.obj'}",
                    }
                )
            )

        with open(os.path.join(self.export_folder, "model.config"), "w") as f:
            f.write(
                ConfigTemplate().template.substitute(
                    {
                        "model_name": self.model_name,
                        "author_name": "TODO",
                        "author_email": "TODO@TODO.now",
                    }
                )
            )

    

if __name__ == "__main__":
    # register()
    pass

    # test call
#    bpy.ops.export_gazebo_model.data('INVOKE_DEFAULT')
