'''
Determines the chain and does the actual counting
'''

# Used to store endpoints
endpoints = {}

'''
Asks user for input to look for stuff in a dictionary
'''
def prompt(book):

	# For monsters, that would be the number
	# For courses, that would be the course code
	print("Please enter an ID.")

	while True:
		try:
			response = input()
			entry = book[response]

		except KeyError:
			print("Entry not found. Please enter another ID.")

		else:
			return entry

'''
Recursively determines a range of possible endpoints
'''
def possibleEnds(book, entry, endBook):

	# Base case: If already at the top of the chain, simply add and break
	if not entry.getPost():
		endBook[entry.getID()] = entry
		return

	# To traverse up the tree made by these chains, 
	for key in entry.getPost().keys():

		# This key will be the new key we will use for the next level
		# Find an entry based on the new key
		nextEntry = book[key]
		possibleEnds(book, nextEntry, endBook)

	# At the end of the loop, add itself
	endBook[entry.getID()] = entry

'''
Prints a dictionary
'''
def printDict(book):
	keys = sorted(book.keys())
	for key in keys:
		print("{}. {}".format(book[key].getID(), book[key].getName()))

'''
The sequence of events
'''
def main(book):
	print("Please pick a starting point.")

	startingPoint = prompt(book)
	print("Your starting point is {}.".format(startingPoint.getName()))

	possibleEnds(book, startingPoint, endpoints)

	# Manually delete the last entry, which should be same as 
	del endpoints[startingPoint.getID()]

	print("Possible endpoints:")
	printDict(endpoints)

	print("Please pick an endpoint.")
	endpoint = prompt(endpoints)

	print("Checking from {} to {}...".format(startingPoint.getName(), endpoint.getName()))