# learnt (but not directly copied) from
# https://www.youtube.com/watch?v=Dp_YxvqYDwU&t=515s

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pygame import mixer


root = Tk()

mixer.init()

def browseFile():
	global fileName
	fileName = filedialog.askopenfilename(filetypes = [("WAV file", "*.wav")])


"""
def playMusic():
	try:
		paused
	except NameError: # if "paused" hasn't been initialized -> play new music
		try:
			mixer.music.load(fileName)
			mixer.music.play()
		except:
			messagebox.showerror("File not found.", "No Music:(")
	else:  # if paused, resume the paused music
		mixer.music.unpause()

def pauseMusic():
	global paused
	paused = True
	mixer.music.pause()

def stopMusic():
	mixer.music.stop()



buttonFrame = Frame(root)
buttonFrame.pack()

def browseButton():
	browseBtn = Button(buttonFrame, text = "Browse", command = browseFile)
	browseBtn.pack(side = LEFT)

def buttons():
	browseButton()

	playBtn = Button(buttonFrame, text = "Play", command = playMusic)
	playBtn.pack(side = LEFT)

	pauseBtn = Button(buttonFrame, text = "Pause", command = pauseMusic)
	pauseBtn.pack(side = LEFT)

	stopBtn = Button(buttonFrame, text = "Stop", command = stopMusic)
	stopBtn.pack(side = LEFT)

"""