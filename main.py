# Take in command line args
import sys

# The scraper
import PADScrape

# Import object to let us create a debugger
from object import Object

'''
The program launcher
'''

# This debugger is set to off by default
debugger = Object("Debugger", 0)

# Check for debug flag
if "-x" in sys.argv:
	debugger.set_debug(1)

# Then check if command-line args are correct
elif len(sys.argv) != 1:

	# Prints correct usage and exits
	print("Usage: python3 main.py [-x]")
	sys.exit(1)

# Load assets and execute
PADScrape.loadBook(debugger)
PADScrape.scrape(debugger)
PADScrape.saveBook(debugger)