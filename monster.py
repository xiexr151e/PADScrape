from object import Object

class Monster:

	'''
	Class ctor
	'''
	def __init__(self, name, number, evolutions, object):

		# Obvious params
		self.name = name
		self.number = number

		# This will probably be an array of tuples(str key, arr value), 
		# one tuple per split evolution
		# i.e. Ney will have 5, Scheat will have 2, Mythlit will have 0
		self.evolutions = evolutions

		# Debug flag for all your message goods
		self.debug = object.debug

		# Some debug tests
		self.getName()
		self.getNum()
		self.getEvo()

	'''
	Returns the name of monster
	'''
	def getName(self):

		# Debug name
		if self.debug:
			print("My name is {}".format(self.name))

		return self.name

	'''
	Returns the number of monster
	'''
	def getNum(self):

		# Debug number
		if self.debug:
			print("My number is {}".format(self.number))

		return self.number

	'''
	Return evo name and its materials
	'''
	def getEvo(self):

		# Debug evo and materials
		if self.debug:

			# Print out every dictionary
			for i in range(len(self.evolutions)):
				branch = self.evolutions[i]

				# Building onto this string...
				evoStr = ''

				# Retrieve the values of this key, which should be the evo name
				evoName = branch[0]
				evoList = branch[1]

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

				print("To evolve {} into {}, you need: {}".format(self.name, evoName, evoStr))

		return self.evolutions

	'''
	Makes a "chain" we can use for the search function.
	current - The current item we are on. Unused for now.
	target - The target we are reaching for.
	book - The book to search in.
	arr - The arr to store the chain.
	'''
	def getChain(self, current, target, book, arr):

		tree = [[self]]

		# Recursively search in this tree...
		# For now, we can use 2D arrays, but once the
	  	# evolution tree gets too complex, we need to change this
		for i in range(len(self.evolutions)):
			

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
		for i in range(len(self.evolutions)):

DEBUG_ON = 1
DEBUG_OFF = 0

Debugger = Object("A", DEBUG_ON)
Hino = Monster("Kagutsuchi", 132, [("Hino Kagutsuchi", ["Red Mask", "Mythlit", "Mythlit", "Keeper of Red", "Keeper of Red"])], Debugger)
Andromeda = Monster("Andromeda", 420, [("Big Andromeda", ["Keeper of Gold", "Blue Mask", "Blue Jewel"]), [("Awoken Andromeda"), ["Ilsix", "Gaia"]]], Debugger)