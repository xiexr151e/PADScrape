from object import Object

class Monster:

	'''
	Class ctor
	'''
	def __init__(self, name, number, preEvo, evolutions, object):

		# Obvious params
		self.name = name
		self.number = number

		# Less obvious, but we might need this for hashing
		# This will always be one value because no two monsters
		# can ever converge/evolve into one same monsters
		self.preEvo = preEvo

		# This will probably be an array of tuples(str key, arr value), 
		# one tuple per split evolution
		# i.e. Ney will have 5, Scheat will have 2, Mythlit will have 0
		self.evolutions = evolutions

		# Debug flag for all your message goods
		self.debug = object.debug

		# Some debug tests
		self.getName()
		self.getNum()
		self.getPreEvo()
		self.getEvo()

	'''
	Returns the name of monster
	'''
	def getName(self):

		# Debug name
		if self.debug:
			print("My name is {}.".format(self.name))

		return self.name

	'''
	Returns the number of monster
	'''
	def getNum(self):

		# Debug number
		if self.debug:
			print("My number is {}.".format(self.number))

		return self.number

	'''
	Returns the pre-evolution
	'''
	def getPreEvo(self):

		# Debug number
		if self.debug:

			if not self.preEvo:
				print("I don't evolve from anything.")
			else:
				print("I evolve from {}.".format(self.preEvo))

		return self.preEvo

	'''
	Return evo name and its materials
	'''
	def getEvo(self):

		# Debug evo and materials
		if self.debug:

			# Print out every dictionary
			for evoName in self.evolutions.keys():

				# Building onto this string...
				evoStr = ''

				# Retrieve the values of this key, which should be the evo name
				evoList = self.evolutions[evoName]

				# Build a string for this branch
				for j in range(len(evoList)):
					evoStr += evoList[j]

					# Some special hard-coded things because English
					if j == len(evoList) - 1:
						evoStr += '.'
					else:
						evoStr += ', '

						if j == len(evoList) - 2:
							evoStr += 'and '

				# The completed print statement here
				print("To evolve {} into {}, you need: {}".format(self.name, evoName, evoStr))

		return self.evolutions			

	'''
	A search function - we use this to recursively search for stuff in a dictionary.
	book - The dictionary itself.
	arr - The array of things to print out.
	freq - Array parallel to arr to keep track of frequency.
	'''
	def search(self, book, arr, freq):

		
		#Base case - return if no evolution beyond this point.
		if len(self.evolutions) == 0:
			return
		
		#Do the recursive search
		#for i in range(len(self.evolutions)):