from abc import ABC, abstractmethod

class Object(ABC):

	def __init__(self, name, debug):
		self.name = name
		self.debug = debug

	'''
	Lets us set the debug flag
	'''
	def set_debug(self, debug):
		self.debug = debug

	'''
	An abstract function - this base function can be used to
	recursively search and print things. I have pre-requisites in mind.
	'''
	def search(self, book, arr, freq):
		print("Nope")
		raise NotImplementedError