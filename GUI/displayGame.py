# construct and display the whole window

import random
import time
from tkinter import *
from pygame import mixer
from tkinter import filedialog
from tkinter import *

import sys
sys.path.append("../")
from roundHalfUp import *
from circleClass import *


####################################
# init
####################################

def init(data):
	data.mode = "selectSong"
	data.beats = []		# tuple (press, release)
	data.press = 0		# at what time the key was pressed (time())
	data.songStart = 0	# when did the song start to play
	data.isPressed = False
	data.songTimer = 0
	data.startGame = False
	data.timer = 0

	data.rows = 5
	data.cols = 5
	data.cellW = (data.width-80) / 5
	data.cellH = (data.height-100) / 5
	data.grid = [ [False] * 5 for row in range(5) ]

	data.circles = []


####################################
# mode dispatcher
####################################

def mousePressed(event, data):
	if (data.mode == "selectSong"): selectSongMousePressed(event, data)
	elif (data.mode == "tapBeats"): tapBeatsMousePressed(event, data)
	elif (data.mode == "playGame"): playGameMousePressed(event, data)

def keyPressed(event, data):
	if (data.mode == "selectSong"): selectSongKeyPressed(event, data)
	elif (data.mode == "tapBeats"): tapBeatsKeyPressed(event, data)
	elif (data.mode == "playGame"): playGameKeyPressed(event, data)

def keyRelease(event, data):
	if (data.mode == "selectSong"): selectSongKeyRelease(event, data)
	elif (data.mode == "tapBeats"): tapBeatsKeyRelease(event, data)
	elif (data.mode == "playGame"): playGameKeyRelease(event, data)

def timerFired(data):
	if (data.mode == "selectSongTimerFired"): selectSongTimerFired(data)
	elif (data.mode == "tapBeats"): tapBeatsTimerFired(data)
	elif (data.mode == "playGame"): playGameTimerFired(data)


def redrawAll(canvas, data):
	if (data.mode == "selectSong"): selectSongRedrawAll(canvas, data)
	elif (data.mode == "tapBeats"): tapBeatsRedrawAll(canvas, data)
	elif (data.mode == "playGame"): playGameRedrawAll(canvas, data)



####################################
# selectSong mode
####################################

def browseFile():
	global fileName
	fileName = filedialog.askopenfilename(filetypes = [("WAV file", "*.wav")])


def selectSongMousePressed(event, data):
	pass

def selectSongKeyPressed(event, data):
	if (event.keysym == 's'):
		browseFile()
		data.mode = "tapBeats"

def selectSongKeyRelease(event, data):
	pass

def selectSongTimerFired(data):
	pass

def selectSongRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2-20,
						text="Select a song you like!", font="Arial 26 bold")
	# might turn it into a button
	canvas.create_text(data.width/2, data.height/2+20,
                       text="Press 's' to select", font="Arial 20")


####################################
# tapBeats mode
####################################

def tapBeatsMousePressed(event, data):
	pass

def tapBeatsKeyPressed(event, data):
	if not mixer.music.get_busy():
		if event.keysym == "m":
			mixer.music.load(fileName)
			mixer.music.play()
			data.songStart = time.time()
		elif event.keysym == "s" and data.beats != []:
			data.mode = "playGame"
	else:
		if event.keysym == "space" and not data.isPressed:
			data.isPressed = True
			data.press = time.time()

def tapBeatsKeyRelease(event, data):
	if data.isPressed and mixer.music.get_busy():
		now = time.time()
		timestamp = (data.press-data.songStart, now-data.songStart)
		data.beats.append(timestamp)
		print(timestamp)
		data.circles.append(Circle(timestamp))
	data.isPressed = False

def tapBeatsTimerFired(data):
	pass

def tapBeatsRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2-20,
						text="Tap your beats!", font="Arial 26 bold")
	# might turn it into a button
	canvas.create_text(data.width/2, data.height/2+50,
                       text="Press 'm' to start music\nPress 'space' to create your beats\nPress 's' to start the game", font="Arial 20")


####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
	if not data.startGame:
		if 0 < event.x < data.width and 0 < event.y < data.height:
			data.startGame = True
			data.songTimer = time.time()	# sec; when the music (game) starts
			mixer.music.load(fileName)
			mixer.music.play()

def playGameKeyPressed(event, data):
	pass

def playGameKeyRelease(event, data):
	pass

def playGameTimerFired(data):
	pass

def playGameRedrawAll(canvas, data):
	drawGrid(canvas, data)
	canvas.create_text(data.width/2, 20, font="Arial 20",
					   text="click anywhere to start game")
	if data.startGame and mixer.music.get_busy():
		if len(data.circles) > 0:
			timeSinceStart = time.time() - data.songTimer
			circle = data.circles[0]
			print("timeSinceStart:", timeSinceStart)
			print("circle.time:", circle.time[0])
			if 0 <= (timeSinceStart-circle.time[0]) <= 0.1:
				circle.draw(canvas, data)
				data.circles.pop(0)







# run function from 15-112 course note
# http://www.kosbie.net/cmu/fall-16/15-112/notes/notes-animations-examples.html

def run(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyReleaseWrapper(event, canvas, data):
		keyRelease(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds
	init(data)

    # create the root and the canvas
    # root = Tk() in buttons.py
	root = Tk()
	root.title("Just Beat It!")
	mixer.init()

	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind('<KeyPress>', lambda event:
							keyPressedWrapper(event, canvas, data))
	root.bind('<KeyRelease>', lambda event: 
							keyReleaseWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
    # and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(600, 600)