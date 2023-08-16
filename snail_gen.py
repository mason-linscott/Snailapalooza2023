import bpy
import math
import sys
import os
import csv


# Delete all objects in the scene, including hidden ones
bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
for obj in bpy.data.objects:
    obj.select_set(True) # Select all objects, including hidden ones
bpy.ops.object.delete()

def make_snail(coil_fatness=.99, face_height=0.25, degree_of_coiling=12):
    # Delete all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Add a circle mesh
    bpy.ops.mesh.primitive_circle_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    circle_object = bpy.context.active_object
    # Rename the object to "Snail"
    circle_object.name = "Snail"

    # Offset the circle by the given value in the X-axis
    circle_object.location.x = -1

    # Add an array modifier to the circle
    array_modifier = circle_object.modifiers.new(name="Array", type='ARRAY')
    array_modifier.count = 1000

    # Uncheck relative offset
    array_modifier.use_relative_offset = False

    # Check constant offset and set the X value to 0 and Z value to the given value
    array_modifier.use_constant_offset = True
    array_modifier.constant_offset_displace[0] = 0
    array_modifier.constant_offset_displace[2] = face_height

    # Add an Empty object with Plain Axes
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(-0.96, 0, 0))
    empty_object = bpy.context.object
    empty_object.name = "Empty"

    # Rotate the Empty object by the given degrees on the X-axis
    empty_object.rotation_euler[0] = math.radians(degree_of_coiling)

    # Set the scales for X, Y, and Z to 0.99
    empty_object.scale = (0.99, coil_fatness, 0.99)

    # Find the object named "Empty" and set it as the offset object in the array modifier
    offset_object = bpy.data.objects["Empty"]
    array_modifier.use_object_offset = True
    array_modifier.offset_object = offset_object

    # Make the circle the active object
    bpy.context.view_layer.objects.active = circle_object
    circle_object.select_set(True)

    # Apply the array modifier to convert the object to a mesh
    bpy.ops.object.modifier_apply(modifier="Array")

    # Enter edit mode, select all edges, and bridge edge loops
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bridge_edge_loops()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    
        # Set the origin to the center of mass
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

# Example usage:
make_snail(coil_fatness=0.98)

def load_csv(filename):
    # Open file in read mode
    file = open(filename,"r")
    # Reading file
    lines = csv.reader(file)

    # Converting into a list
    data = list(lines)
    return data


table = load_csv("C://Users/caleb/Downloads/treedata.csv")
table = {sublist[0]: [float(i) for i in sublist[1:]] for sublist in table[1:]}

def get_tip_states(tip_label):
    return table[tip_label]





for i in range(1, 33):
    
    # Delete all objects in the scene, including hidden ones
    bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
    for obj in bpy.data.objects:
        obj.select_set(True) # Select all objects, including hidden ones
        bpy.ops.object.delete()
    
    tip_state = f"t{i}"
    render_directory = f"D:\\datapalooza\\{tip_state}"

    make_snail(*get_tip_states(tip_state))

    snail_object = bpy.data.objects["Snail"]
    snail_object.select_set(True)

    bpy.context.view_layer.objects.active = snail_object

    bpy.ops.object.toggle_cameras()

    snail_object.select_set(True)
    bpy.context.scene.place_cameras_distance = 25.0

    background_image_path = "D:\\datapalooza\\background.png"
    bpy.ops.traitblender.import_background_image(filepath=background_image_path)

    bpy.ops.object.toggle_background_planes()

    background_controls = bpy.context.scene.background_controls
    background_controls.plane_scale_x = 54
    background_controls.plane_scale_y = 54
    background_controls.plane_scale_z = 54

    bpy.ops.object.scale_background_planes()

    bpy.context.scene.background_plane_distance = 50

    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080

    plane_bottom = bpy.data.objects.get("background_plane.bottom")
    if plane_bottom:
        bpy.ops.object.light_add(type='SUN')
        sun_lamp = bpy.context.active_object
        sun_lamp.location = plane_bottom.location
        snail_obj = bpy.data.objects.get("Snail")
        if snail_obj:
            direction = snail_obj.location - sun_lamp.location
            sun_lamp.rotation_mode = 'QUATERNION'
            sun_lamp.rotation_quaternion = direction.to_track_quat('-Z', 'Y')
        plane_bottom.hide_viewport = True
        plane_bottom.hide_render = True

    snail_material = bpy.data.materials.new(name="Snail_Material")
    snail_material.diffuse_color = (0x8C / 255, 0x76 / 255, 0x56 / 255, 1)

    snail_object = bpy.data.objects.get("Snail")
    if snail_object:
        snail_object.data.materials.clear()
        snail_object.data.materials.append(snail_material)

    camera_bottom = bpy.data.objects.get("camera.bottom")
    bpy.context.scene.camera = camera_bottom

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = bpy.context.copy()
                    override['area'] = area
                    override['region'] = region
                    bpy.ops.view3d.view_camera(override)
                    break

    bpy.ops.object.select_render_directory(directory=render_directory)
    bpy.ops.object.render_all_cameras(camera_names="camera.bottom")
