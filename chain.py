'''
Determines the chain and does the actual counting
'''

# Used to store endpoints
endpoints = {}

# Used to store the main chain itself
mainChain = []

# Used to store the requirements for the chain
requirements = {}

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
Builds a chain to determine the sequence by going from end to beginning
'''
def buildChain(end, start, book):

	chainArr = []

	# If called from a recursive call (no starting point), 
	# go to the very base of possible chain
	if not start:
		while end.getPre():
			# Append the first link 
			ID = end.getID()

			while ID[0] == '0':
				ID = ID[1:]

			chainArr.append(book[ID])

			# Obtain the previous evolution entry if we haven't seen the end
			end = book[end.getPre()]
		chainArr.append(end)

	else:
		# While not at the other end of the chain
		while end != start:

			# Append the first link 
			ID = end.getID()

			while ID[0] == '0':
				ID = ID[1:]

			chainArr.append(book[ID])

			# Obtain the previous evolution entry if we haven't seen the end
			end = book[end.getPre()]

		# Append the starting point at the very end
		chainArr.append(start)

	# Return this new array
	return chainArr

'''
Iterates through the chain links
'''
def iterReq(chainArr, book, reqBook):

	# Start at second last link of the chain, where the (necessary) reqs end
	for entryIndex in range(len(chainArr) - 1, 0, -1):

		# We only need the name of the current link, because that's our key
		preLink = chainArr[entryIndex]
		curLinkID = chainArr[entryIndex - 1].getID()

		while curLinkID[0] == '0':
			curLinkID = curLinkID[1:]

		# Obtain the requirements to the next link from the current link
		preReq = preLink.getPost()[curLinkID]

		# Iterate through these
		for reqs in preReq:
			findReq(reqs, book, reqBook)

'''
Recursively extract sub-requirements within requirements
'''
def findReq(entry, book, reqBook):

	# Obtain the entry object, by using entry which is also a key
	entryObj = book[entry]

	# Also obtain its name, which will be used to store within dictionary
	entryName = entryObj.getName()

	# Check if the object does not have a pre-req
	# If it does not, then append directly; else, recursive calls and append

	if entryObj.getPre():

		# By recursive calls, I mean that we will create a new chain
		subChain = buildChain(entryObj, None, book)
		iterReq(subChain, book, reqBook)

		# Also reduce the entry to be its lowest form
		while entryObj.getPre():
			entryObj = book[entryObj.getPre()]
			entryName = entryObj.getName()
	
	# Check for duplicates; if none, add new
	# If any, add 1 to value
	if entryName not in reqBook.keys():
		reqBook[entryName] = 1

	else:
		reqBook[entryName] = reqBook[entryName] + 1




'''
Prints a dictionary
'''
def printDict(book):
	keys = sorted(book.keys())
	for key in keys:
		print("{}. {}".format(book[key].getID(), book[key].getName()))

'''
Prints an array
'''
def printArr(arr):
	for entry in arr:
		print("{}. {}".format(entry.getID(), entry.getName()))

'''
Prints the final results
'''
def printResult(start, end, reqBook):

	# The original string
	resStr = "To get from {} to {}, you need:\n".format(start.getName(), 
		end.getName())

	# More hard-coded goodness
	for entry in reqBook.keys():
		resStr += "{} {}\n".format(entry, reqBook[entry])

	# Print the final result. We earned it!
	print(resStr)



'''
The sequence of events
'''
def main(book):

	print("Please pick a starting point.")

	startingPoint = prompt(book)
	print("Your starting point is {}.".format(startingPoint.getName()))

	possibleEnds(book, startingPoint, endpoints)

	print("Possible endpoints:")
	printDict(endpoints)

	print("Please pick an endpoint.")
	endpoint = prompt(endpoints)

	print("Checking from {} to {}...".format(startingPoint.getName(), 
		endpoint.getName()))

	mainChain = buildChain(endpoint, startingPoint, book)
	printArr(mainChain)

	iterReq(mainChain, book, requirements)

	printResult(startingPoint, endpoint, requirements)