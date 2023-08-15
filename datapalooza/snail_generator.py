import bpy
import math
import sys
import os
import csv


def make_snail(coil_fatness=.99, face_height=0.25, degree_of_coiling=12):
    # Delete all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Add a circle mesh
    bpy.ops.mesh.primitive_circle_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    circle_object = bpy.context.active_object

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


make_snail(*get_tip_states("t18"))


