import requests
from bs4 import BeautifulSoup

import pickle

LIMIT = 3879 # Presently the last number in the PAD JP
cardPerPage = 100 # Number of cards per page, if all cards are known
def main():

	# Saves the names and numbers of cards
	cardBook = {}

	# Iterate over every page
	for i in range(39, int(LIMIT/cardPerPage)+2, 1):

		# Alternate webpage in each for loop
		PADpage = "http://pd.appbank.net/ml{}".format(i)
		request = requests.get(PADpage)
		soup = BeautifulSoup(request.text, 'html.parser')

		numbers = []
		names = []

		# Find all the numbers and format properly
		for number in soup.find_all('div','num'):
			number = int(number.text.strip()[3:])

			# If already added, then skip
			if number not in cardBook.keys():
				numbers.append(number)

		# Find names within a specific region of the HTML file
		for ul in soup.find_all('ul', {'class' : 'list-box mb-3 spacer'}):
			for name in ul.find_all('div','name'):

				# Format
				name = name.text.strip()

				# If already added, then skip;
				# additionally, add any unknown names to preserve parallel structure
				if name == '不明' or name not in cardBook.values():
					names.append(name)

		# Build/append the dictionary
		for i in range(len(names)):

			print("{}: {}".format(numbers[i], names[i]))

			# Skip if unknown name
			if names[i] != '不明':
				cardBook[numbers[i]] = names[i]

	'''
	for number in cardBook.keys():
		monPage = "http://pd.appbank.net/m{}".format(number)
		print(monPage)
	'''

# Open up a file


main()