from string import Template

class SdfTemplate:
    template = Template(
        """\
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
    """
    )