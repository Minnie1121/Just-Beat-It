# Elongated circle (subclass)
# not sure about how to set the "tuning point" of the tail 
# (i'll call it tx, ty now) might can be calculated by length/cx/cy...
# length = length of that beat

from circleClass import *

class ElongatedCircle(Circle):
	def __init__(self, cx, cy, r, length, tx, ty, color="red"):
		super.__init(cx, cy, r, color)
		self.cx, self.cy = cx, cy
		self.r = r
		self.length = length
		self.tx, self.ty = tx, ty
		self.color = color
