# in playGame mode
# draw out the game


import random
from time import time
from PIL import Image, ImageTk
from tkinter import *

import sys
sys.path.append("../")
from roundHalfUp import *

def setGrid(data):
	for row in range(5):
		for col in range(5):
			data.widgets[(row, col)] = False	# no circle at this point



def drawCircle(data, canvas):
	# data.circle = ImageTk.PhotoImage(file = "pinkcircle.png")
	for row in range(5):
		for col in range(5):
			if data.widgets[(row, col)] == False:
				# mark = Label(root, image = data.circle)
				# mark.image = data.circle
				# mark.grid(row = row, column = col)
				r = 20
				data.cx = col*120 + 60
				data.cy = row*120 + 60
				data.circle = canvas.create_oval(data.cx-r, data.cy-r, data.cx+r, data.cy+r, fill="red")
				data.widgets[(row, col)] = True
				data.cir = (row, col)
				break
		if data.widgets[(row, col)] == True:
			break			# break from the whole nested for loop


def drawLongCircle(canvas, data):
	r = 10
	cx = random.randint(r, data.width-r)
	cy = random.randint(r, data.height-r)
	data.circle = canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="black")


def delCircle(data, canvas):
	# circle = root.grid_slaves(row = data.cir[0], column = data.cir[1])
	# circle.grid_remove()
	canvas.delete(data.circle)
	data.widgets[data.cir] = False


def drawBeats(data, canvas):
	beat = data.beats.pop(0)
	length = beat[1] - beat[0]
	# appear = (time()-data.songTimer) * 1000
	appear = int((data.songTimer+beat[0]) * 1000)
	if length < 1:		# press
		# appear = roundHalfUp((time()-data.songTimer)*1000)	# sec to ms
		canvas.after(appear, drawCircle(data, canvas))
		# canvas.after(appear+500, delCircle(data, canvas))
	else:				# hold
		canvas.after(appear, drawCircle(data, canvas))
		# disappear = roundHalfUp((time()-data.songTimer+length)*1000) 
					# roundHalfUp after "+length" to be more accurate
		# canvas.after(disappear, delCircle(data, canvas))
