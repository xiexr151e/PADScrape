'''
The program launcher
'''

import sys
import PADScrape
from object import Object
import filesys
import chain
import monster

# String constant for launcher
BOOK_NAME = "cardbook"

# A common dictionary
cardbook = {}

# a results dictionary
results = {}

# Check for debug flag
if "-x" in sys.argv:
	filesys.debug = 1
	monster.debug = 1

# Call loader
cardbook = filesys.loadBook(BOOK_NAME)

# Check for update flag
# If updating, terminate once complete
if "-u" in sys.argv:
	PADScrape.scrape(cardbook)
	chain.main(cardbook)
	filesys.saveBook(cardbook, BOOK_NAME)
	sys.exit(0)

# Anything else, do chains
else:
	chain.main(cardbook)



