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
		active_items_in_scene = "" # This should collect all THINGS with a key frame on them. I don't know how I will check for keyframes for things such as render settings, however.
			# I might be able to use the list of "actions"?
		animation_frames = 0

		for i in range(animation_frames):
			if animation_on_this_frame:
				pass
				# Check each animation to make sure it is set to CONSTANT interpolation. If it is, we can save a "stretch" of this frame.
			else:
				pass
				# If any are found to not be constant, we will have to check what the item with the longest interpolation is, and then simply "skip" ahead that amount as we can't cut anything out in that case.
				# Since I'm going to be creating a new .blend file to store this new version of the animation in, I will still need to "save" all of the animations stored between the two points.



		return {"FINISHED"}



if __name__ == "__main__":
	register()