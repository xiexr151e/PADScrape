
'''
Look for something in a dictionary.
'''
def BookSearch(itemName, book):

	# Preemptive hash item for existence
	if itemName not in book:
		print("Item not found!")
		return

	else:
		return book.get(itemName)