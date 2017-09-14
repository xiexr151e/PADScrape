'''
The scraper
'''

import requests
from bs4 import BeautifulSoup
from monster import Monster
import multiprocessing
from functools import partial

# Constants
LIMIT = 3903 # Presently the last number in the PAD JP
cardPerPage = 100 # Number of cards per page, if all cards are known
firstPage = 1

# Variables and switches
lastPage = int(LIMIT / cardPerPage) + 1

# String constants. Shouldn't need to change these
PAGE_FORMAT = "http://pd.appbank.net/ml"
ENTRY_FORMAT = "http://pd.appbank.net/m"
UNKNOWN = "不明"
EVOLVE = "進化合成"
UEVO = "究極進化"

# Global dictionary
PADbook = {}

'''
Main scrape function, used to scrape the entire website
'''
def scrape(book):

	bookList = []

	# Copy global dictionary
	global PADbook
	PADbook = book
	oldLen = len(PADbook)

	# First, create a list of pages to go over
	for currentPage in range(firstPage, lastPage + 1):
		bookList.append("{}{}".format(PAGE_FORMAT, currentPage))

	# Multiprocessing for each index page
	pagePool = multiprocessing.Pool(lastPage - firstPage + 1)
	try:
		pageList = pagePool.map(scrapePage, bookList)
		for page in pageList:
			book.update(page)
	except:
		pass

	# Tells us how many new monsters are added
	print("{} new monsters added.".format(len(PADbook) - oldLen))

'''
Scrapes each page of the "table of contents" of the website
'''
def scrapePage(page):

	thisPage = {}

	index = requests.get(page)
	indexSoup = BeautifulSoup(index.text, 'html.parser')

	# Find numbers and names within a specific region of the HTML file
	for ul in indexSoup.find_all('ul','list-box mb-3 spacer'):
		for li in ul.find_all('li'):

			# Strips the "No." from the number
			number = li.find('div', 'num').text.strip()[3:]

			# Directly strip the tags without modification
			name = li.find('div', 'name').text.strip()

			# If entry is new and known, then gather some more info
			global PADbook
			if number not in PADbook.keys() and name != UNKNOWN:

				# Redirect to next function, which will help
				# to construct a new card
				newMonster = scrapeEntry(name, number)

				# Append this new card into the dictionary
				thisPage[number] = newMonster

	return thisPage


'''
Scrapes individual entries within each page
'''
def scrapeEntry(entryName, entryNumber):

	# Empty variables used to help construct the card
	pre_evo = None
	evos = {}

	# Find the alternate name for this entry
	# Due to the format of the English site, we will do this first
	# Just a debug statement
	print("New card: {}. {}".format(entryNumber, entryName))

	# Feed the corresponding webpage using number
	# If the digits of the number are < 3, do some string formatting
	while len(entryNumber) < 3:
		entryNumber = '0' + entryNumber

	# Some formatting for entry page, which we will scrape
	monPage = "{}{}".format(ENTRY_FORMAT, entryNumber)
	entry = requests.get(monPage)
	entrySoup = BeautifulSoup(entry.text, 'html.parser')

	# Redirect to find a pre-evolution, if any
	pre_evo = scrapePreEvo(entrySoup.find_all('ul','list-media-mim-full'), 
		entryNumber)

	# Finding a tag in a sea of tags
	for div in entrySoup.find_all('div','spacer mb-5'):

		# A holder for title content
		title = div.find('h3','title-border mb-3')

		# Look for a certain attribute that matches a keyword
		if title and (EVOLVE in title or UEVO in title):

			# Redirect to another function if evolution is possible
			evos = scrapeEvo(div.find_all('table', 'table mb-3'))

	# Remember to remove the trailing 0 for storage purposes
	while entryNumber[0] == '0':
		entryNumber = entryNumber[1:]

	# At the end, construct a card and return it
	return Monster(entryName, entryNumber, pre_evo, evos)

'''
Scrapes only the pre-evo section
'''
def scrapePreEvo(preSection, entryNumber):

	# Pre-evo info; only found in this section
	for ul in preSection:

		# This will find all 'a' tags with 'href' attribute,
		# in which we want the 'href' attribute alone
		# In addition, parse the reference link
		pre_evo = ul.find('a', href=True)['href'][2:]

		# Removes trailing 0s to be safe
		while pre_evo[0] == '0':
			pre_evo = pre_evo[1:]

		# Returns a parsed number
		return pre_evo

'''
Scrapes only the evo section
'''
def scrapeEvo(evoSection):

	# Make an empty dictionary to return later
	evos = {}

	# Search within a specific item in this page
	# This table groups monster and the mats together
	for table in evoSection:

		# Prepare empty variables
		evo = None
		mats = []

		# Redirect to find the evolved name
		evo = scrapeEvoName(table.find('td','monster'))

		# Redirect to find the materials
		mats = scrapeMats(table.find('td', 'monsters'))	

		# At the end, append into dictionary of evos
		evos[evo] = mats

	# Returns a dictionary, with parsed numbers as keys
	# and arrays of parsed numbers as values
	return evos

'''
Scrapes the evo name sub-section
'''
def scrapeEvoName(evoNameSection):

	# Returns a parsed number in a string
	evo_name = evoNameSection.a['href'][2:]

	# Removes trailing 0s to be safe
	while evo_name[0] == '0':
		evo_name = evo_name[1:]

	return evo_name

'''
Scrapes the evo material sub-section
'''
def scrapeMats(evoMatSection):

	# Make an empty array to return later
	mats = []
								
	# This section contains all materials
	for mat in evoMatSection.find_all('a',href=True):

		# Each href is a link to one material
		# I parse this link to obtain its number
		material = mat['href'][2:]

		# Removes trailing 0s to be safe
		while material[0] == '0':
			material = material[1:]

		# Call the nonlocal mats variable to append
		mats.append(material)

	# Returns an array of parsed numbers in strings
	return mats

