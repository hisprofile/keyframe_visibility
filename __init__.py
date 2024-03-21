bl_info = {
    "name" : "Keyframe Visibility",
    "description" : "Use operators to toggle and keyframe visibility.",
    "author" : "hisanimations",
    "version" : (1, 0, 0),
    "blender" : (3, 0, 0),
    "location" : "Object > Keyframe Visibility",
    "support" : "COMMUNITY",
    "category" : "3D View",
}
import bpy

def ToggleHide(a, b, c):
    scn = bpy.context.scene
    a.hide_viewport = not b
    a.hide_render = not b
    if bpy.context.scene.show_subframe:
        frame = scn.frame_float
    else:
        frame = scn.frame_current
    a.keyframe_insert(data_path='hide_viewport', frame=frame+c)
    a.keyframe_insert(data_path='hide_render', frame=frame+c)
    a.hide_render = False
    a.hide_viewport = False
    
class KEYVIS_OT_SHOWHIDE(bpy.types.Operator):
    bl_idname = 'keyvis.showhide'
    bl_label = 'Show Now, Hide Next'
    bl_description = 'Show now, hide next frame'
    bl_options = {'UNDO'}
    
    def execute(self, context):
        for i in bpy.context.selected_objects:
            ToggleHide(i, True, 0)
            ToggleHide(i, False, 1)
        
        return {'FINISHED'}

class KEYVIS_OT_HIDESHOW(bpy.types.Operator):
    bl_idname = 'keyvis.hideshow'
    bl_label = 'Hide Before, Show Now'
    bl_description = 'Hide before frame, show now'
    bl_options = {'UNDO'}
    
    def execute(self, context):
        for i in bpy.context.selected_objects:
            ToggleHide(i, False, -1)
            ToggleHide(i, True, 0)
        return {'FINISHED'}
    
class KEYVIS_MT_Menu(bpy.types.Menu):
    bl_label = 'Keyframe Visibility'
    bl_idname = 'VIEW3D_MT_keyvis'
    
    def draw(self, context):
        layout = self.layout
        layout.row().operator('keyvis.hideshow')
        layout.row().operator('keyvis.showhide')
        
def menu_keyvis(self, context):
    #self.layout.menu(KEYVIS_MT_Menu.bl_idname)
    layout = self.layout
    row = layout.row()
    row.operator('keyvis.hideshow', icon='RESTRICT_RENDER_OFF')
    row = layout.row()
    row.operator('keyvis.showhide', icon='RESTRICT_RENDER_ON')
    
classes = [KEYVIS_OT_SHOWHIDE, KEYVIS_OT_HIDESHOW, KEYVIS_MT_Menu]

def register():
    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.VIEW3D_MT_object_showhide.append(menu_keyvis)
    
def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
    bpy.types.VIEW3D_MT_object_showhide.remove(menu_keyvis)
        
if __name__ == '__main__':
    register()
