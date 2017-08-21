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

		# Find numbers and names within a specific region of the HTML file
		for ul in soup.find_all('ul', {'class' : 'list-box mb-3 spacer'}):

			for li in ul.find_all('li'):

				number = li.find('div', 'num').text.strip()[3:]
				name = li.find('div', 'name').text.strip()

				if name != '不明':
					print("{}: {}".format(number, name))

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