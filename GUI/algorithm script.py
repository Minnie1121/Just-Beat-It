

# mousePress
	"""
	# normal circles:
		if clicked in that circle:
			check level
			remove circle
		elif not in that circle:
			if not within another circle:
				level = miss
				remove circle
	# long circles:
		if clicked in blue:
			circle.clickedInBlue = True
		if not clicked in blue:
			if not within another circle:
				level = miss
				remove circle
	"""

# mouseRelease
	"""
	# only deal with long circles?
	# if it's a long circle and is clickedInBlue:
		if released in the red circle:
			check level
			remove circle
		else:
			level = miss
			remove circle
	"""


# timer fired
	"""
	for all the circles:
		if the circle stays on the screen for too long:
			level = miss
			remove circle
	"""