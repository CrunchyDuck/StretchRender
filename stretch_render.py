import bpy

bl_info = {
	"name": "Stretch Render",
	"description": "Alternative rendering compression method.",
	"author": "CrunchyDuck <realvulpes@gmail.com>",
	"version": (0, 1),
	"blender": (2, 83, 0),
	"category": "Render",
	"location": "Operator Search"
}

def register():
	bpy.utils.register_class(RENDER_OT_stretch_render)

def unregister():
	bpy.utils.unregister_class(RENDER_OT_stretch_render)


# I'm quite new to python (This is but my second project so far), so please give me some critique with examples if you look through my code! You can contact me on Discord as CrunchyDuck#2278
class RENDER_OT_stretch_render(bpy.types.Operator):
	"""please don't crash"""
	bl_idname = "render.stretch_render"
	bl_label = "Stretch Render"

	# THIS IS BASICALLY PSEUDO CODE RIGHT NOW!
	# This code is written while tired, busy, and unfocused. It is just to lay out an idea on what I should do when I return.
	def execute(self, context):
		target_scene = ""
		active_items_in_scene = ""


		for i in range(len(active_items_in_scene)):
			current_object = active_items_in_scene[i]
			object_keyframes = active_items_in_scene.keyframes


		return {"FINISHED"}



if __name__ == "__main__":
	register()