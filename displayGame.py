# construct and display the whole window

import random
import time
import threading
from tkinter import *
from pygame import mixer
from tkinter import filedialog
import sys
# sys.path.append("../")
# from circleClass import *


####################################
# init
####################################

def init(data):
	data.mode = "selectSong"
	data.beats = []		# tuple (press, release)
	data.press = 0		# at what time the key was pressed (time.time())
	data.songStart = 0	# when did the song start to play
	data.isPressed = False
	data.songTimer = 0
	data.startGame = False
	data.timer = 0		# count down 3 and the game starts

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
	elif (data.mode == "playGame"): playGameTimerFired(event, data)


def redrawAll(canvas, data):
	if (data.mode == "selectSong"): selectSongRedrawAll(canvas, data)
	elif (data.mode == "tapBeats"): tapBeatsRedrawAll(canvas, data)
	elif (data.mode == "playGame"): playGameRedrawAll(event, data)



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
                       text="Press 's' to select!", font="Arial 20")


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
		data.beats.append((data.press-data.songStart, time.time()-data.songStart))
		print((data.press-data.songStart, time.time()-data.songStart))
	data.isPressed = False

def tapBeatsTimerFired(data):
	pass

def tapBeatsRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2-20,
						text="Tap your beats!", font="Arial 26 bold")
	# might turn it into a button
	canvas.create_text(data.width/2, data.height/2+40,
                       text="Press 'm' to start music.\nPress 'space' to create your beats!\nPress 's' to start the game!", font="Arial 20")


####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
	pass

def playGameKeyPressed(event, data):
	pass

def playGameKeyRelease(event, data):
	pass

def playGameTimerFired(data):
	data.timer += 1
	if data.timer % 30 == 0:	# game starts after 3 secs
		data.startGame = True
		data.songTimer = time.time()
	if data.startGame:
		nextBeat = data.beats[0]
		length = nextBeat[1] - nextBeat[0]
		if time.time()-data.songTimer == nextBeat[0]:
			
			

def playGameRedrawAll(canvas, data):
	canvas.create_text(data.width/2, 20,
						text="click and drag", font="Arial 20")
	if data.startGame:
		drawBeats(canvas, data)
	




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

   	# root.bind("<Key>", lambda event:
    #                        keyPressedWrapper(event, canvas, data))

	timerFiredWrapper(canvas, data)
    # and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(600, 600)