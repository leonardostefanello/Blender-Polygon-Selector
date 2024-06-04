# -------------------- IMPORTS --------------------

import bpy

# -------------------- INFORMATION --------------------

bl_info = {
    "name": "Polygon Selector",
    "author": "Moonlight_",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "3D Viewport > Sidebar > Polygon Selector",
    "description": "Selects objects based on polygon count.",
    "doc_url": "github.com/leonardostefanello/Blender-Polygon-Selector/blob/main/README.md",
    "tracker_url": "github.com/leonardostefanello/Blender-Polygon-Selector/issues",
}

# -------------------- PROPERTIES --------------------

# Validation function for max_polycount to ensure it is not lower than min_polycount (use 0 to clear the value)
def update_max_polycount(self, context):
    if self.max_polycount != 0 and self.max_polycount < self.min_polycount:
        self.max_polycount = self.min_polycount

# Define custom properties for the scene
bpy.types.Scene.selection_mode = bpy.props.EnumProperty(
    name="Limit the object selection",
    description="Selected Mode",
    items=[
        ('VISIBLE', 'Visible', 'Select from visible objects'),
        ('SELECTED', 'Selected', 'Select from already selected objects')
    ],
    default='VISIBLE'
)

# Define custom properties for the minimal and maximal polygon count
bpy.types.Scene.min_polycount = bpy.props.IntProperty(
    name="Polycount Threshold",
    description="Select meshes above this value",
    default=10000,
    min=0
)

bpy.types.Scene.use_max_polycount = bpy.props.BoolProperty(
    name="Polygon Limit",
    description="",
    default=False
)

bpy.types.Scene.max_polycount = bpy.props.IntProperty(
    name="Polycount Limit",
    description="Limit the polygon selection to a specific value",
    default=0,
    min=0,
    update=update_max_polycount
)

bpy.types.Scene.auto_deselect = bpy.props.BoolProperty(
    name="Auto Deselect",
    description="Automatically deselect all objects before selecting them again",
    default=True
)

# -------------------- SETUP --------------------

def select_objects_by_poly_count(context):
    # Retrieve custom properties from the scene
    selection_mode = context.scene.selection_mode
    min_polycount = context.scene.min_polycount
    max_polycount = context.scene.max_polycount
    auto_deselect = context.scene.auto_deselect
    
    # Get the current view layer
    view_layer = bpy.context.view_layer

    if auto_deselect:
        bpy.ops.object.select_all(action='DESELECT')

    # Create a list to hold objects to select or deselect
    objects_to_operate = []

    # Iterate over all objects in the current view layer
    for obj in view_layer.objects:
        if obj.type == 'MESH':  # Only consider mesh objects
            poly_count = len(obj.data.polygons)

            # Check if we should limit selection to visible objects
            if selection_mode == 'VISIBLE':
                if obj.visible_get() and poly_count >= min_polycount and (not context.scene.use_max_polycount or (context.scene.use_max_polycount and (max_polycount == 0 or poly_count <= max_polycount))):
                    objects_to_operate.append(obj)

            # Check if we should limit selection to selected objects
            elif selection_mode == 'SELECTED':
                if obj.select_get():
                    if poly_count >= min_polycount and (not context.scene.use_max_polycount or (context.scene.use_max_polycount and (max_polycount == 0 or poly_count <= max_polycount))):
                        objects_to_operate.append(obj)
                    else:
                        obj.select_set(False)

    # Select or deselect the objects in the list
    for obj in objects_to_operate:
        obj.select_set(True)

    # Ensure the view layer is updated to reflect the selection changes
    bpy.context.view_layer.update()

# Define the panel
class OBJECT_PT_PolygonSelector(bpy.types.Panel):
    bl_label = "Polygon Selector"
    bl_idname = "OBJECT_PT_polygon_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Polygon Selector'

    def draw(self, context):
        layout = self.layout

        # Add limit to dropdown with label
        row = layout.row(align=True)
        subrow = row.row()
        subrow.alignment = 'RIGHT'
        subrow.label(text="Modes ")
        row.prop(context.scene, "selection_mode", text="")

        layout.prop(context.scene, "min_polycount", text="Threshold")
        
        row = layout.row(align=True)
        row.prop(context.scene, "use_max_polycount", text="", emboss=True, icon='CHECKBOX_HLT' if context.scene.use_max_polycount else 'CHECKBOX_DEHLT')
        row.prop(context.scene, "max_polycount", text="MAX >")

        # Add deselect on execute checkbox
        layout.prop(context.scene, "auto_deselect", text="Auto Deselect")

        # Add the select button
        layout.operator("object.select_by_poly_count")

# Define the operator
class OBJECT_OT_SelectByPolyCount(bpy.types.Operator):
    bl_label = "Execute Selection"
    bl_idname = "object.select_by_poly_count"
    bl_description = "Select objects by polygon count"

    def execute(self, context):
        select_objects_by_poly_count(context)
        return {'FINISHED'}

# Register and unregister the panel and operator
def register():
    # Register classes
    bpy.utils.register_class(OBJECT_PT_PolygonSelector)
    bpy.utils.register_class(OBJECT_OT_SelectByPolyCount)

def unregister():
    # Unregister Classes
    bpy.utils.unregister_class(OBJECT_PT_PolygonSelector)
    bpy.utils.unregister_class(OBJECT_OT_SelectByPolyCount)

if __name__ == "__main__":
    register()

# -------------------- END --------------------