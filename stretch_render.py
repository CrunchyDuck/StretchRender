import bpy

bl_info = {
	"name": "Stretch Render",
	"description": "Alternative rendering compression method.",
	"author": "CrunchyDuck <realvulpes@gmail.com>",
	"version": (0, 1, 1),
	"blender": (2, 83, 0),
	"category": "Render",
	"location": "Operator Search"
}

def register():
	bpy.utils.register_class(RENDER_OT_stretch_render)

def unregister():
	bpy.utils.unregister_class(RENDER_OT_stretch_render)


# Thanks to Arix for guiding and motivating me. Visit his cute website at arix.cc where he talks about cool stuff he's been doing.

# I'm quite new to python (This is but my second project so far), so please give me some critique with examples if you look through my code! You can contact me on Discord as CrunchyDuck#2278
# On top of this, I am also quite new to animation in Blender. There's many things like NLA that I have never even touched, so there's a high chance I've missed something I need to store. Please alert me if I have!
class RENDER_OT_stretch_render(bpy.types.Operator):
	"""please don't crash"""
	bl_idname = "render.stretch_render"
	bl_label = "Stretch Render"

	# THIS IS BASICALLY PSEUDO CODE RIGHT NOW!
	# This code is written while tired, busy, and unfocused. It is just to lay out an idea on what I should do when I return.
	def execute(self, context):
		print("-------------------------------\nEXECUTING STRETCH RENDER")
		target_scene = bpy.context.scene
		start_frame = target_scene.frame_start
		end_frame = target_scene.frame_end
		total_frames = end_frame - start_frame

		target_layer = bpy.context.view_layer
		layer_collection_master = target_layer.layer_collection # Get the "main" layer collection. Note that a layer collection is a wrapper that goes around a collection.
		children_layers = layer_collection_master.children

		active_actions = []  # A list of all actions This should collect a directory of all animations.
			# So for now, I'm going to ignore any animations that AREN'T tied to an object, E.G animations on the scene. As of right now, I can't think of any situations where these changes would actually change how the screen *looks*.
		empty_frames = [i for i in range(total_frames)] # This will store a list of all frames in the animation. We will then compare our animations to see which frames aren't empty. By the end of it, we will have an array containing only the unreserved frames.


		# Search through all layers in this scene for any activated actions.
		for i in children_layers:
			layer_actions = self.parse_layer(i)
			active_actions = active_actions + layer_actions


		# Search through the F-curves of the active actions and figure out where their "empty" space is, then index that empty space to compare against other f-curves
		for i in active_actions:
			f_curve = i.fcurves # An action contains an "F_curve" for each line of animation, E.G one for X, Y, and Z position.

			# Maybe I should check if f_curves and keyframe are None?
			for j in f_curve:
				keyframe = j.keyframe_points

				for ii in keyframe:
					keyframe_frame = ii.co[0]
					interp = ii.interpolation # If the interpolation is anything besides constant, that means all frames between this one and the next are reserved.

					if interp != "CONSTANT": # I couldn't get comparing enums to work so I'm comparing strings instead. Whoops.
						print("Keyframe on action " + i.name + ", curve " + j.data_path + ", frame " + str(keyframe_frame) + " is set to interpolation type " + str(interp) + " and not CONSTANT.")






		return {"FINISHED"}

	def parse_layer(self, layer_wrapper):
		"""Search through the given layer and store any objects found that're visible."""
		collection = layer_wrapper.collection  # The collection this wrapper contains.
		layer_collection_children = layer_wrapper.children # Index any layers within this object.
		actions = []  # We'll return this so it can be parsed outside of this function.

		# Check objects within this layer.
		if layer_wrapper.is_visible:  # If the layer is set to be invisible, then none of the OBJECTS inside of it can render. Other layers contained may still render, however.
			collection_objects = collection.objects
			if layer_wrapper.name == "Houses":
				for i in collection_objects:
					print(i.name)

			# Cycle through all objects stored within this collection.
			for j in collection_objects:
				if j.hide_render:  # If the object is invisible, then move on to the next object.
					continue

				# Collect animation data about this object. AS FAR AS I KNOW, objects can only have one action each, therefore I can simply take the single action, and store that.
				object_animation = j.animation_data
				if object_animation is None: # Does this object have any animation at all?
					continue

				object_action = object_animation.action
				if object_action is None: # If this object doesn't have an action, ignore it.
					continue

				actions.append(object_action)

		for i in layer_collection_children:
			self.parse_layer(i)

		return(actions)



if __name__ == "__main__":
	register()




# CONSIDERATIONS:
# Absolutely warn the user that they need to create a duplicate blender file to use this, otherwise I'm going to squish all of their animations.
# I will have to figure out how to get this to work when you have physics animations within your scene. Likely, this will work based off of them being activated/deactivated, but I will need to test further. (Maybe force the user to bake it?)
# Speed, I am almost certainly not going to be able to optimize this on my own, and I will need to see if speed of my operations is a major concern.
# Check to make sure that this works with more than one scene.
# I should allow my code to "print" a log that specifies the location of any non-constant animations.
