import requests
from bs4 import BeautifulSoup

import pickle

LIMIT = 3879 # Presently the last number in the PAD JP
cardPerPage = 100 # Number of cards per page, if all cards are known
def main():

	# Saves the names and numbers of cards
	cardBook = {}

	# Iterate over every page
	for i in range(1, 3, 1):
	#for i in range(39, int(LIMIT/cardPerPage)+2, 1):

		# Alternate webpage in each for loop
		PADpage = "http://pd.appbank.net/ml{}".format(i)
		index = requests.get(PADpage)
		indexSoup = BeautifulSoup(index.text, 'html.parser')

		numbers = []
		names = []

		# Find numbers and names within a specific region of the HTML file
		for ul in indexSoup.find_all('ul','list-box mb-3 spacer'):

			for li in ul.find_all('li'):

				# Strips the "No." from the number
				number = li.find('div', 'num').text.strip()[3:]

				# Directly strip the tags without modification
				name = li.find('div', 'name').text.strip()

				print("{}: {}".format(number, name))

				# If entry is known, then gather some more info about the entry
				if name != '不明':

					# Feed the corresponding webpage using number
					# If the digits of the number are < 3, do some string formatting
					while len(number) < 3:
						number = '0' + number

					monPage = "http://pd.appbank.net/m{}".format(number)
					entry = requests.get(monPage)
					entrySoup = BeautifulSoup(entry.text, 'html.parser')

					# Only obtain the numbers of the mats, evos, and pre-evos;
					# obtain the rest via a dictionary data structure, 
					# or some kind of hashing data structure

					# Pre-evo info; only found in this section
					for ul in entrySoup.find_all('ul','list-media-mim-full'):

						# This will find all 'a' tags with 'href' attribute,
						# in which we want the 'href' attribute alone
						# In addition, parse the reference link
						pre_evo = ul.find('a', href=True)['href'][2:]
						print("{} evolves from {}".format(number, pre_evo))

					# Evo and its mats
					for div in entrySoup.find_all('div','spacer mb-5'):

						title = div.find('h3','title-border mb-3')

						# Look for a certain attribute that matches a keyword
						if title and ('進化合成' in title or '究極進化' in title):
							print("{} is evolvable.".format(name))

							# Search within a specific item in this page
							# This table groups monster and the mats together
							for table in div.find_all('table', 'table mb-3'):

								print("Evolved form:")

								# This section contains the evolved form
								print(table.find('td','monster').a['href'][2:])

								print("Materials:")
								
								# This section contains all materials
								monsters = table.find('td', 'monsters')
								for mat in monsters.find_all('a',href=True):

									# Each href is a link to one material
									# We parse this link to obtain its number
									print(mat['href'][2:])


					#print("{}: {}".format(number, name))

		# Build/append the dictionary
		'''
		for i in range(len(names)):

			print("{}: {}".format(numbers[i], names[i]))

			# Skip if unknown name
			if names[i] != '不明':
				cardBook[numbers[i]] = names[i]
		'''

	'''
	for number in cardBook.keys():
		monPage = "http://pd.appbank.net/m{}".format(number)
		print(monPage)
	'''

# Open up a file


main()