# Circles (superclass)

import random


def distance(x0, y0, x1, y1):
	return ((x0-x1)**2 + (y0-y1)**2) ** 0.5

def getCoor(data, row, col):
	cx = 40 + col*data.cellW + 1/2*data.cellW
	cy = 60 + row*data.cellH + 1/2*data.cellH
	return (cx, cy)


class Circle(object):
	def __init__(self, timestamp, timer, color="blue"):
		self.r = 28
		self.timestamp = timestamp	# (start, end)
		# self.timer = timer		# for how long the circle has stayed (starts from 0)
		self.color = color
		self.row = random.randint(0, 4)
		self.col = random.randint(0, 4)
		self.cx = 0
		self.cy = 0

		# for the attached circle
		self.othercx = 0
		self.othercy = 0
		self.isClickedInBlue = False


	def isLongCir(self):
		return (self.timestamp[1]-self.timestamp[0]) > 1

	def draw(self, canvas, data):
		while data.grid[self.row][self.col] == True:
			self.row = random.randint(0, 4)
			self.col = random.randint(0, 4)
		self.cx, self.cy = getCoor(data, self.row, self.col)
		canvas.create_oval(self.cx-self.r, self.cy-self.r,
						   self.cx+self.r, self.cy+self.r,
						   fill = self.color)
		data.grid[self.row][self.col] = True

		# draw another circle attached to the longCir
		length = self.timestamp[1] - self.timestamp[0]
		if self.isLongCir():
			for row in range(5):
				for col in range(5):
					if data.grid[row][col] == False:	# if there's no cir
						data.grid[row][col] = True
						self.othercx, self.othercy = getCoor(data, row, col)
						break
			canvas.create_oval(self.othercx-self.r, self.othercy-self.r,
							   self.othercx+self.r, self.othercy+self.r,
							   fill = "red")
			canvas.create_line(self.cx, self.cy, self.othercx, self.othercy,
							   fill = "purple")


	def clickedIn(self, x, y):
		return distance(self.cx, self.cy, x, y) <= self.r

	# check if the mouse is released within red circle
	def releasedIn(self, x, y):
		return distance(self.othercx, self.othercy, x, y) <= self.r

	def __repr__(self):
		return "*!*%s %s" % (str(self.timestamp[0]), str(self.timestamp[1]))


"""
def drawGrid(canvas, data):
	for row in range(5):
		for col in range(5):
			canvas.create_rectangle(40+col*data.cellW, 60+row*data.cellH,
									40+(col+1)*data.cellW, 60+(row+1)*data.cellH,
									width = 2)
"""
