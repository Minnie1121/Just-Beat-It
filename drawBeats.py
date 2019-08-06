# in playGame mode
# draw all the beats

def drawBeats(canvas, data):
	for beat in data.beats:
		length = beat[1] - beat[0]
		