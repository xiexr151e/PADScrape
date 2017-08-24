'''
The program launcher
'''

import sys
import PADScrape
from object import Object
import filesys
import chain

# String constant for launcher
BOOK_NAME = "cardbook"

# A common dictionary
cardbook = {}

# This debugger is set to off by default
debugger = Object("Debugger", 0)

# Check for debug flag
if "-x" in sys.argv:
	debugger.set_debug(1)

# Call loader
cardbook = filesys.loadBook(BOOK_NAME, debugger)

# Check for update flag
# If updating, terminate once complete
if "-u" in sys.argv:
	PADScrape.scrape(cardbook, debugger)
	filesys.saveBook(cardbook, BOOK_NAME,debugger)
	sys.exit(0)

# Anything else, do chains
else:
	chain.main(cardbook)



