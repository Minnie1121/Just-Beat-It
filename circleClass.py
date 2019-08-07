# Circles (superclass)

import random

class Circle(object):
	def __init__(self, time, color="blue"):
		self.r = 20
		self.time = time	# (start, end)
		self.color = color

	def draw(self, canvas, data):
		for row in range(5):
			for col in range(5):
				if data.grid[row][col] == False:
					data.grid[row][col] = True
					cx = 40 + col*data.cellW
					cy = 60 + row*data.cellH
					canvas.create_oval(cx-self.r, cy-self.r,
									   cx+self.r, cy+self.r,
									   fill = self.color)
					break
			if data.grid[row][col] == True: break

