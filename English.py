import requests
from bs4 import BeautifulSoup, SoupStrainer
#from BeautifulSoup import SoupStrainer

# Exception: Exclude Crows collab and Voltron collab
Crows = list(range(2601, 2636)) + list(range(3460, 3482))
Voltron = list(range(2601, 2632))

# String constant
EN_FORMAT = "http://www.puzzledragonx.com/en/monster.asp?n="

'''
Translates a single entry into its English equivalent.
May fail on certain exclusives and collabs and etc. Sorry.
'''
def translateEntry(entry):

	if not entry:
		print("Can't translate this.")
		return

	# Make a copy of number first
	numCopy = entry.getID()
	
	# Exception for one collab
	if int(numCopy) in Crows:
		numCopy = '1' + numCopy

	# Make a soup based on the PADx page
	ENPage = "{}{}".format(EN_FORMAT, numCopy)
	ENentry = requests.get(ENPage)
	ENParser = SoupStrainer('div', {'class':'name'})
	ENsoup = BeautifulSoup(ENentry.text, 'html.parser', parse_only = ENParser)

	# Find the name and return it
	EN_name = ENsoup.text.strip()

	# Check if the English text exists
	if not ENsoup or not ENPage or not ENentry or not EN_name:
		return entry.getName()

	return EN_name