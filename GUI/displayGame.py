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

# standard for key hold: (keyrelease-keypress) > 1s

####################################
# init
####################################

def init(data):
	data.mode = "selectSong"
	data.beats = []		# tuple (press, release)
	data.press = 0		# at what time the key was pressed (time())
	data.songStart = 0	# when did the song start to play
	data.wasBusy = False
	data.songLength = 0

	data.isPressed = False
	data.songTimer = 0
	data.startGame = False

	data.rows = 5
	data.cols = 5
	# margin top = 60, bottom = 40
	# margin left = right = 40
	data.cellW = (data.width-80) / 5
	data.cellH = (data.height-100) / 5
	data.grid = [ [False] * 5 for row in range(5) ]

	data.circles = []
	data.lastBeat = None
	data.timer = 0
	data.levels = []	# Perfect, Good, OK, Miss

	data.score = 0
	data.miss = 0
	data.perfect = 0
	data.good = 0
	data.ok = 0



####################################
# mode dispatcher
####################################

def mousePressed(event, data):
	if (data.mode == "selectSong"): selectSongMousePressed(event, data)
	elif (data.mode == "help"): helpMousePressed(event, data)
	elif (data.mode == "tapBeats"): tapBeatsMousePressed(event, data)
	elif (data.mode == "playGame"): playGameMousePressed(event, data)
	elif (data.mode == "gameOver"): gameOverMousePressed(event, data)

def mouseRelease(event, data):
	if (data.mode == "selectSong"): selectSongMouseRelease(event, data)
	elif (data.mode == "help"): helpMouseRelease(event, data)
	elif (data.mode == "tapBeats"): tapBeatsMouseRelease(event, data)
	elif (data.mode == "playGame"): playGameMouseRelease(event, data)
	elif (data.mode == "gameOver"): gameOverMouseRelease(event, data)

def keyPressed(event, data):
	if (data.mode == "selectSong"): selectSongKeyPressed(event, data)
	elif (data.mode == "help"): helpKeyPressed(event, data)
	elif (data.mode == "tapBeats"): tapBeatsKeyPressed(event, data)
	elif (data.mode == "playGame"): playGameKeyPressed(event, data)
	elif (data.mode == "gameOver"): gameOverKeyPressed(event, data)

def keyRelease(event, data):
	if (data.mode == "selectSong"): selectSongKeyRelease(event, data)
	elif (data.mode == "help"): helpKeyRelease(event, data)
	elif (data.mode == "tapBeats"): tapBeatsKeyRelease(event, data)
	elif (data.mode == "playGame"): playGameKeyRelease(event, data)
	elif (data.mode == "gameOver"): gameOverKeyRelease(event, data)

def timerFired(data):
	if (data.mode == "selectSongTimerFired"): selectSongTimerFired(data)
	elif (data.mode == "help"): helpTimerFired(data)
	elif (data.mode == "tapBeats"): tapBeatsTimerFired(data)
	elif (data.mode == "playGame"): playGameTimerFired(data)
	elif (data.mode == "gameOver"): gameOverTimerFired(data)

def redrawAll(canvas, data):
	if (data.mode == "selectSong"): selectSongRedrawAll(canvas, data)
	elif (data.mode == "help"): helpRedrawAll(canvas, data)
	elif (data.mode == "tapBeats"): tapBeatsRedrawAll(canvas, data)
	elif (data.mode == "playGame"): playGameRedrawAll(canvas, data)
	elif (data.mode == "gameOver"): gameOverRedrawAll(canvas, data)



####################################
# selectSong mode
####################################

def browseFile():
	global fileName
	fileName = filedialog.askopenfilename(filetypes=[("All Files","*.*"),
													 ("WAV file", "*.wav"),
													 ("mp3 file", "*.mp3")])


def selectSongMousePressed(event, data):
	pass

def selectSongMouseRelease(event, data):
	pass

def selectSongKeyPressed(event, data):
	if event.keysym == 's':
		browseFile()
		if fileName != "":
			data.mode = "tapBeats"
	elif event.keysym == 'h':
		data.mode = "help"

def selectSongKeyRelease(event, data):
	pass

def selectSongTimerFired(data):
	pass

def selectSongRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2+20,
						text="Select a song you like!", 
						font="Arial 26 bold", fill="indian red")
	canvas.create_text(data.width/2, data.height/2+80,
                       text="Press 's' to select\nPress 'h' to know how to play", font="Arial 20")
	data.gameImage = PhotoImage(file = "game.gif")
	canvas.create_image(data.width/2, 180, image = data.gameImage)



####################################
# help mode
####################################

def helpMousePressed(event, data): 
	pass

def helpMouseRelease(event, data):
	pass

def helpKeyPressed(event, data):
	if (event.keysym == 's'):
		data.mode = "selectSong"

def helpKeyRelease(event, data):
	pass

def helpTimerFired(data):
	pass

def helpRedrawAll(canvas, data):
	canvas.create_text(data.width/2, 60, text = "press 's' to go back",
					   font = "Arial 26")
	intro = """\
    	- choose a song you like
    	- tap the "space" to the beats
    	- single blue circle: click on it
    	- blue and red circles with a line: 
    		click on blue circle and drag to red one
    	- "Miss":
    		click too slow
    		click at wrong places
    		drag your mouse to a wrong place
    	- score:
    		"Perfect": 10
    		"Good": 5
    		"OK": 3
    		"Miss": 0

    	ps: using a mouse would be better ;)"""

	canvas.create_text(data.width/2-30, data.height/2, text = intro, 
					   font = "Arial 16")



####################################
# tapBeats mode
####################################

def tapBeatsMousePressed(event, data):
	pass

def tapBeatsMouseRelease(event, data):
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
			data.wasBusy = True

def tapBeatsKeyRelease(event, data):
	if data.isPressed and mixer.music.get_busy():
		now = time.time()	# sec
		timestamp = (data.press-data.songStart, now-data.songStart)
		data.beats.append(timestamp)
		print(timestamp)
	data.isPressed = False

def tapBeatsTimerFired(data):
	if mixer.music.get_busy() and data.wasBusy:
		data.songLength = time.time() - data.songStart

def tapBeatsRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2-30,
					   text="Tap your beats!", font="Arial 26 bold",
					   fill="indian red")
	# might turn it into a button
	canvas.create_text(data.width/2, data.height/2+50,
                       text="Press 'm' to start music\nPress 'space' to create your beats\nPress 's' to start the game", font="Arial 20")



####################################
# playGame mode
####################################

def almostEqual(x, y):
	return 0 <= abs(x-y) <= 0.1		# 0.1 sec

def clickLevel(data, clickTime, circle):
	# data.isClicked == True for this function
	# releaseTime will be the clickTime for longCir
	diff = clickTime - circle.timestamp[0]
	length = circle.timestamp[1] - circle.timestamp[0]
	if circle.isLongCir():
		if 0 <= diff <= 0.7:
			data.score += 10
			data.perfect += 1
			return "Perfect"
		elif diff <= 1:
			data.score += 5
			data.good += 1
			return "Good"
		elif diff <= max(length, 3):
			data.score += 3
			data.ok += 1
			return "OK"
		else:
			data.miss += 1
			return "Miss"
	else:
		if 0 <= diff <= 0.7:
			data.score += 10
			data.perfect += 1
			return "Perfect"
		elif diff <= 1:
			data.good += 1
			data.score += 5
			return "Good"
		elif diff <= max(length, 2):
			data.ok += 1
			data.score += 3
			return "OK"
		else:
			data.miss += 1
			return "Miss"


def playGameMousePressed(event, data):
	# deal with normal circles in mouse press
	# only change the state of data.isClicked for long circles here
	data.isClicked = True
	if not data.startGame:
		if 0 < event.x < data.width and 0 < event.y < data.height:
			data.startGame = True
			data.songTimer = time.time()	# sec; when the music (game) starts
			mixer.music.load(fileName)
			mixer.music.play()
	elif mixer.music.get_busy():
		toRemove = []
		for circle in data.circles:
			if circle.clickedIn(event.x, event.y):
				circle.isTouched = True  # for later check on the long circle
				if not circle.isLongCir():
					clickTime = time.time() - data.songTimer
					level = clickLevel(data, clickTime, circle)
					data.levels.append((level, circle))
					toRemove.append(circle)
			else:	
				miss = True
				for circle in toRemove:
					if circle.clickedIn(event.x, event.y):
						miss = False	# if click outside the circle 
										# but within another one
				if miss:
					level = "Miss"
					data.miss += 1
					data.levels.append((level, circle))
					toRemove.append(circle)
		remaining = []
		for circle in data.circles:
			if circle not in toRemove:
				remaining.append(circle)
		data.circles = remaining


def playGameMouseRelease(event, data):
	# deal with long circles in mouse release
	if data.isClicked and mixer.music.get_busy():
		toRemove = []
		for circle in data.circles:
			if circle.isLongCir():
				if circle.isTouched:
					if circle.releasedIn(event.x, event.y):
						releaseTime = time.time() - data.songTimer
						level = clickLevel(data, releaseTime, circle)
						data.levels.append((level, circle))
						toRemove.append(circle)
					else:
						level = "Miss"
						data.miss += 1
						data.levels.append((level, circle))
						toRemove.append(circle)
				else:
					if time.time()-data.songTimer > circle.timestamp[1]:
						level = "Miss"
						data.miss += 1
						data.levels.append((level, circle))
						toRemove.append(circle)
		remaining = []
		for circle in data.circles:
			if circle not in toRemove:
				remaining.append(circle)
		data.circles = remaining
	data.isClicked = False


def playGameKeyPressed(event, data):
	pass

def playGameKeyRelease(event, data):
	pass

def playGameTimerFired(data):
	if data.startGame:
		if not mixer.music.get_busy():
			data.mode = "gameOver"
		else:
			data.timer += 1
			for circle in data.circles:
				circle.timer += 1

			for beat in data.beats:
				if (almostEqual(data.timer/10, beat[0]) 
						and beat != data.lastBeat):
					data.circles.append(Circle(beat, 0))
					# avoid the extra timerFired calls
					data.lastBeat = beat
					break

			toRemove = []
			for circle in data.circles:
				length = circle.timestamp[1] - circle.timestamp[0]
				if length < 1:	# key press
					if almostEqual(data.timer/10, 
								   circle.timestamp[0]+2):
						toRemove.append(circle)
				else:			# key hold
					if almostEqual(data.timer/10, 
								   circle.timestamp[0]+max(3, length)):
						toRemove.append(circle)
			remaining = []
			for circle in data.circles:
				if circle not in toRemove:
					remaining.append(circle)
				elif circle in toRemove and not data.isClicked:
					circle.level = "Miss"
					data.miss += 1
			data.circles = remaining


def playGameRedrawAll(canvas, data):
	canvas.create_text(data.width/2-25, 20, font="Arial 17",
					   text="click anywhere to start game\tScore: %d\t Miss: %d" % (data.score, data.miss))
	if mixer.music.get_busy():
		data.grid = [ [False] * 5 for row in range(5) ]
		for circle in data.circles:
			if data.songLength-circle.timestamp[1] > 2:
				# not drawing the very last beats
				circle.draw(canvas, data)
		while len(data.levels) > 0:
			print(data.levels)
			nextLevel = data.levels[0]
				# nextLevel: tuple of (text, Circle)
			if nextLevel[1].isLongCir():
				x, y = nextLevel[1].othercx, nextLevel[1].othercy-20
			else:
				x, y = nextLevel[1].cx, nextLevel[1].cy-20
			canvas.create_text(x, y, text = nextLevel[0], 
							   font = "Arial 20", fill = "indian red")
			data.levels.pop(0)




####################################
# gameOver mode
####################################

def gameOverMousePressed(event, data):
	pass

def gameOverMouseRelease(event, data):
	pass

def gameOverKeyPressed(event, data):
	pass

def gameOverKeyRelease(event, data):
	pass

def gameOverTimerFired(data):
	pass

def gameOverRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2-10,
					   text = "Your Score: %d" % data.score,
					   font = "Arial 26 bold", fill = "indian red")
	canvas.create_text(data.width/2, data.height/2+100,
					   text="Miss: %d\nPerfect: %d\nGood: %d\nOK: %d" % 
					   		(data.miss, data.perfect, data.good, data.ok),
					   font="Arial 24")
	
	data.goodImage = PhotoImage(file = "good.gif")
	canvas.create_image(data.width/2, 180, image = data.goodImage)






# run function taken from 15-112 course note "mode demo"
# but I modified the mouse and key functions
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

	def mouseReleaseWrapper(event, canvas, data):
		mouseRelease(event, data)
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

	root = Tk()
	root.title("Just Beat It!")
	mixer.init()

	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<ButtonRelease-1>", lambda event:
							mouseReleaseWrapper(event, canvas, data))
	root.bind('<KeyPress>', lambda event:
							keyPressedWrapper(event, canvas, data))
	root.bind('<KeyRelease>', lambda event: 
							keyReleaseWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
    # and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(600, 600)