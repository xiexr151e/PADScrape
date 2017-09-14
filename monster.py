'''
The object class for this program
'''

from object import Object

# Debug switch
debug = 0

class Monster:

	'''
	Class ctor
	'''
	def __init__(self, name, number, preEvo, evolutions):

		# Obvious params
		self.name = name
		self.ID = number

		# Less obvious, but we might need this for hashing
		# This will always be one value because no two monsters
		# can ever converge/evolve into one same monsters
		self.pre = preEvo

		# This will probably be an array of tuples(str key, arr value), 
		# one tuple per split evolution
		# i.e. Ney will have 5, Scheat will have 2, Mythlit will have 0
		self.post = evolutions

		# Some debug tests
		self.getName()
		self.getID()
		self.getPre()
		self.getPost()

	'''
	Returns the name of monster
	'''
	def getName(self):

		# Debug name
		if debug:
			print("My name is {}.".format(self.name))

		return self.name

	'''
	Returns the number of monster
	'''
	def getID(self):

		# Debug number
		if debug:
			print("My number is {}.".format(self.ID))

		return self.ID

	'''
	Returns the pre-evolution
	'''
	def getPre(self):

		# Debug number
		if debug:

			if not self.pre:
				print("I don't evolve from anything.")
			else:
				print("I evolve from {}.".format(self.pre))

		return self.pre

	'''
	Return evo name and its materials
	'''
	def getPost(self):

		# Debug evo and materials
		if debug:

			# Print out every dictionary
			for evoName in self.post.keys():

				# Building onto this string...
				evoStr = ''

				# Retrieve the values of this key, which should be the evo name
				evoList = self.post[evoName]

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

		return self.post

	'''
	Sets an alternate name
	'''
	def altName(self, name):
		self.altName = name

	'''
	Return a string representation of monster
	'''
	def toString(self):
		return "{}: {}".format(self.getID(), self.getName())