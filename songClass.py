# beats[]: a list of timestamps (int)

class Song(object):
	def __init__(self, filePath, bestScore, bestCombo, beats=[]):
		self.filePath = filePath
		self.bestScore = bestScore
		self.bestCombo = bestCombo
		self.beats = beats

