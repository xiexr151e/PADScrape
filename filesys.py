'''
Contains functions that load or save files, and other operations
'''
import pickle
import os

# Debug switch
debug = 0

'''
Load a saved dictionary, or make a new one if none exists
'''
def loadBook(bookName):

	# Get the current directory of this script
	currentDir = os.path.dirname(os.path.abspath(__file__))
	dictPath = currentDir + "/{}".format(bookName)

	if debug:
		print("Attempting to find dictionary at {}...".format(dictPath))

	# Try to see if the dictionary file exists
	dict_on_disk = os.path.isfile(dictPath)

	# Not found? No problem
	if not dict_on_disk:
		if debug:
			print("Dictionary does not exist on disk! We will make a new one.")
		return {}
	else:
		if debug:
			print("Dictionary exists on disk! Loading dictionary...")

		# Load this dictionary
		with open(bookName, "rb") as f:
			return pickle.load(f)

'''
Saves dictionary to file
'''
def saveBook(book, bookName):

	if debug:
		print("Dictionary is complete. Saving dictionary...")

	# Save this dictionary to a file
	with open(bookName, "wb") as f:
		pickle.dump(book, f)