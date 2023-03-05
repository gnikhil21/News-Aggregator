import requests
from bs4 import BeautifulSoup

word = 'theft'
url = f'https://www.thesaurus.com/browse/{word}'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

synonyms_div = soup.find('ul', {'class': 'css-x6mqrn e1ccqdb60'})
synonyms_list = synonyms_div.find_all('a')
synonyms = [s.text.strip() for s in synonyms_list]#.find_all('a')]

print(f"Synonyms of {word}: {synonyms}")
