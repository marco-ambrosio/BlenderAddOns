"""
This script will setup Renderer and Compositing node to export Scene with Depth and Segmentation based on Object Pass Indexes
"""
import bpy

bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480

# Enable use of nodes in the compositor
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

# Enable Depth and Object Index passes
view_layer = bpy.context.scene.view_layers["ViewLayer"]
view_layer.use_pass_z = True  # Enable Depth pass
view_layer.use_pass_object_index = True  # Enable Object Index pass

# Clear existing nodes
for node in tree.nodes:
    tree.nodes.remove(node)

# Create Render Layers node
render_layers = tree.nodes.new(type="CompositorNodeRLayers")
render_layers.location = (-400, 0)

# Create Composite node
composite = tree.nodes.new(type="CompositorNodeComposite")
composite.location = (400, 100)
composite.use_alpha = True

# Create File Output node
file_output = tree.nodes.new(type="CompositorNodeOutputFile")
file_output.location = (400, -100)

# Add multiple file outputs (Image, Depth, and one Segment output)
file_output.file_slots.clear()  # Clear existing slots if any
file_output.file_slots.new("Image")   # Output for Image
file_output.file_slots.new("Depth")   # Output for Depth
file_output.file_slots.new("Segmentation") # Output for Object Index (Segmentation)

# Change Depth output format to OpenEXR
file_output.file_slots["Depth"].use_node_format = False
file_output.file_slots["Depth"].format.file_format = 'OPEN_EXR'
file_output.file_slots["Depth"].format.color_mode = 'RGB'
file_output.file_slots["Depth"].format.color_depth = '16'

# Change Segmentation output format to OpenEXR
file_output.file_slots["Segmentation"].use_node_format = False
file_output.file_slots["Segmentation"].format.file_format = 'OPEN_EXR'
file_output.file_slots["Segmentation"].format.color_mode = 'RGB'
file_output.file_slots["Segmentation"].format.color_depth = '16'

## Create Divide Math node for normalizing depth
#divide_node = tree.nodes.new(type="CompositorNodeMath")
#divide_node.operation = 'DIVIDE'
#divide_node.inputs[1].default_value = 255.0
#divide_node.location = (0, -200)

# Link nodes
links = tree.links
links.new(render_layers.outputs["Image"], composite.inputs["Image"])  # Image to Composite
links.new(render_layers.outputs["Image"], file_output.inputs[0])  # Image to File Output
links.new(render_layers.outputs["Depth"], file_output.inputs[1])  # Depth to File Output

# Link Object Index (Segmentation)
links.new(render_layers.outputs["IndexOB"], file_output.inputs[2])  # Segment (Object Index)

# Demo - Render one frame
# import os
# file_output.base_path = os.path.expanduser(os.path.join("~", "OneDrive", "Desktop", "prova"))
# bpy.ops.render.render(write_still=True)