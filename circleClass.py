# Circles (superclass)

class Circle(object):
	def __init__(self, cx, cy, time, color="blue"):
		self.cx = cx
		self.cy = cy
		self.r = 8
		self.time = time
		self.color = color

	def draw(self, canvas, data):
		self.cx = random.randint(self.r, data.width-self.r)
		self.cy = random.randint(self.r, data.height-self.r)
		canvas.create_oval(self.cx-self.r, self.cy-self.r,
							self.cx+self.r, self.cy+self.r,
							fill = self.color)
