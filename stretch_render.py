import bpy
from bpy.types import (Panel, Operator)
import os

os.system("cls") # Clear console


bl_info = {
	"name": "Stretch Render",
	"description": "Alternative rendering compression method.",
	"author": "CrunchyDuck <realvulpes@gmail.com>",
	"version": (0, 1, 1),
	"blender": (2, 83, 0),
	"category": "Render",
	"location": "Operator Search"
}

# Thanks to Arix for guiding and motivating me. Visit his cute website at arix.cc where he talks about cool stuff he's been doing.

# I'm quite new to python (This is but my second project so far), so please give me some critique with examples if you look through my code! You can contact me on Discord as CrunchyDuck#2278
# On top of this, I am also quite new to animation in Blender. There's many things like NLA that I have never even touched, so there's a high chance I've missed something I need to store. Please alert me if I have!
class RENDER_OT_stretch_render(Operator):
	"""please don't crash"""
	bl_idname = "render.stretch_render"
	bl_label = "Stretch Render"

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
		empty_frames = [i for i in range(start_frame, end_frame + 1)] # This will store a list of all frames in the animation. We will then compare our animations to see which frames aren't empty. By the end of it, we will have an array containing only the unreserved frames.
		render_frames = empty_frames.copy()
		empty_frames.pop(0) # Since we'll always need to render the very first frame of an animation, we can remove it immediately.


		# Search through all layers in this scene for any activated actions.
		for i in children_layers:
			layer_actions = self.parse_layer(i)
			active_actions = active_actions + layer_actions

		empty_frames = self.parse_actions(active_actions, empty_frames)
		render_frames = list(set(render_frames) - set(empty_frames)) # The frames we want to render are just the inverse of the frames we don't want to render.

		self.output(empty_frames, total_frames) # Print out the report of the render.

		return {"FINISHED"}

	def parse_layer(self, layer_wrapper):
		"""Search through the given layer and store any objects found that're visible."""
		collection = layer_wrapper.collection  # The collection this wrapper contains.
		layer_collection_children = layer_wrapper.children # Index any layers within this object.
		actions = []  # We'll return this so it can be parsed outside of this function.

		# Check objects within this layer.
		if layer_wrapper.is_visible:  # If the layer is set to be invisible, then none of the OBJECTS inside of it can render. Other layers contained may still render, however.
			collection_objects = collection.objects

			# Cycle through all objects stored within this collection.
			for object in collection_objects:
				if object is None: # Not sure if this can happen, but might as well be safe.
					continue

				if object.hide_render:  # If the object is invisible, then move on to the next object.
					continue

				# Check the object for animation
				object_animation = object.animation_data
				if object_animation is not None: # Does this object have any animation at all?
					object_action = object_animation.action
					if object_action is not None: # If this object doesn't have an action, ignore it.
						actions.append(object_action)

				# Check the object's data block for animation.
				if object.data is not None:
					data_animation = object.data.animation_data # I'm not sure on all of the locations animation data can be stored, but I've found instances of it being stored in the data of an object.
					if data_animation is not None: # Does this object have any animation at all?
						data_action = data_animation.action
						if data_action is not None: # If this object doesn't have an action, ignore it.
							actions.append(data_action)

		for i in layer_collection_children:
			actions = actions + self.parse_layer(i)

		return(actions)

	def output(self, empty_frames, total_frames):
		"""Report the results of stretch render."""
		num_removed = len(empty_frames)
		percent_removed = round((num_removed / total_frames) * 100, 2)

		print("Number of frames free frames: {0}".format(num_removed))
		print("Percent of animation removed: {0}%".format(percent_removed))

	def parse_actions(self, actions_array, blank_array):
		"""Search through all of the provided actions."""
		empty_frames = blank_array
		# Search through the F-curves of the active actions and figure out where their "empty" space is, then index that empty space to compare against other f-curves
		for action in actions_array: # Maybe I should check if f_curves and keyframe are None?
			for fcurve in action.fcurves:
				number_of_keyframes = len(fcurve.keyframe_points)
				for iterator, keyframe in enumerate(fcurve.keyframe_points):
					keyframe_frame = int(keyframe.co[0])
					interp = keyframe.interpolation  # If the interpolation is anything besides constant, that means all frames between this one and the next are reserved.
					curr_y = keyframe.co[1]  # The y position of this keyframe. If it matches another keyframe, it and all frames between should be the same.

					if iterator < number_of_keyframes - 1:  # Only try to check the next keyframe if we're not at the end of the array, so we don't get indexing issues.
						next_keyframe = fcurve.keyframe_points[iterator + 1]
						next_keyframe_frame = int(next_keyframe.co[0])
						next_y = next_keyframe.co[1]  # Y position for the next keyframe. If this matches the current y position, then the frames are the same and interpolation shouldn't matter.

						if not (curr_y is next_y):
							if interp != "CONSTANT":  # If the interpolation isn't constant, we'll render all frames after this keyframe until the next keyframe.
								frames_to_render = [x for x in range(keyframe_frame + 1, next_keyframe_frame + 1)]
								print("Keyframe on action {0}, curve {1}, frame {2} is animated without CONSTANT interpolation.".format(action.name, fcurve.data_path, str(keyframe_frame)))  # I want to output these to a file in the future so that people can see what they might not have set up properly.
							else:  # If it is set to constant, we only need to mark the next frame for change.
								frames_to_render = [next_keyframe_frame]

							empty_frames = list(set(empty_frames) - set(frames_to_render))
							# A little note on optimization as of writing this. I need to find the difference between two arrays: One array which will contain all numbers from start to end, and another array which will contain random numbers within.
							# There seems to be ten dozen ways to do this, using sets, removing individual numbers, using the numpy.unique function. As of right now, I have no way of benchmarking these functions and do not know which is the fastest.
		return empty_frames


class VIEW3D_PT_stretch_render(Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Stretch Render"
	bl_label = "Path Select"

	def draw(self, context):
		layout = self.layout
		col = layout.column(align=True)
		col.prop(context.scene, "stretch_render_location")
		layout.operator("render.stretch_render")




blender_classes = [
	VIEW3D_PT_stretch_render,
	RENDER_OT_stretch_render
]


def register():
	bpy.types.Scene.stretch_render_location = bpy.props.StringProperty(
		name=".fox Output",
		subtype="DIR_PATH",
		default="//",
		description="Where the file containing the duration of each frame will be output, to be used in decompression."
	)
	for blend_class in blender_classes:
		bpy.utils.register_class(blend_class)


def unregister():
	del bpy.types.Scene.stretch_render_location
	for blend_class in blender_classes:
		bpy.utils.unregister_class(blend_class)


if __name__ == "__main__":
	register()




# CONSIDERATIONS:
# Absolutely warn the user that they need to create a duplicate blender file to use this, otherwise I'm going to squish all of their animations.
# I will have to figure out how to get this to work when you have physics animations within your scene. Likely, this will work based off of them being activated/deactivated, but I will need to test further. (Maybe force the user to bake it?)
# Speed, I am almost certainly not going to be able to optimize this on my own, and I will need to see if speed of my operations is a major concern.
# Check to make sure that this works with more than one scene.
# I should allow my code to "print" a log that specifies the location of any non-constant animations.
# Add checks for animations that are not tied to objects (E.G grease pencil animation)

