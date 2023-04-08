# BlenderAddOns

This is a collection of Blender AddOns I've written. They are all licensed under the MIT license.

## Installation

Compress the folder of the desired add-on in a .zip file. In Blender, go to `Edit - Preferences - Add-ons - Install...` and select the .zip file.

## AddOns

- [ExportGazeboModel](#ExportGazeboModel)

### ExportGazeboModel

This AddOn allows you to export a Blender model to a Gazebo model. It is a work in progress, but it is functional. 

Once installed, the AddOn is available in the `File - Export` menu.

It exports the model to a directory with the same name of the file ready to be used in a Gazebo model folder.

Meshes are exported as .obj, textures are saved in the meshes folder and are used by the .mtl file.

