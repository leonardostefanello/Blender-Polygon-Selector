# -------------------- IMPORTS --------------------

import bpy

# -------------------- INFORMATION --------------------

bl_info = {
    "name": "Polygon Selector",
    "author": "Moonlight_",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "category": "Select",
    "location": "View3D > Sidebar > Triangle Selector",
    "description": "Selects objects based on polygon count.",
    "doc_url": "github.com/leonardostefanello/Blender-Polygon-Selector/blob/main/README.md",
}

# -------------------- PROPERTIES --------------------

# Define custom properties for the scene
bpy.types.Scene.object_type = bpy.props.EnumProperty(
    name="Object Type",
    description="Type of objects to select",
    items=[
        ('MESH', 'Mesh', 'Mesh objects'),
        ('CURVE', 'Curve', 'Curve objects'),
        ('SURFACE', 'Surface', 'Surface objects'),
        ('META', 'Meta', 'Metaball objects'),
        ('FONT', 'Font', 'Text objects'),
        ('ARMATURE', 'Armature', 'Armature objects'),
        ('LATTICE', 'Lattice', 'Lattice objects'),
        ('EMPTY', 'Empty', 'Empty objects'),
        ('GPENCIL', 'Grease Pencil', 'Grease pencil objects'),
        ('CAMERA', 'Camera', 'Camera objects'),
        ('LIGHT', 'Light', 'Light objects'),
        ('LIGHT_PROBE', 'Light Probe', 'Light probe objects'),
        ('SPEAKER', 'Speaker', 'Speaker objects'),
        ('VOLUME', 'Volume', 'Volume objects')
    ],
    default='MESH'
)

# Define custom properties for the polycount threshold
bpy.types.Scene.poly_threshold = bpy.props.IntProperty(
    name="Poly Count Threshold",
    description="Threshold for the polygon/triangle count",
    default=10000,
    min=0
)

# -------------------- SETUP --------------------

def select_objects_by_poly_count(context):
    # Retrieve custom properties from the scene
    obj_type = context.scene.object_type
    poly_threshold = context.scene.poly_threshold
    
    # Get the current view layer
    view_layer = bpy.context.view_layer

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Iterate over all objects in the current view layer
    selected_objects = []
    for obj in view_layer.objects:
        if obj.type == obj_type:  # Check if the object matches the specified type
            poly_count = len(obj.data.polygons)
            
            # Check if the polygon count exceeds the threshold
            if poly_count > poly_threshold:
                obj.select_set(True)  # Select the object
                selected_objects.append((obj.name, poly_count))
            else:
                obj.select_set(False)  # Deselect the object
    
    # Ensure the view layer is updated to reflect the selection changes
    bpy.context.view_layer.update()

# Define the panel
class OBJECT_PT_TriangleSelector(bpy.types.Panel):
    bl_label = "Triangle Selector"
    bl_idname = "OBJECT_PT_triangle_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Triangle Selector'

    def draw(self, context):
        layout = self.layout

        # Add object type dropdown with label
        layout.label(text="Object Type:")
        layout.prop(context.scene, "object_type", text="")

        # Add poly count threshold input with label
        layout.label(text="Polycount Threshold:")
        layout.prop(context.scene, "poly_threshold", text="")

        # Add some space before the select button
        layout.separator()

        # Add the select button
        layout.operator("object.select_by_poly_count")

# Define the operator
class OBJECT_OT_SelectByPolyCount(bpy.types.Operator):
    bl_label = "Select"
    bl_idname = "object.select_by_poly_count"
    bl_description = "Select objects by polygon count"

    def execute(self, context):
        select_objects_by_poly_count(context)
        return {'FINISHED'}

# Register and unregister the panel and operator
def register():
    # Register classes
    bpy.utils.register_class(OBJECT_PT_TriangleSelector)
    bpy.utils.register_class(OBJECT_OT_SelectByPolyCount)

def unregister():
    # Unregister Classes
    bpy.utils.unregister_class(OBJECT_PT_TriangleSelector)
    bpy.utils.unregister_class(OBJECT_OT_SelectByPolyCount)

if __name__ == "__main__":
    register()

# -------------------- END --------------------
