# Beat stores the time in a song when the user press a key
# and how long it was held
# maybe set a maximum length?

class Beat(object):
	def __init__(self, timestamp, length):
		self.timestamp = timestamp
		self.length = length