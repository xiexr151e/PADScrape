'''
Determines the chain and does the actual counting
'''
import English
from multiprocessing import Pool

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

	# Check if the object does not have a pre-req
	# If it does not, then append directly; else, recursive calls and append

	if entryObj.getPre():

		# By recursive calls, I mean that we will create a new chain
		subChain = buildChain(entryObj, None, book)
		iterReq(subChain, book, reqBook)

		# Also reduce the entry to be its lowest form
		while entryObj.getPre():
			entryObj = book[entryObj.getPre()]
			#entryName = entryObj.getName()
	
	# Check for duplicates; if none, add new
	# If any, add 1 to value
	if entryObj not in reqBook.keys():
		reqBook[entryObj] = 1

	else:
		reqBook[entryObj] = reqBook[entryObj] + 1

'''
Prints a dictionary
'''
def printDict(book):

	# Prepare a list we need for translation
	values = list(book.values())

	# Multiprocessing pool
	engPool = Pool(5)
	engList = engPool.map(English.translateEntry, values)

	# Print a dictionary alonside an array
	printCount = 0
	for entry in values:
		print("{} ({})".format(entry.toString(), 
			engList[printCount]))
		printCount += 1

	print()

'''
Prints the final results
'''
def printResult(start, end, reqBook):

	# The original string
	resStr = "To get from {} ({}) to {} ({}), you need:\n\n".format(
		start.getName(), English.translateEntry(start), 
		end.getName(), English.translateEntry(end))

	# Just because we wanna see how many items are in here
	total = 0

	# Multiprocessing pool
	engPool = Pool(5)
	engList = engPool.map(English.translateEntry, reqBook)
	printCount = 0

	# Print out and add up stuff
	for entry in reqBook.keys():
		resStr += "{}({}) x {}\n".format(entry.getName(), 
			engList[printCount], reqBook[entry])
		printCount += 1
		total += int(reqBook[entry])

	# Print the final result. We earned it!
	print(resStr)
	print("Total amount of requirements: {}".format(total))



'''
The sequence of events
'''
def main(book):

	# Prompt user for starting point
	print("Please pick a starting point.")
	startingPoint = prompt(book)
	print("Your starting point is {}.".format(startingPoint.getName()))

	# Determine a list of endpoints
	possibleEnds(book, startingPoint, endpoints)
	# Delete the starting point. That is not an endpoint
	endpoints.pop(startingPoint.getID())

	# Print endpoints
	print("Possible endpoints:\n")
	printDict(endpoints)

	# Prompt user for endpoint
	print("Please pick an endpoint.")
	endpoint = prompt(endpoints)

	# Determine requirements
	print("Checking from {} to {}...".format(startingPoint.getName(), 
		endpoint.getName()))
	mainChain = buildChain(endpoint, startingPoint, book)
	iterReq(mainChain, book, requirements)

	# Print final result
	printResult(startingPoint, endpoint, requirements)

	return requirements